# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .reference_dto import ReferenceDto
from .lifecycle_dto import LifecycleDto
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ConfigResponseModel(UniversalBaseModel):
    params: typing.Dict[str, typing.Optional[typing.Any]]
    url: typing.Optional[str] = None
    application_ref: typing.Optional[ReferenceDto] = None
    service_ref: typing.Optional[ReferenceDto] = None
    variant_ref: typing.Optional[ReferenceDto] = None
    environment_ref: typing.Optional[ReferenceDto] = None
    application_lifecycle: typing.Optional[LifecycleDto] = None
    service_lifecycle: typing.Optional[LifecycleDto] = None
    variant_lifecycle: typing.Optional[LifecycleDto] = None
    environment_lifecycle: typing.Optional[LifecycleDto] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
            extra="allow", frozen=True
        )  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
