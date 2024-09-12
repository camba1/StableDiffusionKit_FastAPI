from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Header, Depends
from app.routes.image import generate_image
from app.config import read_config, ImageQualityEnum, RequestConfig


config = read_config()


def verify_token(x_token: Annotated[str, Header()]) -> None:
    """Verify the token is valid."""

    if x_token != config.api_key.get_secret_value():
        err_detail = "X-Token header invalid"
        raise HTTPException(status_code=401, detail=err_detail)


app = FastAPI(dependencies=[Depends(verify_token)])


# @app.post("/image")
# async def generate_image_endpoint(prompt: str,
#                                   image_quality: ImageQualityEnum = ImageQualityEnum.low, seed: int = None):
#     return await generate_image(config, prompt, image_quality, seed)

@app.post("/image")
async def generate_image_endpoint(image_request: RequestConfig):
    return await generate_image(config, image_request.prompt, image_request.image_quality,image_request.seed)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
