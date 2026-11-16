import pytest
from digitalhub.entities._constructors.spec import build_spec
from digitalhub.entities.task._base.models import CorePort
from pydantic import ValidationError

from digitalhub_runtime_container.entities.function.container.models import SourceValidator
from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer
from digitalhub_runtime_container.entities.run.build.spec import RunSpecContainerRunBuild
from digitalhub_runtime_container.entities.run.serve.spec import RunSpecContainerRunServe
from digitalhub_runtime_container.entities.task.build.spec import TaskSpecContainerBuild
from digitalhub_runtime_container.entities.task.job.spec import TaskSpecContainerJob
from digitalhub_runtime_container.entities.task.serve.spec import TaskSpecContainerServe


def test_container_function_spec_validates_nested_source_and_pull_policy():
    spec = build_spec(
        FunctionSpecContainer,
        source={"handler": "predict"},
        image_pull_policy="Always",
    )

    assert isinstance(spec.source, SourceValidator)
    assert spec.image_pull_policy == "Always"

    with pytest.raises(ValidationError):
        build_spec(FunctionSpecContainer, image_pull_policy="sometimes")


def test_container_task_specs_validate_runtime_fields_and_constraints():
    build = build_spec(TaskSpecContainerBuild, function="function", instructions=["apt-get update"])
    job = build_spec(TaskSpecContainerJob, function="function", run_as_user=0, run_as_group=1000, fs_group=1)
    serve = build_spec(
        TaskSpecContainerServe,
        function="function",
        replicas=0,
        service_type="ClusterIP",
        service_ports=[{"port": 8080, "target_port": 80}],
        fs_group=1,
    )

    assert build.instructions == ["apt-get update"]
    assert job.run_as_user == 0
    assert serve.replicas == 0
    assert serve.service_type == "ClusterIP"
    assert isinstance(serve.service_ports[0], CorePort)

    with pytest.raises(ValidationError):
        build_spec(TaskSpecContainerJob, function="function", fs_group=0)


def test_container_run_specs_exclude_task_fields():
    run = build_spec(RunSpecContainerRunBuild, task="task", args=["--verbose"], image="image:latest")
    assert run.args == ["--verbose"]

    with pytest.raises(TypeError, match="instructions"):
        build_spec(RunSpecContainerRunBuild, task="task", instructions=["apt-get update"])

    with pytest.raises(TypeError, match="service_type"):
        build_spec(RunSpecContainerRunServe, task="task", service_type="ClusterIP")

    with pytest.raises(TypeError, match="run_as_user"):
        build_spec(RunSpecContainerRunServe, task="task", run_as_user=1000)

    with pytest.raises(TypeError, match="replicas"):
        build_spec(TaskSpecContainerBuild, function="function", replicas=2)

    legacy = RunSpecContainerRunBuild.from_dict({"task": "task", "instructions": ["legacy build instruction"]})
    assert legacy.to_dict()["instructions"] == ["legacy build instruction"]
