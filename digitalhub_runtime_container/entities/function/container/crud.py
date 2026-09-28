# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.function.crud import new_function

from digitalhub_runtime_container.entities.function.container.builder import FunctionContainerBuilder

if typing.TYPE_CHECKING:
    from digitalhub.entities.task._base.models import CorePullPolicy

    from digitalhub_runtime_container.entities.function.container.entity import FunctionContainer


def new_function_container(
    project: str,
    name: str,
    image: str | None = None,
    base_image: str | None = None,
    image_pull_policy: CorePullPolicy | None = None,
    command: str | None = None,
    code: str | None = None,
    code_src: str | None = None,
    handler: str | None = None,
    lang: str | None = None,
    uuid: str | None = None,
    version: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = False,
) -> FunctionContainer:
    """
    Create a container-backed function entity.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Function name.
    image : str, optional
        Name of the function's container image.
    base_image : str, optional
        Base container image used to build the function image.
    image_pull_policy : CorePullPolicy, optional
        Policy used when pulling the function container image.
    command : str, optional
        Command to run inside the container.
    code : str, optional
        Function source code as plain text.
    code_src : str, optional
        Local path or URI pointing to the function source code.
    handler : str, optional
        Function entrypoint.
    lang : str, optional
        Source code language hint.
    uuid : str, optional
        Function identifier.
    version : str, optional
        Function version.
    description : str, optional
        Human-readable function description.
    labels : list[str], optional
        Function labels.
    embedded : bool, default=False
        Whether to embed the function specification in the project specification.

    Returns
    -------
    FunctionContainer
        Created container function entity.
    """
    if code is not None and code_src is not None:
        raise ValueError("Only one of 'code' or 'code_src' can be provided.")

    return new_function(
        project=project,
        name=name,
        kind=FunctionContainerBuilder.ENTITY_KIND,
        uuid=uuid,
        version=version,
        description=description,
        labels=labels,
        embedded=embedded,
        image=image,
        base_image=base_image,
        image_pull_policy=image_pull_policy,
        command=command,
        code=code,
        code_src=code_src,
        handler=handler,
        lang=lang,
    )
