export function DesignEntry({
  method,
  setMethod,
  disabled,
  imported,
  onImport,
}: {
  method: "manual" | "import";
  setMethod: (method: "manual" | "import") => void;
  disabled: boolean;
  imported: boolean;
  onImport: (file: File) => void;
}) {
  return (
    <fieldset className="design-entry">
      <legend>¿Cómo quieres preparar el diseño?</legend>
      <label className="check">
        <input
          type="radio"
          name="design-method"
          value="manual"
          checked={method === "manual"}
          disabled={disabled}
          onChange={() => setMethod("manual")}
        />
        Configurar manualmente
      </label>
      <label className="check">
        <input
          type="radio"
          name="design-method"
          value="import"
          checked={method === "import"}
          disabled={disabled}
          onChange={() => setMethod("import")}
        />
        Importar un diseño JSON
      </label>
      {method === "import" && (
        <>
          <label>
            Importar diseño JSON
            <input
              type="file"
              accept="application/json,.json"
              disabled={disabled}
              onChange={(e) => {
                const file = e.currentTarget.files?.[0];
                e.currentTarget.value = "";
                if (file) onImport(file);
              }}
            />
          </label>
          <p className="note">
            Carga el JSON descargado antes desde EasyPodcast. Incluye ajustes,
            no audio, subtítulos, fondo ni logo. Después podrás revisar y
            modificar lo importado.
          </p>
          {imported && (
            <p role="status">
              ✓ Diseño importado. Revisa sus ajustes y el fondo antes de
              continuar.
            </p>
          )}
          {!imported && (
            <p className="note">
              Elige un JSON para continuar o vuelve a configurar manualmente sin
              perder tus ajustes actuales.
            </p>
          )}
        </>
      )}
    </fieldset>
  );
}
