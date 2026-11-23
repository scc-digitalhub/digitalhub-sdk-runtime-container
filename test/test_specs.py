import pytest
from digitalhub.entities._constructors.spec import build_spec
from digitalhub.entities._frameworks.k8s.models import CorePort
from pydantic import ValidationError

from digitalhub_runtime_container.entities.function.container.builder import FunctionContainerBuilder
from digitalhub_runtime_container.entities.function.container.models import ContainerSourceCode
from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer
from digitalhub_runtime_container.entities.run.build.spec import RunSpecContainerRunBuild
from digitalhub_runtime_container.entities.run.job.spec import RunSpecContainerRunJob
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

    assert isinstance(spec.source, ContainerSourceCode)
    assert spec.image_pull_policy == "Always"

    with pytest.raises(ValidationError):
        build_spec(FunctionSpecContainer, image_pull_policy="sometimes")


def test_container_builder_routes_top_level_source_arguments():
    builder = FunctionContainerBuilder()

    function = builder.build(
        kind=builder.ENTITY_KIND,
        project="project",
        name="function",
        code="select 1",
        handler="main",
    )

    assert function.spec.source.base64 == "c2VsZWN0IDE="
    assert function.spec.source.handler == "main"


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


def test_container_run_specs_merge_only_action_fields():
    build = build_spec(
        RunSpecContainerRunBuild,
        function="function",
        task="task",
        args=["--verbose"],
        image="image:latest",
        instructions=["apt-get update"],
    )
    job = build_spec(RunSpecContainerRunJob, function="function", task="task", run_as_user=1000)
    serve = build_spec(
        RunSpecContainerRunServe,
        function="function",
        task="task",
        service_type="ClusterIP",
        run_as_user=1000,
        replicas=2,
    )

    assert build.args == ["--verbose"]
    assert build.instructions == ["apt-get update"]
    assert job.run_as_user == 1000
    assert serve.service_type == "ClusterIP"
    assert serve.run_as_user == 1000
    assert serve.replicas == 2

    with pytest.raises(TypeError, match="instructions"):
        build_spec(RunSpecContainerRunJob, function="function", task="task", instructions=["apt-get update"])

    with pytest.raises(TypeError, match="replicas"):
        build_spec(RunSpecContainerRunJob, function="function", task="task", replicas=2)

    with pytest.raises(TypeError, match="replicas"):
        build_spec(TaskSpecContainerBuild, function="function", replicas=2)

    legacy = RunSpecContainerRunBuild.from_dict(
        {"function": "function", "task": "task", "instructions": ["legacy build instruction"]}
    )
    assert legacy.to_dict()["instructions"] == ["legacy build instruction"]
