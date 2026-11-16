# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_container.entities.run._base.spec import RunSpecContainerRun
from digitalhub_runtime_container.entities.task.serve.spec import ContainerServeSpecMixin


class RunSpecContainerRunServe(RunSpecContainerRun, ContainerServeSpecMixin):
    """RunSpecContainerRunServe specifications."""
