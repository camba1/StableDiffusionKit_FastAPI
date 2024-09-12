# Local Image Generation API for MacOS

This FastAPI Python project enables local image generation using Stable Diffusion/Flux on an M-based Mac.
It leverages Diffusion Kit to utilize onboard GPUs.

### Image Quality Settings:

Default image quality settings:

- **Low**: Uses Sd3-medium model, 256x256 resolution, 30 inference steps.
- **Medium**: Uses Sd3-medium model, 512x512 resolution, 50 inference steps.
- **High**: Uses Flux-schnell model, 1024x1024 resolution, 4 inference steps.
- **Extreme**: Uses Flux-Schnell model, 1280x1280 resolution, 6 inference steps.

**Note:** The Flux model requires 26 GB of RAM. Ensure adequate RAM before using high or extreme settings.

The image quality settings can be adjusted in the `config.ini` file.

### Running the API

This project uses Poetry for dependency management.

1. Create a new virtual environment.
2. Install dependencies with `poetry install`.
3. Run the server with `make runDev`.
4. Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view and test the API.

Alternatively, you can use `curl` to access the API:

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/image' \
  -H 'accept: application/json' \
  -H 'x-token: secret-token' \
  -H 'Content-Type: application/json' \
  --output 'image.png' \
  -d '{
  "prompt": "a photograph of an astronaut walking on the moon",
  "image_quality": "medium"
}'
```

Image generation times:
- Low quality: ~30-40 seconds
- Extreme quality: ~3 minutes

The generation times were obtained by running the API in a Mac M3 Pro with 32 GB of RAM. 

### Environment Variables

- `LOCAL_IMAGE_GEN_API_KEY`: The API key for the local image generation API. Set this to any value and use the same value for the `x-token` parameter when calling the API.

By default, running the application with `make runDev` sets the API key to `secret-token`.

