from digitalhub_core.runtimes.registry import RuntimeRegistry

registry = RuntimeRegistry()
registry.register(
    "digitalhub_data_nefertem.runtime.runtime",
    "RuntimeNefertem",
)
