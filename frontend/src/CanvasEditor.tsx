import { useRef, useState } from "react";
import type { Design, Job } from "./types";
import { artifactUrl } from "./api";
import { t } from "./i18n";
import { fontFamilies } from "./TypographyControls";
/** Output dimensions are shared by composition sizing and direct-manipulation math. */
export function frameSize(design?: Design | null): [number, number] {
  return design?.output_format === "portrait"
    ? [1080, 1920]
    : design?.output_format === "square"
      ? [1080, 1080]
      : [1920, 1080];
}
/** Convert pointer motion in the displayed canvas to pixels in the actual output frame. */
export function canvasDelta(
  dx: number,
  dy: number,
  rect: { width: number; height: number },
  frame: [number, number],
) {
  return [(dx / rect.width) * frame[0], (dy / rect.height) * frame[1]];
}
/** Match FFmpeg logo coordinates, including clamping free placement to the visible frame. */
export function logoBox(
  design: Design,
  frame: [number, number],
  natural: { width: number; height: number },
) {
  const [width, height] = frame;
  const position = design.logo_position ?? "top-right";
  const margin = design.logo_margin ?? 40;
  const w = natural.width * (design.logo_scale ?? 1);
  const h = natural.height * (design.logo_scale ?? 1);
  const left =
    design.logo_x != null
      ? Math.min(width - w, Math.max(0, width * design.logo_x))
      : position.endsWith("right")
        ? width - w - margin
        : margin;
  const top =
    design.logo_y != null
      ? Math.min(height - h, Math.max(0, height * design.logo_y))
      : position.startsWith("middle")
        ? (height - h) / 2
        : position.startsWith("bottom")
          ? height - h - margin
          : margin;
  return { left, top, width: w, height: h };
}
/** Drag title/logo, resize them and use keyboard arrows; approval remains a separate explicit action. */
export function CanvasEditor({
  job,
  design,
  revision,
  disabled,
  change,
}: {
  job: Job;
  design: Design;
  revision: number;
  disabled: boolean;
  change: <K extends keyof Design>(key: K, value: Design[K]) => void;
}) {
  const [dragging, setDragging] = useState(false);
  const [naturalLogo, setNaturalLogo] = useState({ width: 300, height: 160 });
  const drag = useRef<{
    kind: string;
    x: number;
    y: number;
    offsetX: number;
    offsetY: number;
    size: number;
    left: number;
    top: number;
    rect: DOMRect;
  } | null>(null);
  const frame = frameSize(design);
  const [width, height] = frame;
  const box = logoBox(design, frame, naturalLogo);
  const limit = Math.min(600, width / 2 - 160);
  /** Capture a pointer and the original output coordinates before starting a drag/resize. */
  function begin(e: React.PointerEvent<HTMLElement>, kind: string) {
    if (disabled) return;
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.focus({ preventScroll: true });
    const canvas = e.currentTarget.closest(".canvas")!.getBoundingClientRect();
    const item =
      e.currentTarget
        .closest(".canvas-title,.canvas-logo")
        ?.getBoundingClientRect() ?? e.currentTarget.getBoundingClientRect();
    drag.current = {
      kind,
      x: e.clientX,
      y: e.clientY,
      offsetX: design.title_offset_x ?? 0,
      offsetY: design.title_offset_y ?? 0,
      size:
        kind === "logo-size"
          ? (design.logo_scale ?? 1)
          : (design.title_font_size ?? 64),
      left: (item.left - canvas.left) / canvas.width,
      top: (item.top - canvas.top) / canvas.height,
      rect: canvas,
    };
    e.currentTarget.setPointerCapture(e.pointerId);
    setDragging(true);
  }
  /** Apply the current pointer delta within validated title/logo bounds. */
  function move(e: React.PointerEvent<HTMLElement>) {
    const state = drag.current;
    if (!state || disabled) return;
    e.stopPropagation();
    const [dx, dy] = canvasDelta(
      e.clientX - state.x,
      e.clientY - state.y,
      state.rect,
      frame,
    );
    if (state.kind === "title") {
      change(
        "title_offset_x",
        Math.round(Math.max(-limit, Math.min(limit, state.offsetX + dx))),
      );
      change(
        "title_offset_y",
        Math.round(Math.max(-80, Math.min(400, state.offsetY + dy))),
      );
    } else if (state.kind === "title-size")
      change(
        "title_font_size",
        Math.round(Math.max(28, Math.min(110, state.size + dx / 8))),
      );
    else if (state.kind === "logo-size")
      change(
        "logo_scale",
        Math.max(0.25, Math.min(2.5, state.size + dx / 300)),
      );
    else {
      change("logo_x", Math.max(0, Math.min(0.95, state.left + dx / width)));
      change("logo_y", Math.max(0, Math.min(0.95, state.top + dy / height)));
    }
  }
  /** Release transient drag state and hide alignment guides. */
  function end() {
    drag.current = null;
    setDragging(false);
  }
  /** Move title/logo with arrow keys, using Shift for a larger output-pixel step. */
  function keyboard(
    e: React.KeyboardEvent<HTMLElement>,
    kind: "title" | "logo",
  ) {
    if (
      disabled ||
      !["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)
    )
      return;
    e.preventDefault();
    const amount = e.shiftKey ? 50 : 10;
    const dx =
      e.key === "ArrowLeft" ? -amount : e.key === "ArrowRight" ? amount : 0;
    const dy =
      e.key === "ArrowUp" ? -amount : e.key === "ArrowDown" ? amount : 0;
    if (kind === "title") {
      change(
        "title_offset_x",
        Math.max(-limit, Math.min(limit, (design.title_offset_x ?? 0) + dx)),
      );
      change(
        "title_offset_y",
        Math.max(-80, Math.min(400, (design.title_offset_y ?? 0) + dy)),
      );
    } else {
      const rect = e.currentTarget.getBoundingClientRect();
      const canvas = e.currentTarget
        .closest(".canvas")!
        .getBoundingClientRect();
      change(
        "logo_x",
        Math.max(
          0,
          Math.min(0.95, (rect.left - canvas.left) / canvas.width + dx / width),
        ),
      );
      change(
        "logo_y",
        Math.max(
          0,
          Math.min(0.95, (rect.top - canvas.top) / canvas.height + dy / height),
        ),
      );
    }
  }
  const handlers = {
    onPointerMove: move,
    onPointerUp: end,
    onPointerCancel: end,
  };
  return (
    <>
      <img
        src={artifactUrl(job, "background", false, revision)}
        alt={t("Fondo actual del episodio")}
      />
      {dragging && <div className="alignment-guides" aria-hidden="true" />}
      <div
        className={`canvas-title ${!disabled ? "editable-object" : ""}`}
        tabIndex={disabled ? -1 : 0}
        role="group"
        aria-label={t("Move title with drag or arrow keys")}
        onKeyDown={(e) => keyboard(e, "title")}
        onPointerDown={(e) => begin(e, "title")}
        {...handlers}
        style={{
          fontFamily: fontFamilies[design.title_font ?? "sans"],
          fontSize: `${(design.title_font_size ?? 64) / (width / 100)}cqw`,
          fontWeight: (design.title_bold ?? true) ? 700 : 400,
          top: `${((100 + (design.title_offset_y ?? 0)) / height) * 100}%`,
          left: `${((width / 2 + (design.title_offset_x ?? 0)) / width) * 100}%`,
          right: "auto",
          transform: "translateX(-50%)",
          width: `${(Math.max(80, Math.min(1600, 2 * (width / 2 - Math.abs(design.title_offset_x ?? 0) - 120))) / width) * 100}%`,
          lineHeight: 1.3,
        }}
      >
        {design.title}
        {!disabled && (
          <button
            className="resize-handle"
            aria-label={t("Resize title")}
            onPointerDown={(e) => begin(e, "title-size")}
            {...handlers}
          >
            ↘
          </button>
        )}
      </div>
      {job.artifacts.includes("logo") && (
        <>
          <img
            className={`canvas-logo ${!disabled ? "editable-object" : ""}`}
            src={artifactUrl(job, "logo", false, revision)}
            alt={t("Logo del episodio")}
            draggable={false}
            tabIndex={disabled ? -1 : 0}
            onPointerDown={(e) => begin(e, "logo")}
            onKeyDown={(e) => keyboard(e, "logo")}
            {...handlers}
            onLoad={(e) =>
              setNaturalLogo({
                width: e.currentTarget.naturalWidth,
                height: e.currentTarget.naturalHeight,
              })
            }
            style={{
              position: "absolute",
              width: `${(box.width / width) * 100}%`,
              height: `${(box.height / height) * 100}%`,
              left: `${(box.left / width) * 100}%`,
              top: `${(box.top / height) * 100}%`,
              maxWidth: "none",
              maxHeight: "none",
              right: "auto",
              bottom: "auto",
              transform: "none",
            }}
          />
          {!disabled && (
            <button
              className="resize-handle logo-resize"
              style={{
                left: `${((box.left + box.width) / width) * 100}%`,
                top: `${((box.top + box.height) / height) * 100}%`,
                right: "auto",
                bottom: "auto",
              }}
              aria-label={t("Resize logo")}
              onPointerDown={(e) => begin(e, "logo-size")}
              {...handlers}
            >
              ↘
            </button>
          )}
        </>
      )}
      <div className="safe-area" style={{ top: `${design.wave_y * 100}%` }}>
        {t("Zona del visualizador · se renderiza con tu audio")}
      </div>
      <div
        className="sample-caption"
        style={{
          fontFamily: fontFamilies[design.subtitle_font ?? "sans"],
          fontSize: `${design.font_size / (width / 100)}cqw`,
          bottom: `${(design.subtitle_margin / height) * 100}%`,
        }}
      >
        {t("Vista de composición aproximada")}
      </div>
    </>
  );
}
