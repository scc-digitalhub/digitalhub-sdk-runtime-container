from __future__ import annotations

from digitalhub_runtime_kfp.entities.task.kfp_pipeline.entity import TaskKfpPipeline
from digitalhub_runtime_kfp.entities.task.kfp_pipeline.spec import TaskSpecKfpPipeline, TaskValidatorKfpPipeline
from digitalhub_runtime_kfp.entities.task.kfp_pipeline.status import TaskStatusKfpPipeline

from digitalhub.entities.task._base.builder import TaskBuilder


class TaskKfpPipelineBuilder(TaskBuilder):
    """
    TaskKfpPipelineBuilder pipelineer.
    """

    ENTITY_CLASS = TaskKfpPipeline
    ENTITY_SPEC_CLASS = TaskSpecKfpPipeline
    ENTITY_SPEC_VALIDATOR = TaskValidatorKfpPipeline
    ENTITY_STATUS_CLASS = TaskStatusKfpPipeline
    ENTITY_KIND = "kfp+pipeline"
