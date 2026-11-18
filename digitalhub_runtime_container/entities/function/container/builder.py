# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status
from digitalhub.entities._mixin.source.builder import SourceBuilderMixin
from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_container.entities._base.runtime_entity.builder import RuntimeEntityBuilderContainer
from digitalhub_runtime_container.entities._commons.enums import EntityKinds
from digitalhub_runtime_container.entities.function.container.entity import FunctionContainer
from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer


class FunctionContainerBuilder(SourceBuilderMixin, FunctionBuilder, RuntimeEntityBuilderContainer):
    """
    FunctionContainer builder.
    """

    ENTITY_CLASS = FunctionContainer
    ENTITY_SPEC_CLASS = FunctionSpecContainer
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.FUNCTION_CONTAINER.value
