# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.runtimes._base import Runtime


class RuntimeContainer(Runtime):
    """
    Runtime Container class.
    """

    def run(self, run: dict) -> dict:
        """
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        task_kind = run["spec"]["task"].split(":")[0]
        raise NotImplementedError(f"Local execution not implemented for task kind: {task_kind}")
