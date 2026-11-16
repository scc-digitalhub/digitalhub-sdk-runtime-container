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

try:
    from digitalhub_runtime_container.runtimes.builder import RuntimeContainerBuilder
except ImportError as e:
    from digitalhub.utils.logger.logger import get_logger

    get_logger(__name__).debug(f"Error importing runtime builder: {e}")
    RuntimeContainerBuilder = None

function_container_plugin = EntityPlugin(
    builder=FunctionContainerBuilder,
    shortcuts=(CrudPlugin(new_function_container),),
    runtime_builder=RuntimeContainerBuilder,
)

entity_plugins = (
    function_container_plugin,
    EntityPlugin(builder=TaskContainerBuildBuilder, runtime_builder=RuntimeContainerBuilder),
    EntityPlugin(builder=TaskContainerJobBuilder, runtime_builder=RuntimeContainerBuilder),
    EntityPlugin(builder=TaskContainerServeBuilder, runtime_builder=RuntimeContainerBuilder),
    EntityPlugin(builder=RunContainerRunBuildBuilder, runtime_builder=RuntimeContainerBuilder),
    EntityPlugin(builder=RunContainerRunJobBuilder, runtime_builder=RuntimeContainerBuilder),
    EntityPlugin(builder=RunContainerRunServeBuilder, runtime_builder=RuntimeContainerBuilder),
)
