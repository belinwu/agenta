# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.remove_none_from_dict import remove_none_from_dict
from ...errors.unprocessable_entity_error import UnprocessableEntityError
from ...types.feedback import Feedback
from ...types.http_validation_error import HttpValidationError
from ...types.observability_dashboard_data import ObservabilityDashboardData
from ...types.span import Span
from ...types.span_detail import SpanDetail

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ObservabilityClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def dashboard(self) -> ObservabilityDashboardData:
        """
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.dashboard()
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/dashboard"
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(ObservabilityDashboardData, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_trace(
        self,
        *,
        app_id: typing.Optional[str] = OMIT,
        variant_id: typing.Optional[str] = OMIT,
        cost: typing.Optional[float] = OMIT,
        latency: float,
        status: typing.Optional[str] = OMIT,
        token_consumption: typing.Optional[int] = OMIT,
        tags: typing.Optional[typing.List[str]] = OMIT,
        start_time: typing.Optional[dt.datetime] = OMIT,
        end_time: typing.Optional[dt.datetime] = OMIT,
        spans: typing.List[str],
    ) -> str:
        """
        Parameters:
            - app_id: typing.Optional[str].

            - variant_id: typing.Optional[str].

            - cost: typing.Optional[float].

            - latency: float.

            - status: typing.Optional[str].

            - token_consumption: typing.Optional[int].

            - tags: typing.Optional[typing.List[str]].

            - start_time: typing.Optional[dt.datetime].

            - end_time: typing.Optional[dt.datetime].

            - spans: typing.List[str].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.create_trace(
            latency=1.1,
            spans=["spans"],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"latency": latency, "spans": spans}
        if app_id is not OMIT:
            _request["app_id"] = app_id
        if variant_id is not OMIT:
            _request["variant_id"] = variant_id
        if cost is not OMIT:
            _request["cost"] = cost
        if status is not OMIT:
            _request["status"] = status
        if token_consumption is not OMIT:
            _request["token_consumption"] = token_consumption
        if tags is not OMIT:
            _request["tags"] = tags
        if start_time is not OMIT:
            _request["start_time"] = start_time
        if end_time is not OMIT:
            _request["end_time"] = end_time
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/trace"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(str, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_spans_of_generation(
        self, *, type: typing.Optional[str] = None
    ) -> typing.List[Span]:
        """
        Parameters:
            - type: typing.Optional[str].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.get_spans_of_generation()
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/spans"
            ),
            params=remove_none_from_dict({"type": type}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Span], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_span(
        self,
        *,
        parent_span_id: typing.Optional[str] = OMIT,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        event_name: str,
        event_type: typing.Optional[str] = OMIT,
        start_time: typing.Optional[dt.datetime] = OMIT,
        duration: typing.Optional[int] = OMIT,
        status: str,
        inputs: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        outputs: typing.Optional[typing.List[str]] = OMIT,
        prompt_template: typing.Optional[str] = OMIT,
        tokens_input: typing.Optional[int] = OMIT,
        tokens_output: typing.Optional[int] = OMIT,
        token_total: typing.Optional[int] = OMIT,
        cost: typing.Optional[float] = OMIT,
        tags: typing.Optional[typing.List[str]] = OMIT,
    ) -> str:
        """
        Parameters:
            - parent_span_id: typing.Optional[str].

            - meta: typing.Optional[typing.Dict[str, typing.Any]].

            - event_name: str.

            - event_type: typing.Optional[str].

            - start_time: typing.Optional[dt.datetime].

            - duration: typing.Optional[int].

            - status: str.

            - inputs: typing.Optional[typing.Dict[str, typing.Any]].

            - outputs: typing.Optional[typing.List[str]].

            - prompt_template: typing.Optional[str].

            - tokens_input: typing.Optional[int].

            - tokens_output: typing.Optional[int].

            - token_total: typing.Optional[int].

            - cost: typing.Optional[float].

            - tags: typing.Optional[typing.List[str]].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.create_span(
            event_name="event_name",
            status="status",
        )
        """
        _request: typing.Dict[str, typing.Any] = {
            "event_name": event_name,
            "status": status,
        }
        if parent_span_id is not OMIT:
            _request["parent_span_id"] = parent_span_id
        if meta is not OMIT:
            _request["meta"] = meta
        if event_type is not OMIT:
            _request["event_type"] = event_type
        if start_time is not OMIT:
            _request["start_time"] = start_time
        if duration is not OMIT:
            _request["duration"] = duration
        if inputs is not OMIT:
            _request["inputs"] = inputs
        if outputs is not OMIT:
            _request["outputs"] = outputs
        if prompt_template is not OMIT:
            _request["prompt_template"] = prompt_template
        if tokens_input is not OMIT:
            _request["tokens_input"] = tokens_input
        if tokens_output is not OMIT:
            _request["tokens_output"] = tokens_output
        if token_total is not OMIT:
            _request["token_total"] = token_total
        if cost is not OMIT:
            _request["cost"] = cost
        if tags is not OMIT:
            _request["tags"] = tags
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/spans"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(str, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_span_of_generation(
        self, span_id: str, *, type: typing.Optional[str] = None
    ) -> SpanDetail:
        """
        Parameters:
            - span_id: str.

            - type: typing.Optional[str].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.get_span_of_generation(
            span_id="span_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/spans/{span_id}",
            ),
            params=remove_none_from_dict({"type": type}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SpanDetail, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_trace_status(self, trace_id: str, *, status: str) -> bool:
        """
        Parameters:
            - trace_id: str.

            - status: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.update_trace_status(
            trace_id="trace_id",
            status="status",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "PUT",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/traces/{trace_id}",
            ),
            json=jsonable_encoder({"status": status}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(bool, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_feedbacks(self, trace_id: str) -> typing.List[Feedback]:
        """
        Parameters:
            - trace_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.get_feedbacks(
            trace_id="trace_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Feedback], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_feedback(
        self,
        trace_id: str,
        *,
        feedback: typing.Optional[str] = OMIT,
        score: typing.Optional[float] = OMIT,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
    ) -> str:
        """
        Parameters:
            - trace_id: str.

            - feedback: typing.Optional[str].

            - score: typing.Optional[float].

            - meta: typing.Optional[typing.Dict[str, typing.Any]].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.create_feedback(
            trace_id="trace_id",
        )
        """
        _request: typing.Dict[str, typing.Any] = {}
        if feedback is not OMIT:
            _request["feedback"] = feedback
        if score is not OMIT:
            _request["score"] = score
        if meta is not OMIT:
            _request["meta"] = meta
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}",
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(str, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_feedback(self, trace_id: str, feedback_id: str) -> Feedback:
        """
        Parameters:
            - trace_id: str.

            - feedback_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.get_feedback(
            trace_id="trace_id",
            feedback_id="feedback_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}/{feedback_id}",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Feedback, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_feedback(
        self,
        trace_id: str,
        feedback_id: str,
        *,
        feedback: str,
        score: typing.Optional[float] = OMIT,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
    ) -> Feedback:
        """
        Parameters:
            - trace_id: str.

            - feedback_id: str.

            - feedback: str.

            - score: typing.Optional[float].

            - meta: typing.Optional[typing.Dict[str, typing.Any]].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability.update_feedback(
            trace_id="trace_id",
            feedback_id="feedback_id",
            feedback="feedback",
        )
        """
        _request: typing.Dict[str, typing.Any] = {"feedback": feedback}
        if score is not OMIT:
            _request["score"] = score
        if meta is not OMIT:
            _request["meta"] = meta
        _response = self._client_wrapper.httpx_client.request(
            "PUT",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}/{feedback_id}",
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Feedback, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncObservabilityClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def dashboard(self) -> ObservabilityDashboardData:
        """
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.dashboard()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/dashboard"
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(ObservabilityDashboardData, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_trace(
        self,
        *,
        app_id: typing.Optional[str] = OMIT,
        variant_id: typing.Optional[str] = OMIT,
        cost: typing.Optional[float] = OMIT,
        latency: float,
        status: typing.Optional[str] = OMIT,
        token_consumption: typing.Optional[int] = OMIT,
        tags: typing.Optional[typing.List[str]] = OMIT,
        start_time: typing.Optional[dt.datetime] = OMIT,
        end_time: typing.Optional[dt.datetime] = OMIT,
        spans: typing.List[str],
    ) -> str:
        """
        Parameters:
            - app_id: typing.Optional[str].

            - variant_id: typing.Optional[str].

            - cost: typing.Optional[float].

            - latency: float.

            - status: typing.Optional[str].

            - token_consumption: typing.Optional[int].

            - tags: typing.Optional[typing.List[str]].

            - start_time: typing.Optional[dt.datetime].

            - end_time: typing.Optional[dt.datetime].

            - spans: typing.List[str].
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.create_trace(
            latency=1.1,
            spans=["spans"],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"latency": latency, "spans": spans}
        if app_id is not OMIT:
            _request["app_id"] = app_id
        if variant_id is not OMIT:
            _request["variant_id"] = variant_id
        if cost is not OMIT:
            _request["cost"] = cost
        if status is not OMIT:
            _request["status"] = status
        if token_consumption is not OMIT:
            _request["token_consumption"] = token_consumption
        if tags is not OMIT:
            _request["tags"] = tags
        if start_time is not OMIT:
            _request["start_time"] = start_time
        if end_time is not OMIT:
            _request["end_time"] = end_time
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/trace"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(str, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_spans_of_generation(
        self, *, type: typing.Optional[str] = None
    ) -> typing.List[Span]:
        """
        Parameters:
            - type: typing.Optional[str].
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.get_spans_of_generation()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/spans"
            ),
            params=remove_none_from_dict({"type": type}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Span], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_span(
        self,
        *,
        parent_span_id: typing.Optional[str] = OMIT,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        event_name: str,
        event_type: typing.Optional[str] = OMIT,
        start_time: typing.Optional[dt.datetime] = OMIT,
        duration: typing.Optional[int] = OMIT,
        status: str,
        inputs: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        outputs: typing.Optional[typing.List[str]] = OMIT,
        prompt_template: typing.Optional[str] = OMIT,
        tokens_input: typing.Optional[int] = OMIT,
        tokens_output: typing.Optional[int] = OMIT,
        token_total: typing.Optional[int] = OMIT,
        cost: typing.Optional[float] = OMIT,
        tags: typing.Optional[typing.List[str]] = OMIT,
    ) -> str:
        """
        Parameters:
            - parent_span_id: typing.Optional[str].

            - meta: typing.Optional[typing.Dict[str, typing.Any]].

            - event_name: str.

            - event_type: typing.Optional[str].

            - start_time: typing.Optional[dt.datetime].

            - duration: typing.Optional[int].

            - status: str.

            - inputs: typing.Optional[typing.Dict[str, typing.Any]].

            - outputs: typing.Optional[typing.List[str]].

            - prompt_template: typing.Optional[str].

            - tokens_input: typing.Optional[int].

            - tokens_output: typing.Optional[int].

            - token_total: typing.Optional[int].

            - cost: typing.Optional[float].

            - tags: typing.Optional[typing.List[str]].
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.create_span(
            event_name="event_name",
            status="status",
        )
        """
        _request: typing.Dict[str, typing.Any] = {
            "event_name": event_name,
            "status": status,
        }
        if parent_span_id is not OMIT:
            _request["parent_span_id"] = parent_span_id
        if meta is not OMIT:
            _request["meta"] = meta
        if event_type is not OMIT:
            _request["event_type"] = event_type
        if start_time is not OMIT:
            _request["start_time"] = start_time
        if duration is not OMIT:
            _request["duration"] = duration
        if inputs is not OMIT:
            _request["inputs"] = inputs
        if outputs is not OMIT:
            _request["outputs"] = outputs
        if prompt_template is not OMIT:
            _request["prompt_template"] = prompt_template
        if tokens_input is not OMIT:
            _request["tokens_input"] = tokens_input
        if tokens_output is not OMIT:
            _request["tokens_output"] = tokens_output
        if token_total is not OMIT:
            _request["token_total"] = token_total
        if cost is not OMIT:
            _request["cost"] = cost
        if tags is not OMIT:
            _request["tags"] = tags
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "observability/spans"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(str, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_span_of_generation(
        self, span_id: str, *, type: typing.Optional[str] = None
    ) -> SpanDetail:
        """
        Parameters:
            - span_id: str.

            - type: typing.Optional[str].
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.get_span_of_generation(
            span_id="span_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/spans/{span_id}",
            ),
            params=remove_none_from_dict({"type": type}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SpanDetail, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_trace_status(self, trace_id: str, *, status: str) -> bool:
        """
        Parameters:
            - trace_id: str.

            - status: str.
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.update_trace_status(
            trace_id="trace_id",
            status="status",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "PUT",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/traces/{trace_id}",
            ),
            json=jsonable_encoder({"status": status}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(bool, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_feedbacks(self, trace_id: str) -> typing.List[Feedback]:
        """
        Parameters:
            - trace_id: str.
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.get_feedbacks(
            trace_id="trace_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Feedback], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_feedback(
        self,
        trace_id: str,
        *,
        feedback: typing.Optional[str] = OMIT,
        score: typing.Optional[float] = OMIT,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
    ) -> str:
        """
        Parameters:
            - trace_id: str.

            - feedback: typing.Optional[str].

            - score: typing.Optional[float].

            - meta: typing.Optional[typing.Dict[str, typing.Any]].
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.create_feedback(
            trace_id="trace_id",
        )
        """
        _request: typing.Dict[str, typing.Any] = {}
        if feedback is not OMIT:
            _request["feedback"] = feedback
        if score is not OMIT:
            _request["score"] = score
        if meta is not OMIT:
            _request["meta"] = meta
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}",
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(str, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_feedback(self, trace_id: str, feedback_id: str) -> Feedback:
        """
        Parameters:
            - trace_id: str.

            - feedback_id: str.
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.get_feedback(
            trace_id="trace_id",
            feedback_id="feedback_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}/{feedback_id}",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Feedback, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_feedback(
        self,
        trace_id: str,
        feedback_id: str,
        *,
        feedback: str,
        score: typing.Optional[float] = OMIT,
        meta: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
    ) -> Feedback:
        """
        Parameters:
            - trace_id: str.

            - feedback_id: str.

            - feedback: str.

            - score: typing.Optional[float].

            - meta: typing.Optional[typing.Dict[str, typing.Any]].
        ---
        from agenta.client import AsyncAybruhmApi

        client = AsyncAybruhmApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.observability.update_feedback(
            trace_id="trace_id",
            feedback_id="feedback_id",
            feedback="feedback",
        )
        """
        _request: typing.Dict[str, typing.Any] = {"feedback": feedback}
        if score is not OMIT:
            _request["score"] = score
        if meta is not OMIT:
            _request["meta"] = meta
        _response = await self._client_wrapper.httpx_client.request(
            "PUT",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"observability/feedbacks/{trace_id}/{feedback_id}",
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Feedback, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
