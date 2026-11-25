# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import RunSpecFunction


class RunSpecContainerRun(RunSpecFunction):
    """Specification shared by container runs."""

    args: list[str] | None = None
    """Arguments to pass to the entrypoint."""

    source: dict | None = None
    image: str | None = None
    base_image: str | None = None
    image_pull_policy: str | None = None
    command: str | None = None
