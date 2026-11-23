# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_container.entities._mixin.execution.spec import ContainerRunAsSpecMixin
from digitalhub_runtime_container.entities.run._base.spec import RunSpecContainerRun


class RunSpecContainerRunJob(RunSpecContainerRun, ContainerRunAsSpecMixin):
    """RunSpecContainerRunJob specifications."""
