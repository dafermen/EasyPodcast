export function DesignActions({
  dirty,
  disabled,
  saved,
  onSave,
  onContinue,
  disabledMessage,
}: {
  dirty: boolean;
  disabled: boolean;
  saved: boolean;
  onSave: () => void;
  onContinue: () => void;
  disabledMessage?: string;
}) {
  return (
    <div className="design-actions">
      <button disabled={disabled || !dirty} onClick={onSave}>
        {saved && !dirty ? "✓ Diseño guardado" : "Guardar diseño"}
      </button>
      <p role="status" className={saved && !dirty ? "saved-feedback" : "note"}>
        {disabled
          ? (disabledMessage ?? "Espera a que termine la operación activa.")
          : dirty
            ? "Tienes cambios sin guardar. Pulsa Guardar diseño para habilitar el siguiente paso."
            : saved
              ? "Diseño guardado. Revisa el fondo y pulsa Aprobar fondo y continuar."
              : "Revisa el diseño y el fondo. Si están bien, pulsa Aprobar fondo y continuar."}
      </p>
      <button
        className="primary continue-design"
        disabled={disabled || dirty}
        onClick={onContinue}
      >
        Aprobar fondo y continuar →
      </button>
    </div>
  );
}
