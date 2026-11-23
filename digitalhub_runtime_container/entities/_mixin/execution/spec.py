# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.spec import Spec
from pydantic import Field


class ContainerRunAsSpecMixin(Spec):
    """Spec mixin for container run-as fields."""

    run_as_user: int | None = Field(default=None, ge=0)
    run_as_group: int | None = Field(default=None, ge=0)
    fs_group: int | None = Field(default=None, ge=1)
