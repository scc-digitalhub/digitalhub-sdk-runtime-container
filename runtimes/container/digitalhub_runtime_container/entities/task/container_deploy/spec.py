from __future__ import annotations

from pydantic import Field

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecContainerDeploy(TaskSpecFunction):
    """
    TaskSpecContainerDeploy specifications.
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
        replicas: int | None = None,
        fsGroup: int | None = None,
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
            **kwargs,
        )
        self.replicas = replicas
        self.fsGroup = fsGroup


class TaskValidatorContainerDeploy(TaskValidatorFunction):
    """
    TaskValidatorContainerDeploy validator.
    """

    replicas: int = Field(default=None, ge=1)
    """Number of replicas."""

    fsGroup: int = Field(default=None, ge=1)
    """FSGroup."""
