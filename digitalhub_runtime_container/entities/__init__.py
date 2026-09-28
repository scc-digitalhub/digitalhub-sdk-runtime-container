# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.factory.plugins import CrudPlugin, EntityPlugin

from digitalhub_runtime_container.entities.function.container.builder import FunctionContainerBuilder
from digitalhub_runtime_container.entities.function.container.crud import new_function_container
from digitalhub_runtime_container.entities.run.build.builder import RunContainerRunBuildBuilder
from digitalhub_runtime_container.entities.run.job.builder import RunContainerRunJobBuilder
from digitalhub_runtime_container.entities.run.serve.builder import RunContainerRunServeBuilder
from digitalhub_runtime_container.entities.task.build.builder import TaskContainerBuildBuilder
from digitalhub_runtime_container.entities.task.job.builder import TaskContainerJobBuilder
from digitalhub_runtime_container.entities.task.serve.builder import TaskContainerServeBuilder

function_container_plugin = EntityPlugin(
    builder=FunctionContainerBuilder,
    shortcuts=(CrudPlugin(new_function_container),),
)

entity_plugins = (
    function_container_plugin,
    EntityPlugin(builder=TaskContainerBuildBuilder),
    EntityPlugin(builder=TaskContainerJobBuilder),
    EntityPlugin(builder=TaskContainerServeBuilder),
    EntityPlugin(builder=RunContainerRunBuildBuilder),
    EntityPlugin(builder=RunContainerRunJobBuilder),
    EntityPlugin(builder=RunContainerRunServeBuilder),
)
