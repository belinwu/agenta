# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .. import core
from ..core.request_options import RequestOptions
from ..types.test_set_simple_response import TestSetSimpleResponse
from ..core.pydantic_utilities import parse_obj_as
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.test_set_output_response import TestSetOutputResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TestsetsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def upload_file(
        self,
        *,
        file: core.File,
        upload_type: typing.Optional[str] = OMIT,
        testset_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Uploads a CSV or JSON file and saves its data to MongoDB.

        Args:
        upload_type : Either a json or csv file.
            file (UploadFile): The CSV or JSON file to upload.
            testset_name (Optional): the name of the testset if provided.

        Returns:
            dict: The result of the upload process.

        Parameters
        ----------
        file : core.File
            See core.File for more documentation

        upload_type : typing.Optional[str]

        testset_name : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.upload_file()
        """
        _response = self._client_wrapper.httpx_client.request(
            "testsets/upload",
            method="POST",
            data={
                "upload_type": upload_type,
                "testset_name": testset_name,
            },
            files={
                "file": file,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def import_testset(
        self,
        *,
        endpoint: typing.Optional[str] = OMIT,
        testset_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Import JSON testset data from an endpoint and save it to MongoDB.

        Args:
            endpoint (str): An endpoint URL to import data from.
            testset_name (str): the name of the testset if provided.

        Returns:
            dict: The result of the import process.

        Parameters
        ----------
        endpoint : typing.Optional[str]

        testset_name : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.import_testset()
        """
        _response = self._client_wrapper.httpx_client.request(
            "testsets/endpoint",
            method="POST",
            json={
                "endpoint": endpoint,
                "testset_name": testset_name,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_testsets(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[TestSetOutputResponse]:
        """
        Get all testsets.

        Returns:

        - A list of testset objects.

        Raises:

        - `HTTPException` with status code 404 if no testsets are found.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[TestSetOutputResponse]
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.get_testsets()
        """
        _response = self._client_wrapper.httpx_client.request(
            "testsets",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[TestSetOutputResponse],
                    parse_obj_as(
                        type_=typing.List[TestSetOutputResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_testset(
        self,
        *,
        name: str,
        csvdata: typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Create a testset with given name, save the testset to MongoDB.

        Args:
        name (str): name of the test set.
        testset (Dict[str, str]): test set data.

        Returns:
        str: The id of the test set created.

        Parameters
        ----------
        name : str

        csvdata : typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.create_testset(
            name="name",
            csvdata=[{"key": "value"}],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "testsets",
            method="POST",
            json={
                "name": name,
                "csvdata": csvdata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_testsets(
        self,
        *,
        testset_ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[str]:
        """
        Delete specific testsets based on their unique IDs.

        Args:
        testset_ids (List[str]): The unique identifiers of the testsets to delete.

        Returns:
        A list of the deleted testsets' IDs.

        Parameters
        ----------
        testset_ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[str]
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.delete_testsets(
            testset_ids=["testset_ids"],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "testsets",
            method="DELETE",
            json={
                "testset_ids": testset_ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[str],
                    parse_obj_as(
                        type_=typing.List[str],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def deprecating_create_testset(
        self,
        app_id: str,
        *,
        name: str,
        csvdata: typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Create a testset with given name, save the testset to MongoDB.

        Args:
        name (str): name of the test set.
        testset (Dict[str, str]): test set data.

        Returns:
        str: The id of the test set created.

        Parameters
        ----------
        app_id : str

        name : str

        csvdata : typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.deprecating_create_testset(
            app_id="app_id",
            name="name",
            csvdata=[{"key": "value"}],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"testsets/{jsonable_encoder(app_id)}",
            method="POST",
            json={
                "name": name,
                "csvdata": csvdata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_single_testset(
        self,
        testset_id: str,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[typing.Any]:
        """
        Fetch a specific testset in a MongoDB collection using its _id.

        Args:
            testset_id (str): The _id of the testset to fetch.

        Returns:
            The requested testset if found, else an HTTPException.

        Parameters
        ----------
        testset_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.get_single_testset(
            testset_id="testset_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"testsets/{jsonable_encoder(testset_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    parse_obj_as(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_testset(
        self,
        testset_id: str,
        *,
        name: str,
        csvdata: typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[typing.Any]:
        """
        Update a testset with given id, update the testset in MongoDB.

        Args:
        testset_id (str): id of the test set to be updated.
        csvdata (NewTestset): New data to replace the old testset.

        Returns:
        str: The id of the test set updated.

        Parameters
        ----------
        testset_id : str

        name : str

        csvdata : typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.testsets.update_testset(
            testset_id="testset_id",
            name="name",
            csvdata=[{"key": "value"}],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"testsets/{jsonable_encoder(testset_id)}",
            method="PUT",
            json={
                "name": name,
                "csvdata": csvdata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    parse_obj_as(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncTestsetsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def upload_file(
        self,
        *,
        file: core.File,
        upload_type: typing.Optional[str] = OMIT,
        testset_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Uploads a CSV or JSON file and saves its data to MongoDB.

        Args:
        upload_type : Either a json or csv file.
            file (UploadFile): The CSV or JSON file to upload.
            testset_name (Optional): the name of the testset if provided.

        Returns:
            dict: The result of the upload process.

        Parameters
        ----------
        file : core.File
            See core.File for more documentation

        upload_type : typing.Optional[str]

        testset_name : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.upload_file()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "testsets/upload",
            method="POST",
            data={
                "upload_type": upload_type,
                "testset_name": testset_name,
            },
            files={
                "file": file,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def import_testset(
        self,
        *,
        endpoint: typing.Optional[str] = OMIT,
        testset_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Import JSON testset data from an endpoint and save it to MongoDB.

        Args:
            endpoint (str): An endpoint URL to import data from.
            testset_name (str): the name of the testset if provided.

        Returns:
            dict: The result of the import process.

        Parameters
        ----------
        endpoint : typing.Optional[str]

        testset_name : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.import_testset()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "testsets/endpoint",
            method="POST",
            json={
                "endpoint": endpoint,
                "testset_name": testset_name,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_testsets(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[TestSetOutputResponse]:
        """
        Get all testsets.

        Returns:

        - A list of testset objects.

        Raises:

        - `HTTPException` with status code 404 if no testsets are found.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[TestSetOutputResponse]
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.get_testsets()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "testsets",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[TestSetOutputResponse],
                    parse_obj_as(
                        type_=typing.List[TestSetOutputResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_testset(
        self,
        *,
        name: str,
        csvdata: typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Create a testset with given name, save the testset to MongoDB.

        Args:
        name (str): name of the test set.
        testset (Dict[str, str]): test set data.

        Returns:
        str: The id of the test set created.

        Parameters
        ----------
        name : str

        csvdata : typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.create_testset(
                name="name",
                csvdata=[{"key": "value"}],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "testsets",
            method="POST",
            json={
                "name": name,
                "csvdata": csvdata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_testsets(
        self,
        *,
        testset_ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[str]:
        """
        Delete specific testsets based on their unique IDs.

        Args:
        testset_ids (List[str]): The unique identifiers of the testsets to delete.

        Returns:
        A list of the deleted testsets' IDs.

        Parameters
        ----------
        testset_ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[str]
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.delete_testsets(
                testset_ids=["testset_ids"],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "testsets",
            method="DELETE",
            json={
                "testset_ids": testset_ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[str],
                    parse_obj_as(
                        type_=typing.List[str],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def deprecating_create_testset(
        self,
        app_id: str,
        *,
        name: str,
        csvdata: typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSetSimpleResponse:
        """
        Create a testset with given name, save the testset to MongoDB.

        Args:
        name (str): name of the test set.
        testset (Dict[str, str]): test set data.

        Returns:
        str: The id of the test set created.

        Parameters
        ----------
        app_id : str

        name : str

        csvdata : typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSetSimpleResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.deprecating_create_testset(
                app_id="app_id",
                name="name",
                csvdata=[{"key": "value"}],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"testsets/{jsonable_encoder(app_id)}",
            method="POST",
            json={
                "name": name,
                "csvdata": csvdata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSetSimpleResponse,
                    parse_obj_as(
                        type_=TestSetSimpleResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_single_testset(
        self,
        testset_id: str,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[typing.Any]:
        """
        Fetch a specific testset in a MongoDB collection using its _id.

        Args:
            testset_id (str): The _id of the testset to fetch.

        Returns:
            The requested testset if found, else an HTTPException.

        Parameters
        ----------
        testset_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.get_single_testset(
                testset_id="testset_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"testsets/{jsonable_encoder(testset_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    parse_obj_as(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_testset(
        self,
        testset_id: str,
        *,
        name: str,
        csvdata: typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[typing.Any]:
        """
        Update a testset with given id, update the testset in MongoDB.

        Args:
        testset_id (str): id of the test set to be updated.
        csvdata (NewTestset): New data to replace the old testset.

        Returns:
        str: The id of the test set updated.

        Parameters
        ----------
        testset_id : str

        name : str

        csvdata : typing.Sequence[typing.Dict[str, typing.Optional[typing.Any]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[typing.Any]
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.testsets.update_testset(
                testset_id="testset_id",
                name="name",
                csvdata=[{"key": "value"}],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"testsets/{jsonable_encoder(testset_id)}",
            method="PUT",
            json={
                "name": name,
                "csvdata": csvdata,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.Optional[typing.Any],
                    parse_obj_as(
                        type_=typing.Optional[typing.Any],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
