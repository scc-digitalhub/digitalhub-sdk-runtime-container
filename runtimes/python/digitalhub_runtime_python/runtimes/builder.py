from __future__ import annotations

from digitalhub_runtime_python.runtimes.kind_registry import kind_registry
from digitalhub_runtime_python.runtimes.runtime import RuntimePython

from digitalhub.runtimes.builder import RuntimeBuilder


class RuntimePythonBuilder(RuntimeBuilder):
    """RuntaimePythonBuilder class."""

    RUNTIME_CLASS = RuntimePython
    KIND_REGISTRY = kind_registry