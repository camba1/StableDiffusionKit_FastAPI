from enum import Enum
from os import getenv, getcwd, path
import configparser
from pydantic import BaseModel, SecretStr, ConfigDict, Field
from pydantic_settings import BaseSettings


class ImageQualityEnum(str, Enum):
    """
    Enum for image quality settings.
    """
    low = "low"
    medium = "medium"
    high = "high"
    extreme = "extreme"


class ModelTypeEnum(str, Enum):
    """
    Enum for model type settings.
    """
    sd3 = "sd3"
    flux = "flux"


class RequestConfig(BaseModel):
    """
    Configuration class for the request body when generating an image.
    """
    prompt: str = Field(title="Prompt", description="Prompt used to generate the image",
                        examples=["a photograph of an astronaut riding a horse"])
    image_quality: ImageQualityEnum = Field(title="Image quality",
                                            default=ImageQualityEnum.low,
                                            description="Dictates image size and the model used to generate the image",
                                            examples=["low", "medium"])
    seed: int = Field(title="Image quality",
                      default=None,
                      description="Seed used to generate the image",
                      examples=["23456789"])


class BaseConfig(BaseModel):
    """
    Base configuration class that stores the basic settings for models.
    """
    model_config = ConfigDict(protected_namespaces=())
    model_name: str
    model_type: ModelTypeEnum
    height: int
    width: int
    num_steps: int
    cfg_weight: float


class AppConfig(BaseSettings):
    """
    Application configuration class that aggregates different model configurations.
    """
    model_config = ConfigDict(protected_namespaces=())
    api_key: SecretStr
    model_verbose_output: bool
    low_res_model: BaseConfig
    med_res_model: BaseConfig
    high_res_model: BaseConfig
    extreme_res_model: BaseConfig


def setup_base_config(config: configparser.ConfigParser, config_section: str):
    """
    Sets up a base model configuration by reading from a ConfigParser object.

    Args:
        config (configparser.ConfigParser): The ConfigParser object holding the configuration data.
        config_section (str): The section of the configuration file to read.

    Returns:
        BaseConfig: The base model configuration.
    """

    base = BaseConfig(
        model_name=config.get(config_section, 'model_name'),
        model_type=config.get(config_section, 'model_type'),
        height=config.get(config_section, 'height'),
        width=config.getfloat(config_section, 'width'),
        num_steps=config.get(config_section, 'num_steps'),
        cfg_weight=config.get(config_section, 'cfgWeight')
    )
    return base


def read_config(filename: str = 'config.ini') -> AppConfig:
    """
    Reads the application configuration from a specified file.

    Args:
        filename (str): The name of the configuration file. Defaults to 'config.ini'.

    Returns:
        AppConfig: The overall application configuration.

    Raises:
        RuntimeError: If the configuration file cannot be read or processed.
    """
    try:
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the configuration file
        config_filename = path.join(getcwd(), "app", filename)
        config.read(config_filename)

        model_provider_api_key_name = config.get("common", 'model_provider_api_key_name')
        model_verbose_output = config.getboolean("common", 'model_verbose_output')

        # Set up the base model configuration
        low_res_model = setup_base_config(config, "lowResModel")
        med_res_model = setup_base_config(config, "medResModel")
        high_res_model = setup_base_config(config, "highResModel")
        extreme_res_model = setup_base_config(config, "extremeResModel")

        # Create the overall application configuration
        return AppConfig(
            api_key=getenv(model_provider_api_key_name),
            model_verbose_output=model_verbose_output,
            low_res_model=low_res_model,
            med_res_model=med_res_model,
            high_res_model=high_res_model,
            extreme_res_model=extreme_res_model
        )

    except Exception as e:
        raise RuntimeError("Failed to read configuration: " + str(e))

# Example usage
# config = read_config()
# print(config)
