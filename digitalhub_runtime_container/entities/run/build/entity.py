# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.run._base.status import RunStatusContainerRun
    from digitalhub_runtime_container.entities.run.build.spec import RunSpecContainerRunBuild


class RunContainerRunBuild(Run):
    """
    RunContainerRunBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecContainerRunBuild
        self.status: RunStatusContainerRun

    @property
    def image(self) -> str | None:
        """
        Get run's image.

        Returns
        -------
        str | None
            The image.
        """
        return self.status.outputs.get("image")
