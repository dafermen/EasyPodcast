"""Local-library administration, portable packages and review-before-restore endpoints."""

import asyncio

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse

from . import library, packages
from .config import settings
from .jobs import ACTIVE, store
from .models import ItemName, PurgeConfirmation, SubtitleDraftRequest


def attach(app, get_job, editable):
    """Register routes before the static frontend mount, reusing the existing job security boundary."""

    def authorized(request: Request):
        """Require the same-origin local-library cookie on every administration/transfer route."""
        library.authorize(request)

    router = APIRouter(prefix="/api", dependencies=[Depends(authorized)])

    @router.get("/library/usage")
    def usage():
        """Report local storage and package budgets without returning filesystem paths."""
        return {
            **library.usage(),
            "max_bundle_bytes": settings.max_bundle_bytes,
            "max_expanded_bytes": settings.max_bundle_expanded_bytes,
        }

    @router.get("/library/trash")
    def trash():
        """List recoverable project/template records and the space they still occupy."""
        return library.trash_items()

    @router.patch("/library/items/{kind}/{identifier}")
    def rename(kind: str, identifier: str, body: ItemName):
        """Change a library label, retaining the video's original title."""
        if not body.title.strip():
            raise ValueError("Name cannot be blank.")
        library.rename(kind, identifier, body.title)
        return {"renamed": True}

    @router.post("/library/items/{kind}/{identifier}/trash")
    def move_to_trash(kind: str, identifier: str):
        """Checkpoint and close idle workspaces before the explicitly requested recoverable move."""
        with store.lock:
            affected = (
                [job for job in store.jobs.values() if job.project_id == identifier]
                if kind == "projects"
                else []
            )
            for job in affected:
                editable(job)
            for job in affected:
                store.checkpoint(job)
                if job.archive_error:
                    raise HTTPException(507, job.archive_error)
            library.trash_item(kind, identifier)
            for job in affected:
                store.remove_path(job.path)
                del store.jobs[job.id]
        return {"trashed": True}

    @router.post("/library/trash/{kind}/{identifier}/restore")
    def restore(kind: str, identifier: str):
        """Recover an item from Trash without duplicating its identity or dropping its drafts."""
        library.restore_trash(kind, identifier)
        return {"restored": True}

    @router.delete("/library/trash/{kind}/{identifier}")
    def purge(kind: str, identifier: str, body: PurgeConfirmation):
        """Permanently delete only after the UI supplies the item's exact confirmation name."""
        library.purge_trash(kind, identifier, body.confirmation)
        return {"deleted": True}

    @router.put("/projects/{identifier}/subtitle-draft")
    def caption_draft(identifier: str, body: SubtitleDraftRequest):
        """Persist incomplete subtitle edits without mutating saved cues or approving a render."""
        # Keep the database draft and live render gate in the same critical section as explicit saves.
        with store.lock:
            saved = library.save_caption_draft(identifier, body.srt, body.base_digest, body.base_version)
            if saved:
                for job in store.jobs.values():
                    if job.project_id == identifier:
                        job.subtitle_draft_available = True
        return {"saved": saved}

    @router.delete("/projects/{identifier}/subtitle-draft")
    def discard_caption_draft(identifier: str):
        """Advance the generation when the user explicitly discards subtitle corrections."""
        with store.lock:
            library.project(identifier)
            library.clear_caption_draft(identifier)
            for job in store.jobs.values():
                if job.project_id == identifier:
                    job.subtitle_draft_available = False
        return {"discarded": True}

    async def prepare(request, scope, identifier=None):
        """Freeze saved state, build a bounded disk-backed package, then return a single-use download."""
        manager = request.app.state.transfers
        async with request.app.state.bundle_slot:
            entry = manager.begin("export")
            try:
                if identifier:
                    with store.lock:
                        library.project(identifier)
                        for job in store.jobs.values():
                            if job.project_id == identifier and job.state not in ACTIVE:
                                store.checkpoint(job)
                                if job.archive_error:
                                    raise HTTPException(507, job.archive_error)
                output = await asyncio.to_thread(packages.build, entry["path"], scope, identifier)
                filename = f"easypodcast-{scope}-{entry['id'][:8]}.zip"
                manager.ready(entry, filename=filename, output=output)
                return {
                    "url": f"/api/library/exports/{entry['id']}",
                    "filename": filename,
                    "bytes": output.stat().st_size,
                    "expires_at": entry["expires"],
                }
            except BaseException:
                manager.discard(entry["id"])
                raise

    @router.post("/projects/{identifier}/export")
    async def export_project(identifier: str, request: Request):
        """Export inputs, media, completed outputs, appearance and subtitle recovery drafts."""
        return await prepare(request, "project", identifier)

    @router.post("/library/backup")
    async def backup(request: Request):
        """Back up projects/templates including Trash, without the machine-local capability or database file."""
        return await prepare(request, "library")

    @router.get("/library/exports/{identifier}")
    def download(identifier: str, request: Request):
        """Stream a built ZIP and clean its private staged files even after client disconnection."""
        manager = request.app.state.transfers
        lease = manager.lease(identifier, "export")
        entry = lease.__enter__()

        class Download(FileResponse):
            """Hold the transfer lease for the entire response lifetime."""

            async def __call__(self, scope, receive, send):
                """Release resources on normal completion, range completion or disconnect."""
                try:
                    await super().__call__(scope, receive, send)
                finally:
                    lease.__exit__(None, None, None)
                    manager.discard(identifier)

        return Download(
            entry["output"],
            media_type="application/zip",
            filename=entry["filename"],
            headers={"Cache-Control": "no-store"},
        )

    @router.delete("/library/exports/{identifier}")
    def cancel_export(identifier: str, request: Request):
        """Release an unused prepared download without retaining an inaccessible transfer slot."""
        manager = request.app.state.transfers
        with manager.lease(identifier, "export"):
            pass
        manager.discard(identifier)
        return {"cancelled": True}

    @router.post("/library/import")
    async def preview_import(request: Request):
        """Stream a ZIP to a bounded workspace and return a validated review before installation."""
        manager = request.app.state.transfers
        if request.app.state.upload_slot.locked():
            raise HTTPException(429, "An upload is already in progress.")
        async with request.app.state.upload_slot, request.app.state.bundle_slot:
            entry = manager.begin("import")
            try:
                size = 0
                with (entry["path"] / "upload.zip").open("xb") as target:
                    async with asyncio.timeout(settings.active_ttl_seconds):
                        async for block in request.stream():
                            size += len(block)
                            if size > settings.max_bundle_bytes:
                                raise HTTPException(413, "Package exceeds the configured size limit.")
                            if (
                                library.shutil.disk_usage(entry["path"]).free
                                < len(block) + settings.min_free_bytes
                            ):
                                raise HTTPException(507, "Insufficient disk space to import this package.")
                            target.write(block)
                report = await asyncio.to_thread(packages.inspect_package, entry["path"])
                manager.ready(entry, report=report)
                return {**report, "ticket": entry["id"], "expires_at": entry["expires"]}
            except BaseException:
                manager.discard(entry["id"])
                raise

    @router.post("/library/imports/{identifier}/confirm")
    async def confirm(identifier: str, request: Request):
        """Install only a previously verified review ticket as independent new copies."""
        manager = request.app.state.transfers
        async with request.app.state.bundle_slot:
            with manager.lease(identifier, "import") as entry:
                result = await asyncio.to_thread(packages.install, entry["path"])
            manager.discard(identifier)
            return result

    @router.delete("/library/imports/{identifier}")
    def cancel_import(identifier: str, request: Request):
        """Cancel an unconfirmed import without changing any durable project."""
        manager = request.app.state.transfers
        with manager.lease(identifier, "import"):
            pass
        manager.discard(identifier)
        return {"cancelled": True}

    app.include_router(router)
