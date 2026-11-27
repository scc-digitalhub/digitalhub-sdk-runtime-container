# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.plugins import (
    Action,
    BuilderDef,
    CrudPlugin,
    ExecFamily,
    ExecutableActions,
    FunctionBuilder,
    Run,
    RunBuilder,
    SourceBuilderMixin,
    Status,
    Task,
    TaskBuilder,
)

from digitalhub_runtime_container.entities._commons.enums import Actions, EntityKinds
from digitalhub_runtime_container.entities.function.container.crud import new_function_container
from digitalhub_runtime_container.entities.function.container.entity import FunctionContainer
from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer
from digitalhub_runtime_container.entities.run._base.status import RunStatusContainerRun
from digitalhub_runtime_container.entities.run.build.entity import RunContainerRunBuild
from digitalhub_runtime_container.entities.run.build.spec import RunSpecContainerRunBuild
from digitalhub_runtime_container.entities.run.job.spec import RunSpecContainerRunJob
from digitalhub_runtime_container.entities.run.serve.entity import RunContainerRunServe
from digitalhub_runtime_container.entities.run.serve.spec import RunSpecContainerRunServe
from digitalhub_runtime_container.entities.task.build.spec import TaskSpecContainerBuild
from digitalhub_runtime_container.entities.task.job.spec import TaskSpecContainerJob
from digitalhub_runtime_container.entities.task.serve.spec import TaskSpecContainerServe

# Imported on first use: the entities register even when the runtime cannot be
# imported, and the import error is reported when a run executes locally.
RUNTIME_CONTAINER_BUILDER = "digitalhub_runtime_container.runtimes.builder:RuntimeContainerBuilder"

container = ExecFamily(
    executable=BuilderDef(
        EntityKinds.FUNCTION_CONTAINER,
        FunctionContainer,
        FunctionSpecContainer,
        Status,
        base=FunctionBuilder,
        mixins=(SourceBuilderMixin,),
        shortcuts=(CrudPlugin(new_function_container),),
    ),
    actions={
        ExecutableActions.BUILD: Action(
            task=BuilderDef(EntityKinds.TASK_CONTAINER_BUILD, Task, TaskSpecContainerBuild, Status, base=TaskBuilder),
            run=BuilderDef(
                EntityKinds.RUN_CONTAINER_BUILD,
                RunContainerRunBuild,
                RunSpecContainerRunBuild,
                RunStatusContainerRun,
                base=RunBuilder,
            ),
        ),
        Actions.JOB: Action(
            task=BuilderDef(EntityKinds.TASK_CONTAINER_JOB, Task, TaskSpecContainerJob, Status, base=TaskBuilder),
            run=BuilderDef(
                EntityKinds.RUN_CONTAINER_JOB,
                Run,
                RunSpecContainerRunJob,
                RunStatusContainerRun,
                base=RunBuilder,
            ),
        ),
        ExecutableActions.SERVE: Action(
            task=BuilderDef(EntityKinds.TASK_CONTAINER_SERVE, Task, TaskSpecContainerServe, Status, base=TaskBuilder),
            run=BuilderDef(
                EntityKinds.RUN_CONTAINER_SERVE,
                RunContainerRunServe,
                RunSpecContainerRunServe,
                RunStatusContainerRun,
                base=RunBuilder,
            ),
        ),
    },
    runtime_builder=RUNTIME_CONTAINER_BUILDER,
)

entity_plugins = (*container.plugins(),)
