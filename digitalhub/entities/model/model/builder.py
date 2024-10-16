from __future__ import annotations

from digitalhub.entities.model._base.builder import ModelBuilder
from digitalhub.entities.model.model.entity import ModelModel
from digitalhub.entities.model.model.spec import ModelSpecModel, ModelValidatorModel
from digitalhub.entities.model.model.status import ModelStatusModel


class ModelModelBuilder(ModelBuilder):
    """
    ModelModel builder.
    """

    ENTITY_CLASS = ModelModel
    ENTITY_SPEC_CLASS = ModelSpecModel
    ENTITY_SPEC_VALIDATOR = ModelValidatorModel
    ENTITY_STATUS_CLASS = ModelStatusModel
