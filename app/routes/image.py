import gc
from io import BytesIO
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from diffusionkit.mlx import FluxPipeline, DiffusionPipeline
from app.config import ImageQualityEnum, ModelTypeEnum, AppConfig
from mlx.core.metal import clear_cache

IMAGE_FORMAT = "png"
MEDIA_TYPE = f"image/{IMAGE_FORMAT}"


def get_generation_values(config: AppConfig, image_quality: ImageQualityEnum = ImageQualityEnum.low):
    """
    Get the generation values based on the image quality. These include the model type, model name, height, width,
    The values are passed to the pipeline to generate the image.
    """
    match image_quality:
        case ImageQualityEnum.low:
            return config.low_res_model
        case ImageQualityEnum.medium:
            return config.med_res_model
        case ImageQualityEnum.high:
            return config.high_res_model
        case ImageQualityEnum.extreme:
            return config.extreme_res_model
        case _:
            raise HTTPException(status_code=400, detail="Invalid image quality")


def get_pipeline(model_type: ModelTypeEnum, model_name: str):
    """
    Get the pipeline used to generate the image based on the model type.
    """
    match model_type:
        case ModelTypeEnum.sd3:
            pipeline = DiffusionPipeline(
                shift=3.0,
                use_t5=False,
                model_version=model_name,
                low_memory_mode=True,
                a16=True,
                w16=True,
            )
            return pipeline
        case ModelTypeEnum.flux:
            pipeline = FluxPipeline(
                shift=1.0,
                model_version=model_name,
                low_memory_mode=True,
                a16=True,
                w16=True,
            )
            return pipeline
        case _:
            raise HTTPException(status_code=400, detail="Invalid model type")


async def generate_image(config: AppConfig, prompt: str,
                         image_quality: ImageQualityEnum = ImageQualityEnum.low, seed: int = None):
    """
    Generate an image based on the prompt, image quality and seed provided by the end user of the API.
    The image quality dictates which model is used to generate the image as well as the size of the image.
    """
    try:
        gen_values = get_generation_values(config, image_quality)
        pipeline = get_pipeline(gen_values.model_type, gen_values.model_name)
        image, _ = pipeline.generate_image(
            prompt,
            cfg_weight=gen_values.cfg_weight,
            num_steps=gen_values.num_steps,
            latent_size=(gen_values.height // 8, gen_values.width // 8),
            seed=seed,
            verbose=config.model_verbose_output
        )

        # Convert the image to a byte stream
        image_byte_stream = BytesIO()
        image.save(image_byte_stream, format=IMAGE_FORMAT)
        image_byte_stream.seek(0)

        # Clean up memory
        clear_cache()
        gc.collect()

        return StreamingResponse(image_byte_stream, media_type=MEDIA_TYPE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
