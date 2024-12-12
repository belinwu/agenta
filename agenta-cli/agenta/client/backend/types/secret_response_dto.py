# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .header_dto import HeaderDto
from .secret_dto import SecretDto
from .lifecycle_dto import LifecycleDto
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class SecretResponseDto(UniversalBaseModel):
    header: typing.Optional[HeaderDto] = None
    secret: SecretDto
    id: str
    lifecycle: typing.Optional[LifecycleDto] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True
        )  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
