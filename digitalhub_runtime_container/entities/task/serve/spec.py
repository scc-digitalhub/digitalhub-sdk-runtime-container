# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import ServeSpecMixin, TaskSpecFunction

from digitalhub_runtime_container.entities._mixin.execution.spec import ContainerRunAsSpecMixin


class ContainerServeSpecMixin(ContainerRunAsSpecMixin, ServeSpecMixin):
    """Spec mixin for container serve action fields."""


class TaskSpecContainerServe(TaskSpecFunction, ContainerServeSpecMixin):
    """Specification for a container serving task."""
