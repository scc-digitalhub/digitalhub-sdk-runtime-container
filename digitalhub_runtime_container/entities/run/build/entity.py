# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_container.entities.run._base.entity import RunContainerRun

if typing.TYPE_CHECKING:

    from digitalhub_runtime_container.entities.run.build.spec import RunSpecContainerRunBuild
    from digitalhub_runtime_container.entities.run.build.status import RunStatusContainerRunBuild


class RunContainerRunBuild(RunContainerRun):
    """
    RunContainerRunBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecContainerRunBuild
        self.status: RunStatusContainerRunBuild
