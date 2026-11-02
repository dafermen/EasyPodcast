# Privacidad y archivos

Audio, SRT, imágenes, logo y renders se guardan temporalmente en el equipo donde corre backend. No todo se procesa en el navegador: FFmpeg lee/escribe disco. TEMP_ROOT por defecto es `easypodcast` bajo el temporal del sistema, fuera del repositorio. Cada trabajo tiene UUID y nombres internos; no se usan rutas del cliente.

Solo una descripción visual construida desde título, descripción, estilo y ambiente llega a OpenAI al pulsar generación. Audio y SRT no se envían. La retención del proveedor depende de sus políticas y cuenta; esta aplicación no garantiza retención cero ni cancelación de costes tras enviar una petición.

No hay base de datos, localStorage, historial ni preferencias persistentes. Token de API permanece en memoria React; cookie HttpOnly/SameSite Strict permite solo medios del trabajo. Al recargar la página no se recupera el token. JSON exportado contiene únicamente Design.

TTL: 60 minutos después de operaciones completadas; 15 tras fallo/cancelación; máximo activo cuatro horas. Limpieza cada dos segundos. Descargas activas impiden borrado y mutaciones. Cancelar conserva entradas para reintento; Eliminar marca borrado y cancela; apagado ordenado limpia. En arranque se eliminan UUID residuales solo dentro de raíz marcada y bloqueada. No se siguen symlinks.

Un crash o apagado abrupto puede dejar medios hasta el siguiente arranque. El borrado normal no es borrado forense ni garantiza eliminación de copias del OS/backups. El usuario controla los archivos descargados fuera del temporal. CLI conserva explícitamente su salida elegida. No ejecutar backend en red pública.

No se registran claves, audio, SRT, prompts completos o imágenes. Scripts de inicio desactivan access logs. Errores al cliente no incluyen stderr ni rutas internas. Los temporales requieren permisos apropiados de la cuenta del OS; no hay aislamiento frente a otros procesos de la misma cuenta.
