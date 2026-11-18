# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities._mixin.source.entity import SourceEntityMixin
from digitalhub.entities.function._base.entity import Function
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.file_utils import eval_zip_type
from digitalhub.utils.generic_utils import read_source

from digitalhub_runtime_container.entities._commons.enums import Actions

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.status import Status

    from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer


class FunctionContainer(SourceEntityMixin, Function):
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

    def build(
        self,
        wait: bool = True,
        log_info: bool = True,
        extensions: list[dict] | None = None,
        **kwargs,
    ):
        """
        Build the function using the build action.

        Parameters
        ----------
        wait : bool
            Whether to wait for the build to complete.
        log_info : bool
            Whether to log information while waiting.
        extensions : list[dict] | None
            List of extensions to apply.
        **kwargs : dict
            Keyword arguments passed to the run builder.

        Returns
        -------
        Run
            Build run instance.
        """
        return super().run(
            Actions.BUILD.value,
            wait=wait,
            log_info=log_info,
            extensions=extensions,
            **kwargs,
        )

    def run(
        self,
        action: str,
        wait: bool = False,
        log_info: bool = True,
        extensions: list[dict] | None = None,
        auto_build: bool = False,
        **kwargs,
    ):
        """
        Run the function, building it first when no image is available.

        Parameters
        ----------
        action : str
            Action to execute.
        wait : bool
            Whether to wait for execution to complete.
        log_info : bool
            Whether to log information while waiting.
        extensions : list[dict] | None
            List of extensions to apply.
        auto_build : bool
            Whether to build the function when ``spec.image`` is ``None``.
        **kwargs : dict
            Keyword arguments passed to the run builder.

        Returns
        -------
        Run
            Run instance.
        """
        if auto_build and self.spec.image is None:
            self.build(wait=True, log_info=log_info)

        return super().run(
            action,
            wait=wait,
            log_info=log_info,
            extensions=extensions,
            **kwargs,
        )
