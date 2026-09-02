# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.function._base.entity import Function
from digitalhub.utils.generic_utils import decode_base64_string
from digitalhub.utils.io_utils import write_text
from digitalhub.utils.uri_utils import has_local_scheme

from digitalhub_runtime_container.entities._commons.enums import Actions

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer
    from digitalhub_runtime_container.entities.function.container.status import FunctionStatusContainer


class FunctionContainer(Function):
    """
    FunctionContainer class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: FunctionSpecContainer
        self.status: FunctionStatusContainer

    def export(self) -> str:
        """
        Export object as a YAML file in the context folder.

        Returns
        -------
        str
            Exported filepath.
        """
        # Strip base64 from source at following conditions:
        # - source is local path
        # - base64 is not None

        # Check source
        source = self.spec.source.get("source")
        if source is not None and has_local_scheme(source):
            # Check base64. If it is set, decode it in a local file
            # save in variable to restore on object after export
            base64 = self.spec.source.pop("base64", None)
            if base64 is not None:
                # Write local file
                src_pth = self._context().root / source
                write_text(src_pth, decode_base64_string(base64))

                # Export and restore base64, then return
                pth = super().export()
                self.spec.source["base64"] = base64
                return pth

        return super().export()

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
