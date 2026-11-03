# Optional image provider

The existing integration is backend/app/images.py. ImageProvider defines generate_background(design, destination); OpenAIProvider uses the Python SDK client.images.generate with model, prompt, n=1, size and quality, requiring data[0].b64_json. It uses a 180-second timeout and max_retries=0. Tests inject a fake provider and never incur charges.

Configure OPENAI_API_KEY and an accessible IMAGE_MODEL in the backend .env only. Defaults IMAGE_SIZE=1536x1024 and IMAGE_QUALITY=medium describe the existing integration; check your selected model's current API compatibility before paying for generation. No model is chosen automatically. No request is sent at startup.

An explicit Generate AI image action sends visual title/context, description, style and atmosphere. Source audio, SRT and logo are not sent. Images are decoded, bounded by configured limits and normalized to the output canvas. The previous background is retained on failure. Approval remains explicit.

Network/authentication/quota errors are sanitized and not automatically retried. A timed-out or cancelled request may already have been billed; local cancellation cannot undo provider charges. Never expose keys in React, logs, screenshots or Git. The paid integration has not been verified with a real billed generation in this project; fake-provider tests do not establish account access or output quality.
