# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.plugins import CrudPlugin, EntityPlugin

from digitalhub_runtime_container.entities.function.container.builder import FunctionContainerBuilder
from digitalhub_runtime_container.entities.function.container.crud import new_function_container
from digitalhub_runtime_container.entities.run.build.builder import RunContainerRunBuildBuilder
from digitalhub_runtime_container.entities.run.job.builder import RunContainerRunJobBuilder
from digitalhub_runtime_container.entities.run.serve.builder import RunContainerRunServeBuilder
from digitalhub_runtime_container.entities.task.build.builder import TaskContainerBuildBuilder
from digitalhub_runtime_container.entities.task.job.builder import TaskContainerJobBuilder
from digitalhub_runtime_container.entities.task.serve.builder import TaskContainerServeBuilder

# Imported on first use: the entities register even when the runtime cannot be
# imported, and the import error is reported when a run executes locally.
RUNTIME_CONTAINER_BUILDER = "digitalhub_runtime_container.runtimes.builder:RuntimeContainerBuilder"

function_container_plugin = EntityPlugin(
    builder=FunctionContainerBuilder,
    shortcuts=(CrudPlugin(new_function_container),),
    runtime_builder=RUNTIME_CONTAINER_BUILDER,
)

entity_plugins = (
    function_container_plugin,
    EntityPlugin(builder=TaskContainerBuildBuilder, runtime_builder=RUNTIME_CONTAINER_BUILDER),
    EntityPlugin(builder=TaskContainerJobBuilder, runtime_builder=RUNTIME_CONTAINER_BUILDER),
    EntityPlugin(builder=TaskContainerServeBuilder, runtime_builder=RUNTIME_CONTAINER_BUILDER),
    EntityPlugin(builder=RunContainerRunBuildBuilder, runtime_builder=RUNTIME_CONTAINER_BUILDER),
    EntityPlugin(builder=RunContainerRunJobBuilder, runtime_builder=RUNTIME_CONTAINER_BUILDER),
    EntityPlugin(builder=RunContainerRunServeBuilder, runtime_builder=RUNTIME_CONTAINER_BUILDER),
)
