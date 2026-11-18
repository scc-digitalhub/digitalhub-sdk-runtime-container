# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_container.entities.run._base.entity import RunContainerRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.run._base.status import RunStatusContainerRun
    from digitalhub_runtime_container.entities.run.job.spec import RunSpecContainerRunJob


class RunContainerRunJob(RunContainerRun):
    """
    RunContainerRunJob class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecContainerRunJob
        self.status: RunStatusContainerRun
