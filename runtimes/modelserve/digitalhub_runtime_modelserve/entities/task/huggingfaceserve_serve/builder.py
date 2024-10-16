from __future__ import annotations

from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.entity import TaskHuggingfaceserveServe
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.spec import (
    TaskSpecHuggingfaceserveServe,
    TaskValidatorHuggingfaceserveServe,
)
from digitalhub_runtime_modelserve.entities.task.huggingfaceserve_serve.status import TaskStatusHuggingfaceserveServe

from digitalhub.entities.task._base.builder import TaskBuilder


class TaskHuggingfaceserveServeBuilder(TaskBuilder):
    """
    TaskHuggingfaceserveServe builder.
    """

    ENTITY_CLASS = TaskHuggingfaceserveServe
    ENTITY_SPEC_CLASS = TaskSpecHuggingfaceserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorHuggingfaceserveServe
    ENTITY_STATUS_CLASS = TaskStatusHuggingfaceserveServe
