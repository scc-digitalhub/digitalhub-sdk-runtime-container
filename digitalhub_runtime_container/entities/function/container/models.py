# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import ClassVar

from digitalhub.plugins import HandlerSourceCode


class ContainerSourceCode(HandlerSourceCode):
    """Source code model for container functions."""

    REQUIRE_SOURCE: ClassVar[bool] = False
    REQUIRE_HANDLER: ClassVar[bool] = False
