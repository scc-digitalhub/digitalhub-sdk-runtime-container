# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

import requests
from digitalhub.utils.exceptions import EntityError

from digitalhub_runtime_container.entities.run._base.entity import RunContainerRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_container.entities.run.serve.spec import RunSpecContainerRunServe
    from digitalhub_runtime_container.entities.run.serve.status import RunStatusContainerRunServe


class RunContainerRunServe(RunContainerRun):
    """
    RunContainerRunServe class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecContainerRunServe,
        status: RunStatusContainerRunServe,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecContainerRunServe
        self.status: RunStatusContainerRunServe

    def invoke(
        self,
        method: str = "POST",
        url: str | None = None,
        **kwargs,
    ) -> requests.Response:
        """
        Invoke run service endpoint. It uses the service URL from the run
        status if no URL is specified.
        The method defaults to "POST" if data or json is provided in kwargs,
        otherwise it defaults to "GET". The function returns a requests.Response
        object.

        Parameters
        ----------
        method : str
            Method of the request (e.g., "GET", "POST").
        url : str
            URL to invoke. If specified, it must start with the service URL
            (http:// or https:// prefixes are required and stripped before comparison).
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from service.
        """
        try:
            base_url: str = self.status.service.get("url")
        except AttributeError:
            raise EntityError(
                "Url not specified and service not found on run status."
                " If a service is deploying, use run.wait() or try again later."
            )

        if url is not None and not url.removeprefix("http://").removeprefix("https://").startswith(base_url):
            raise EntityError(f"Invalid URL: {url}. It must start with the service URL: {base_url}")

        if url is None:
            url = f"http://{base_url}"

        if "data" not in kwargs and "json" not in kwargs:
            method = "GET"

        return requests.request(method=method, url=url, **kwargs)
