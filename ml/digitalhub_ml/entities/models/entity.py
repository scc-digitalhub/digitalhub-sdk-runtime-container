from __future__ import annotations

import typing
from pathlib import Path
from urllib.parse import urlparse

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.crud import create_entity_api_ctx, read_entity_api_ctx, update_entity_api_ctx
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.stores.builder import get_store
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import get_timestamp
from digitalhub_core.utils.io_utils import write_yaml
from digitalhub_core.utils.uri_utils import check_local_path
from digitalhub_ml.entities.entity_types import EntityTypes

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_ml.entities.models.spec import ModelSpec
    from digitalhub_ml.entities.models.status import ModelStatus


class Model(Entity):
    """
    A class representing a model.
    """

    ENTITY_TYPE = EntityTypes.MODELS.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: ModelSpec,
        status: ModelStatus,
        user: str | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Project name.
        name : str
            Name of the object.
        uuid : str
            Version of the object.
        kind : str
            Kind the object.
        metadata : Metadata
            Metadata of the object.
        spec : ModelSpec
            Specification of the object.
        status : ModelStatus
            Status of the object.
        user : str
            Owner of the object.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = uuid
        self.kind = kind
        self.key = f"store://{project}/{self.ENTITY_TYPE}/{kind}/{name}:{uuid}"
        self.metadata = metadata
        self.spec = spec
        self.status = status
        self.user = user

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["project", "name", "id", "key"])

    #############################
    #  Save / Refresh / Export
    #############################

    def save(self, update: bool = False) -> Model:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        Model
            Entity saved.
        """
        obj = self.to_dict()

        if not update:
            new_obj = create_entity_api_ctx(self.project, self.ENTITY_TYPE, obj)
            self._update_attributes(new_obj)
            return self

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        new_obj = update_entity_api_ctx(self.project, self.ENTITY_TYPE, self.id, obj)
        self._update_attributes(new_obj)
        return self

    def refresh(self) -> Model:
        """
        Refresh object from backend.

        Returns
        -------
        Model
            Entity refreshed.
        """
        new_obj = read_entity_api_ctx(self.key)
        self._update_attributes(new_obj)
        return self

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self.to_dict()
        if filename is None:
            filename = f"{self.kind}_{self.name}_{self.id}.yml"
        pth = self._context().root / filename
        pth.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(pth, obj)

    #############################
    #  Context
    #############################

    def _context(self) -> Context:
        """
        Get context.

        Returns
        -------
        Context
            Context.
        """
        return get_context(self.project)

    #############################
    #  Model methods
    #############################

    def as_file(self) -> str:
        """
        Get model as file. In the case of a local store, the store returns the current
        path of the model. In the case of a remote store, the model is downloaded in
        a temporary directory.

        Returns
        -------
        str
            Path of the model.
        """
        path = self.spec.path
        store = get_store(path)
        return store.download(path)

    def download(
        self,
        destination: str | None = None,
        force_download: bool = False,
        overwrite: bool = False,
    ) -> str:
        """
        Download model from storage. If store is local, the model is copied to
        destination path.

        Parameters
        ----------
        destination : str
            Destination path as filename.
        force_download : bool
            Force download if a previous download was already done.
        overwrite : bool
            Specify if overwrite an existing file. Default value is False.

        Returns
        -------
        str
            Path of the downloaded model.
        """

        # Check if target path is remote
        path = self.spec.path
        store = get_store(path)

        # Check if download destination path is specified and rebuild it if necessary
        if destination is None:
            filename = Path(urlparse(path).path).name
            destination = f"{self.project}/{self.ENTITY_TYPE}/{self.name}/{self.id}/{filename}"

        # Download dataitem and return path
        return store.download(path, dst=destination, force=force_download, overwrite=overwrite)

    def upload(self, source: str) -> str:
        """
        Upload model from given local path to spec path destination.

        Parameters
        ----------
        source : str
            Source path is the local path of the model.

        Returns
        -------
        str
            Path of the uploaded model.
        """
        # Check if target path is remote
        path = self.spec.path
        store = get_store(path)

        # Get store and upload model and return remote path
        target = store.upload(source, path)
        file_info = store.get_file_info(target, source)

        if file_info is not None:
            self.refresh()
            self.status.add_file(file_info)
            self.save(update=True)

        return target

    #############################
    #  Private Helpers
    #############################

    @staticmethod
    def _check_local(path: str) -> None:
        """
        Check through URI scheme if given path is local or not.

        Parameters
        ----------
        path : str
            Path of some source.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If source path is not local.
        """
        if not check_local_path(path):
            raise EntityError("Only local paths are supported for source paths.")

    #############################
    #  Static interface methods
    #############################

    @staticmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        name = build_name(obj.get("name"))
        kind = obj.get("kind")
        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(kind, **obj.get("metadata", {}))
        spec = build_spec(kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, **obj.get("status", {}))
        user = obj.get("user")
        return {
            "project": project,
            "name": name,
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "user": user,
        }


def model_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    git_source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    framework: str | None = None,
    algorithm: str | None = None,
    **kwargs,
) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4).
    git_source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    description : str
        Description of the object (human readable).
    embedded : bool
        Flag to determine if object must be embedded in project.
    path : str
        Object path on local file system or remote storage.
        If not provided, it's generated.
    framework : str
        Model framework (e.g. 'pytorch').
    algorithm : str
        Model algorithm (e.g. 'resnet').
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    if path is None:
        raise EntityError("Path must be provided.")
    name = build_name(name)
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        kind,
        project=project,
        name=name,
        version=uuid,
        description=description,
        source=git_source,
        labels=labels,
        embedded=embedded,
    )
    spec = build_spec(
        kind,
        path=path,
        framework=framework,
        algorithm=algorithm,
        **kwargs,
    )
    status = build_status(kind)
    return Model(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def model_from_dict(obj: dict) -> Model:
    """
    Create Model instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Model
        Model instance.
    """
    return Model.from_dict(obj)
