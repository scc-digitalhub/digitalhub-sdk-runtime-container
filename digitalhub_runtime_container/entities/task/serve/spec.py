# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.models import CorePort, CoreServiceType
from digitalhub.entities.task._base.spec import TaskSpecFunction
from pydantic import Field


class TaskSpecContainerServe(TaskSpecFunction):
    """Specification for a container serving task."""

    replicas: int | None = Field(default=None, ge=0)
    """Number of replicas."""

    service_ports: list[CorePort] | None = None
    """Service ports mapper."""

    service_type: CoreServiceType | None = None
    """Service type."""

    service_name: str | None = None
    """Service name."""

    run_as_user: int | None = Field(default=None, ge=0)
    """RunAsUser."""

    run_as_group: int | None = Field(default=None, ge=0)
    """RunAsGroup."""

    fs_group: int | None = Field(default=None, ge=1)
    """FSGroup."""
