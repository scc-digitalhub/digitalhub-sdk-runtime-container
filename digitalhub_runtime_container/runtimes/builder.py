# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import RuntimeBuilder

from digitalhub_runtime_container.runtimes.runtime import RuntimeContainer


class RuntimeContainerBuilder(RuntimeBuilder):
    """RuntaimeContainerBuilder class."""

    RUNTIME_CLASS = RuntimeContainer
