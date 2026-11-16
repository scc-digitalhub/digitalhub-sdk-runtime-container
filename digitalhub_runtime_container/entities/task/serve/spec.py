# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.models import CorePort, CoreServiceType
from digitalhub.entities.task._base.spec import TaskSpecFunction
from pydantic import Field

from digitalhub_runtime_container.entities.task.job.spec import ContainerRunAsSpecMixin


class ContainerServeSpecMixin(ContainerRunAsSpecMixin):
    """Spec mixin for container serve action fields."""

    replicas: int | None = Field(default=None, ge=0)
    """Number of replicas."""

    service_ports: list[CorePort] | None = None
    """Service ports mapper."""

    service_type: CoreServiceType | None = None
    """Service type."""

    service_name: str | None = None
    """Service name."""


class TaskSpecContainerServe(TaskSpecFunction, ContainerServeSpecMixin):
    """Specification for a container serving task."""
