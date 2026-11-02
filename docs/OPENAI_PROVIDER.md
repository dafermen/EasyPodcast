# Proveedor de imágenes

Implementación: `backend/app/images.py`, SDK oficial Python `OpenAI.images.generate`, cliente con timeout de 180 segundos y `max_retries=0`. La interfaz ImageProvider permite pruebas falsas sin red. Solo petición explícita del usuario llama al proveedor.

Contrato consultado el 2 de noviembre de 2026: [referencia oficial Python](https://developers.openai.com/api/reference/python/resources/images/methods/generate). La integración envía model, prompt, n=1, size y quality; necesita respuesta `data[0].b64_json`. Está orientada a modelos GPT Image, no a respuestas URL de proveedores antiguos. La referencia admite el tamaño horizontal 1536×1024 para GPT Image. Se adapta a 1920×1080 con márgenes, sin estirar ni recortar caras.

Configura OPENAI_API_KEY y un IMAGE_MODEL GPT Image disponible en tu cuenta en `.env`. Se deja modelo vacío para no suponer acceso o escoger automáticamente una opción con costes. IMAGE_SIZE=1536x1024 e IMAGE_QUALITY=medium son parámetros de contrato, **no una llamada real verificada**. Revisa compatibilidad del modelo elegido en la referencia. Reinicia backend.

No se ejecutaron generaciones pagadas. La prueba del proveedor falso no demuestra autenticación, cuota o calidad reales. La cancelación puede descartar el resultado local, pero no revierte una petición cobrada. Errores de red/cuota/autenticación se traducen sin revelar datos. Nunca reintentar automáticamente; la petición puede haber llegado al servicio.
