# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.spec import FunctionSpec
from digitalhub.entities.task._base.models import CorePullPolicy

from digitalhub_runtime_container.entities.function.container.models import ContainerSourceCode


class FunctionSpecContainer(FunctionSpec):
    """Function specification for container functions."""

    image: str | None = None
    """Name of the function's container image."""

    base_image: str | None = None
    """Base image used to build the function image."""

    image_pull_policy: CorePullPolicy | None = None
    """Function's container image pull policy."""

    command: str | None = None
    """Command to run inside the container."""

    source: ContainerSourceCode | None = None
    """Source code parameters."""
