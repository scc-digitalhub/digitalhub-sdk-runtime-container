from __future__ import annotations

from digitalhub_core.registry.registry import registry
from digitalhub_core.registry.utils import create_info
from digitalhub_data.entities.entity_types import EntityTypes

root = "digitalhub_runtime_dbt"
runtime_info = {
    "module": f"{root}.runtimes.runtime",
    "class_name": "RuntimeDbt",
}

root_ent = f"{root}.entities"


# Function
entity_type = EntityTypes.FUNCTIONS.value
func_kind = "dbt"
prefix = entity_type.removesuffix("s").capitalize()
suffix = func_kind.capitalize()
func_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
registry.register(func_kind, func_info)


# Tasks
entity_type = EntityTypes.TASKS.value
for i in ["transform"]:
    task_kind = f"{func_kind}+{i}"
    prefix = entity_type.removesuffix("s").capitalize()
    suffix = i.capitalize()
    task_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
    registry.register(task_kind, task_info)


# Runs
entity_type = EntityTypes.RUNS.value
run_kind = f"{func_kind}+run"
prefix = entity_type.removesuffix("s").capitalize()
suffix = func_kind.capitalize()
run_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
registry.register(run_kind, run_info)