# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_container.entities._base.runtime_entity.builder import RuntimeEntityBuilderContainer

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.run.build.spec import RunSpecContainerRunBuild
    from digitalhub_runtime_container.entities.run.build.status import RunStatusContainerRunBuild


class RunContainerRunBuild(RunBuilder, RuntimeEntityBuilderContainer):
    """
    RunContainerRunBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecContainerRunBuild
        self.status: RunStatusContainerRunBuild
