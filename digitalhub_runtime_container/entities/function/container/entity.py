# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import ExecutableBuildMixin, Function, SourceEntityMixin
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.file_utils import eval_zip_type
from digitalhub.utils.generic_utils import read_source

if typing.TYPE_CHECKING:
    from digitalhub.plugins import Status

    from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer


class FunctionContainer(SourceEntityMixin, ExecutableBuildMixin, Function):
    """
    FunctionContainer class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: FunctionSpecContainer
        self.status: Status

    def _is_inlineable_source(self, path: str) -> bool:
        return not eval_zip_type(path)

    def _read_inline_source(self, path: str) -> str:
        try:
            return read_source(path)
        except (OSError, UnicodeError) as error:
            raise EntityError(f"Error reading source {path}: {error}") from error
