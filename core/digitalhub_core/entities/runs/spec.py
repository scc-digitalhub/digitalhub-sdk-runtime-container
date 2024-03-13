"""
Run base specification module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._base.spec import Spec, SpecParams
from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.utils.generic_utils import parse_entity_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity


ENTITY_FUNC = {
    "artifacts": get_artifact_from_key,
}


class RunSpec(Spec):
    """Run specification."""

    def __init__(
        self,
        task: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        task : str
            The task associated with the run.
        inputs : dict
            The inputs of the run.
        outputs : dict
            The outputs of the run.
        parameters : dict
            The parameters for the run.
        local_execution : bool
            Flag to indicate if the run will be executed locally
        **kwargs
            Keywords arguments.
        """
        self.task = task
        self.inputs = inputs if inputs is not None else []
        self.outputs = outputs if outputs is not None else []
        self.parameters = parameters if parameters is not None else {}
        self.local_execution = local_execution

    def get_inputs(self, as_dict: bool = False) -> list[dict[str, Entity]]:
        """
        Get inputs.

        Returns
        -------
        list[dict[str, Entity]]
            The inputs.
        """
        inputs = []
        for i in self.inputs:
            for k, v in i.items():
                parameter, entity_type, _ = self._parse_input_key(k)

                # TODO: Check if entity exists, otherwise create it

                if entity_type is None:
                    # Get entity by type from entity key
                    if v.startswith("store://"):
                        _, entity_type, _, _, _ = parse_entity_key(v)
                        entity = ENTITY_FUNC[entity_type](v)
                        if as_dict:
                            entity = entity.to_dict()
                        inputs.append({parameter: entity})
                    else:
                        raise ValueError(f"Invalid entity key: {v}")

                # TODO: Create new entity
                else:
                    raise NotImplementedError

        return inputs

    @staticmethod
    def _parse_input_key(key: str) -> tuple:
        """
        Parse input key.

        Parameters
        ----------
        key : str
            Input key.

        Returns
        -------
        tuple
            The parsed key.
        """
        # Get parameter name
        splitted = key.split(":")
        parameter = splitted[0]

        try:
            splitted = splitted[1].split(".")
        except IndexError:
            return parameter, None, None

        # Get entity type
        if len(splitted) == 1:
            return parameter, splitted[0], None

        # Get entity kind
        return parameter, splitted[0], splitted[1]

    @staticmethod
    def _entity_type_from_entity_key(key: str) -> str:
        """
        Split key and return entity type.

        Parameters
        ----------
        key : str
            Entity key.

        Returns
        -------
        str
            Entity type.
        """
        key = key.replace("store://", "")
        return key.split("/")[1]


class RunParams(SpecParams):
    """
    Run parameters.
    """

    task: str = None
    """The task string associated with the run."""

    inputs: list[dict[str, str]] = None
    """Run inputs."""

    outputs: list[dict[str, str]] = None
    """Run outputs."""

    parameters: dict = None
    """Parameters to be used in the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
