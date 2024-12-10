from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field


class TaskSpecContainerJob(TaskSpecFunction):
    """
    TaskSpecContainerJob specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        runtime_class: str | None = None,
        priority_class: str | None = None,
        backoff_limit: int | None = None,
        schedule: str | None = None,
        run_as_user: int | None = None,
        fs_group: int | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            runtime_class,
            priority_class,
            **kwargs,
        )
        self.backoff_limit = backoff_limit
        self.schedule = schedule
        self.run_as_user = run_as_user
        self.fs_group = fs_group


class TaskValidatorContainerJob(TaskValidatorFunction):
    """
    TaskValidatorContainerJob validator.
    """

    backoff_limit: int = Field(default=None, ge=0)
    """Backoff limit."""

    schedule: str = None
    """Schedule."""

    run_as_user: int = Field(default=None, ge=0)
    """RunAsUser."""

    fs_group: int = Field(default=None, ge=1)
    """FSGroup."""
