from typing import Optional, Any, Dict
from enum import Enum
from uuid import UUID

# from traceback import format_exc

from httpx import get as check

from opentelemetry.trace import (
    get_current_span,
    set_tracer_provider,
    get_tracer_provider,
    Status,
    StatusCode,
)
from opentelemetry.sdk.trace import Span, Tracer, TracerProvider
from opentelemetry.sdk.resources import Resource

from agenta.sdk.utils.singleton import Singleton
from agenta.sdk.utils.exceptions import suppress
from agenta.sdk.utils.logging import log
from agenta.sdk.tracing.processors import TraceProcessor
from agenta.sdk.tracing.exporters import InlineExporter, OTLPExporter
from agenta.sdk.tracing.spans import CustomSpan
from agenta.sdk.tracing.inline import parse_inline_trace
from agenta.sdk.tracing.conventions import Reference, is_valid_attribute_key


class Tracing(metaclass=Singleton):
    VERSION = "0.1.0"

    Status = Status
    StatusCode = StatusCode

    def __init__(
        self,
        url: str,
    ) -> None:
        # ENDPOINT (OTLP)
        self.otlp_url = url
        # AUTHENTICATION (OTLP)
        self.project_id: Optional[str] = None
        # AUTHORIZATION (OTLP)
        self.api_key: Optional[str] = None
        # HEADERS (OTLP)
        self.headers: Dict[str, str] = dict()
        # REFERENCES
        self.references: Dict[str, str] = dict()

        # TRACER PROVIDER
        self.tracer_provider: Optional[TracerProvider] = None
        # TRACER
        self.tracer: Optional[Tracer] = None
        # INLINE SPANS for INLINE TRACES (INLINE PROCESSOR)
        self.inline_spans: Dict[str, Any] = dict()

    # PUBLIC

    def configure(
        self,
        project_id: Optional[str] = None,
        api_key: Optional[str] = None,
        # DEPRECATING
        app_id: Optional[str] = None,
    ):
        # AUTHENTICATION (OTLP)
        self.project_id = project_id  # "f7943e42-ec69-498e-bf58-8db034b9286e"
        self.app_id = app_id
        # AUTHORIZATION (OTLP)
        self.api_key = api_key
        # HEADERS (OTLP)
        self.headers = {}
        if project_id:
            self.headers.update(**{"AG-PROJECT-ID": project_id})
        if app_id:
            self.headers.update(**{"AG-APP-ID": app_id})
        if api_key:
            self.headers.update(**{"Authorization": self.api_key})

        # REFERENCES
        self.references["application.id"] = app_id

        # TRACER PROVIDER
        self.tracer_provider = TracerProvider(
            resource=Resource(attributes={"service.name": "agenta-sdk"})
        )
        # TRACE PROCESSORS -- INLINE
        self.inline = TraceProcessor(
            InlineExporter(
                registry=self.inline_spans,
            ),
            references=self.references,
        )
        self.tracer_provider.add_span_processor(self.inline)
        # TRACE PROCESSORS -- OTLP
        try:
            log.info("--------------------------------------------")
            log.info(f"Agenta SDK - connecting to otlp receiver at: {self.otlp_url}")
            log.info("--------------------------------------------")

            check(
                self.otlp_url,
                headers=self.headers,
                timeout=1,
            )

            _otlp = TraceProcessor(
                OTLPExporter(
                    endpoint=self.otlp_url,
                    headers=self.headers,
                ),
                references=self.references,
            )

            self.tracer_provider.add_span_processor(_otlp)

            log.info(f"Success: traces will be exported.")
            log.info("--------------------------------------------")

        except:
            # log.warning(format_exc().strip("\n"))
            # log.warning("--------------------------------------------")
            log.warning(f"Failure: traces will not be exported.")
            log.warning("--------------------------------------------")

        # GLOBAL TRACER PROVIDER -- INSTRUMENTATION LIBRARIES
        set_tracer_provider(self.tracer_provider)
        # TRACER
        self.tracer: Tracer = self.tracer_provider.get_tracer("agenta.tracer")

    def get_current_span(self):
        _span = None

        with suppress():
            _span = get_current_span()

            if _span.is_recording():
                return CustomSpan(_span)

        return _span

    def store_internals(
        self,
        attributes: Dict[str, Any],
        span: Optional[Span] = None,
    ):
        with suppress():
            if span is None:
                span = self.get_current_span()

            span.set_attributes(
                attributes={"internals": attributes},
                namespace="data",
            )

    def store_refs(
        self,
        refs: Dict[str, str],
        span: Optional[Span] = None,
    ):
        with suppress():
            if span is None:
                span = self.get_current_span()

            for key in refs.keys():
                if key in Reference:
                    # TYPE AND FORMAT CHECKING
                    if key.endswith(".id"):
                        try:
                            refs[key] = UUID(refs[key]).hex
                        except:
                            refs[key] = None

                    refs[key] = str(refs[key])

                    # ADD REFERENCE TO THIS SPAN
                    span.set_attribute(
                        key.value if isinstance(key, Enum) else key,
                        refs[key],
                        namespace="refs",
                    )

                    # AND TO ALL SPANS CREATED AFTER THIS ONE
                    self.references[key] = refs[key]
                    # TODO: THIS SHOULD BE REPLACED BY A TRACE CONTEXT !!!

    def store_meta(
        self,
        meta: Dict[str, Any],
        span: Optional[Span] = None,
    ):
        with suppress():
            if span is None:
                span = self.get_current_span()

            for key in meta.keys():
                if is_valid_attribute_key(key):
                    span.set_attribute(
                        key,
                        meta[key],
                        namespace="meta",
                    )

    def store_metrics(
        self,
        metrics: Dict[str, Any],
        span: Optional[Span] = None,
    ):
        with suppress():
            if span is None:
                span = self.get_current_span()

            for key in metrics.keys():
                if is_valid_attribute_key(key):
                    span.set_attribute(
                        key,
                        metrics[key],
                        namespace="metrics",
                    )

    def is_inline_trace_ready(
        self,
        trace_id: Optional[int] = None,
    ) -> bool:
        is_ready = True

        with suppress():
            if trace_id is not None:
                is_ready = self.inline.is_ready(trace_id)

        return is_ready

    def get_inline_trace(
        self,
        trace_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        _inline_trace = {}

        with suppress():
            is_ready = self.inline.is_ready(trace_id)

            if is_ready is True:
                otel_spans = self.inline.fetch(trace_id)

                if otel_spans:
                    _inline_trace = parse_inline_trace(
                        self.project_id or self.app_id, otel_spans
                    )

        return _inline_trace


def get_tracer(tracing: Tracing) -> Tracer:
    if tracing is None or tracing.tracer is None or tracing.tracer_provider is None:
        return get_tracer_provider().get_tracer("default.tracer")

    return tracing.tracer
