# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status
from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_container.entities._base.runtime_entity.builder import RuntimeEntityBuilderContainer
from digitalhub_runtime_container.entities._commons.enums import EntityKinds
from digitalhub_runtime_container.entities.task.serve.entity import TaskContainerServe
from digitalhub_runtime_container.entities.task.serve.spec import TaskSpecContainerServe


class TaskContainerServeBuilder(TaskBuilder, RuntimeEntityBuilderContainer):
    """
    TaskContainerServeBuilder serveer.
    """

    ENTITY_CLASS = TaskContainerServe
    ENTITY_SPEC_CLASS = TaskSpecContainerServe
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_CONTAINER_SERVE.value
