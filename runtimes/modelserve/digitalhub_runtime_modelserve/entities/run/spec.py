from __future__ import annotations

from digitalhub_ml.entities.run.spec import RunParamsMl, RunSpecMl

class RunSpecModelserve(RunSpecMl):
    """Run model serving specification."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(task, local_execution)
        self.image = kwargs.get("image")
        self.function = kwargs.get("function")
        self.node_selector = kwargs.get("node_selector")
        self.volumes = kwargs.get("volumes")
        self.resources = kwargs.get("resources")
        self.affinity = kwargs.get("affinity")
        self.tolerations = kwargs.get("tolerations")
        self.env = kwargs.get("env")
        self.secrets = kwargs.get("secrets")
        self.service_type = kwargs.get("service_type")
        self.replicas = kwargs.get("replicas")

class RunParamsModelserve(RunParamsMl):
    """Run Model serving parameters."""

    # Function parameters
    image: str = None

    # Task parameters
    function: str = None
    node_selector: list[dict] = None
    volumes: list[dict] = None
    resources: list[dict] = None
    affinity: dict = None
    tolerations: list[dict] = None
    env: list[dict] = None
    secrets: list[str] = None

    # Task serve
    service_type: str = None
    replicas: int = None

class RunSpecSklearnserve(RunSpecModelserve):
    """Run SKLearn model serving specification."""

class RunSpecMlflowserve(RunSpecModelserve):
    """Run MLFLow model serving specification."""

class RunSpecHuggingfaceserve(RunSpecModelserve):
    """Run Huggingface model serving specification."""

class RunParamsSklearnserve(RunParamsModelserve):
    """Run SKLearn model serving parameters."""

class RunParamsMlflowserve(RunParamsModelserve):
    """Run MLFLow model serving parameters."""

class RunParamsHuggingfaceserve(RunParamsModelserve):
    """Run Huggingface model serving parameters."""

