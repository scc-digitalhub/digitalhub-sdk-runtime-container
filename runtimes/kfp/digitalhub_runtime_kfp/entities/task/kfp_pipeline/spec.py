from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecK8s, TaskValidatorK8s


class TaskSpecKfpPipeline(TaskSpecK8s):
    """
    TaskSpecKfpPipeline specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        schedule: str | None = None,
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
        self.schedule = schedule


class TaskValidatorKfpPipeline(TaskValidatorK8s):
    """
    TaskValidatorKfpPipeline validator.
    """

    schedule: str = None
    """KFP schedule specifications."""
