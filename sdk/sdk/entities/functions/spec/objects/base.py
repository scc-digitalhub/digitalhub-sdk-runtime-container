"""
Base Function specification module.
"""
from pydantic import BaseModel

from sdk.entities.base.spec import Spec


class FunctionSpec(Spec):
    """
    Specification for a Function.
    """

    def __init__(
        self,
        source: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source : str
            Path to the Function's source code on the local file system.
        **kwargs
            Keyword arguments.
        """
        self.source = source

        self._any_setter(**kwargs)


class FunctionParams(BaseModel):
    """
    Function parameters model.
    """

    source: str | None = None
    """Path to the Function's source code on the local file system."""