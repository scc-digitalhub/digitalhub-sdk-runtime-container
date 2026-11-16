# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import BuildSpecMixin

from digitalhub_runtime_container.entities.run._base.spec import RunSpecContainerRun


class RunSpecContainerRunBuild(RunSpecContainerRun, BuildSpecMixin):
    """RunSpecContainerRunBuild specifications."""
