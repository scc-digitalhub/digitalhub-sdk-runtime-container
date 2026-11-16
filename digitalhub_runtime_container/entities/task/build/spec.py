# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import BuildSpecMixin, TaskSpecFunction


class TaskSpecContainerBuild(TaskSpecFunction, BuildSpecMixin):
    """Specification for a container build task."""

    """Build instructions."""
