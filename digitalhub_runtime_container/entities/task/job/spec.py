# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction
from pydantic import Field


class TaskSpecContainerJob(TaskSpecFunction):
    """Specification for a container job task."""

    run_as_user: int | None = Field(default=None, ge=0)
    """RunAsUser."""

    run_as_group: int | None = Field(default=None, ge=0)
    """RunAsGroup."""

    fs_group: int | None = Field(default=None, ge=1)
    """FSGroup."""
