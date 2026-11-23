# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub_runtime_container.entities._mixin.execution.spec import ContainerRunAsSpecMixin
from digitalhub_runtime_container.entities.run.job.spec import RunSpecContainerRunJob
from digitalhub_runtime_container.entities.task.job.spec import TaskSpecContainerJob
from digitalhub_runtime_container.entities.task.serve.spec import TaskSpecContainerServe


def test_run_as_mixin_has_one_runtime_owner() -> None:
    assert ContainerRunAsSpecMixin in TaskSpecContainerJob.__mro__
    assert ContainerRunAsSpecMixin in TaskSpecContainerServe.__mro__
    assert ContainerRunAsSpecMixin in RunSpecContainerRunJob.__mro__
