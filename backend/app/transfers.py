"""Short-lived package transfer tickets with leases and UUID-only temporary cleanup."""

import shutil
import threading
import time
import uuid
from contextlib import contextmanager

from fastapi import HTTPException


class TransferManager:
    """Own staged package files, expiry and single-consumer leases independently of job credentials."""

    def __init__(self, root):
        """Bind cleanup to the workspace root resolved at application startup."""
        self.root = root.resolve()
        self.lock = threading.RLock()
        self.entries = {}

    def remove(self, path):
        """Delete only an exact UUID directory allocated by this manager under its captured root."""
        if (
            path.parent.resolve() != self.root
            or len(path.name) != 32
            or any(c not in "0123456789abcdef" for c in path.name)
            or path.is_symlink()
            or path.is_junction()
        ):
            raise ValueError("Invalid package staging directory.")
        if path.exists():
            shutil.rmtree(path)

    def begin(self, kind):
        """Reserve one bounded transfer slot and an empty private staging directory."""
        with self.lock:
            self.clean()
            if len(self.entries) >= 3:
                raise HTTPException(429, "Finish or cancel an existing package transfer first.")
            identifier = uuid.uuid4().hex
            stage = self.root / identifier
            stage.mkdir(mode=0o700)
            entry = {
                "id": identifier,
                "path": stage,
                "kind": kind,
                "expires": time.time() + 1800,
                "busy": True,
            }
            self.entries[identifier] = entry
            return entry

    def ready(self, entry, **metadata):
        """Publish a completed build/validation ticket and its review metadata."""
        with self.lock:
            entry.update(metadata, busy=False, expires=time.time() + 1800)

    def discard(self, identifier):
        """Consume a transfer after success/cancel; active leases must be ended by their owner."""
        with self.lock:
            entry = self.entries.pop(identifier, None)
            if entry:
                self.remove(entry["path"])

    @contextmanager
    def lease(self, identifier, kind):
        """Prevent duplicate confirmation/download and protect staged files from expiry while in use."""
        with self.lock:
            self.clean()
            entry = self.entries.get(identifier)
            if not entry or entry["kind"] != kind:
                raise HTTPException(404, "Package transfer expired. Prepare it again.")
            if entry["busy"]:
                raise HTTPException(409, "This package transfer is already in progress.")
            entry["busy"] = True
        try:
            yield entry
        finally:
            with self.lock:
                if identifier in self.entries:
                    entry["busy"] = False

    def clean(self, force=False):
        """Expire idle tickets; a busy download/import is never removed underneath its consumer."""
        with self.lock:
            for identifier, entry in list(self.entries.items()):
                if not entry["busy"] and (force or time.time() > entry["expires"]):
                    self.discard(identifier)
