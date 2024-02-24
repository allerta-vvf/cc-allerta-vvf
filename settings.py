from pydantic import BaseModel, Field
from enum import Enum
from datetime import date, time
from cat.mad_hatter.decorators import plugin


# settings
class AllertaVVFSettings(BaseModel):
    login_token: str = Field(
        default="",
        title="Login Token",
        description="Your login token for the Allerta VVF API",
    )
    api_url: str = Field(
        default="http://localhost/api/",
        title="API URL",
        description="The base URL for the Allerta VVF API, with a trailing slash",
    )


# Give your settings model to the Cat.
@plugin
def settings_model():
    return AllertaVVFSettings

def get_setting(cat, name=None):
    settings = cat.mad_hatter.plugins['allerta_vvf'].load_settings()

    if name is not None:
        return settings[name] if name in settings else None

    return settings
