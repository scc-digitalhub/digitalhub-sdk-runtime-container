# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import Run, ServeRunMixin

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.run._base.status import RunStatusContainerRun
    from digitalhub_runtime_container.entities.run.serve.spec import RunSpecContainerRunServe


class RunContainerRunServe(ServeRunMixin, Run):
    """
    RunContainerRunServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecContainerRunServe
        self.status: RunStatusContainerRun
