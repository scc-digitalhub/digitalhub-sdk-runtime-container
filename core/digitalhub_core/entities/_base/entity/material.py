from __future__ import annotations

import typing

from digitalhub_core.entities._base.crud import files_info_put_api
from digitalhub_core.entities._base.entity.versioned import VersionedEntity
from digitalhub_core.stores.builder import get_store

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities._base.spec.material import MaterialSpec
    from digitalhub_core.entities._base.status.material import MaterialStatus


class MaterialEntity(VersionedEntity):
    """
    A class representing an entity that can be materialized
    as file(s).
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: MaterialSpec,
        status: MaterialStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)
        self.spec: MaterialSpec
        self.status: MaterialStatus

    def save(self, update: bool = False) -> MaterialEntity:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        MaterialEntity
            Entity saved.
        """
        obj = self.to_dict()

        files = None
        if len(self.status.files) > 5 and not self._context().local:
            files = obj["status"].pop("files")

        if not update:
            new_obj: MaterialEntity = self._save(obj)
        else:
            new_obj: MaterialEntity = self._update(obj)

        # Handle file infos
        if files is not None:
            files_info_put_api(self.project, self.ENTITY_TYPE, self.id, files)
            new_obj.status.files = files

        return new_obj

    #############################
    # I/O Methods
    #############################

    def as_file(self) -> list[str]:
        """
        Get object as file(s).

        Returns
        -------
        list[str]
            List of file paths.
        """
        store = get_store(self.spec.path)
        paths = self._get_paths()
        return store.download(paths)

    def download(
        self,
        destination: str | None = None,
        overwrite: bool = False,
    ) -> str:
        """
        Download object from storage into given local path.

        Parameters
        ----------
        destination : str
            Destination path as filename or directory.
        overwrite : bool
            Specify if overwrite existing file(s).

        Returns
        -------
        list[str]
            List of downloaded file paths.
        """
        store = get_store(self.spec.path)
        paths = self._get_paths()

        if destination is None:
            destination = str(self._context().root / self.ENTITY_TYPE / self.name)

        return store.download(paths, dst=destination, overwrite=overwrite)

    def upload(self, source: str) -> None:
        """
        Upload dataitem from given local path to spec path destination.

        Parameters
        ----------
        source : str
            Source path is the local path of the dataitem.

        Returns
        -------
        str
            Path of the uploaded dataitem.
        """
        # Get store and upload dataitem
        store = get_store(self.spec.path)
        paths = store.upload(source, self.spec.path)

        # Update file infos
        file_infos = store.get_file_info(paths)
        self._update_file_infos(file_infos)

    #############################
    #  Private Helpers
    #############################

    def _get_paths(self) -> list[tuple[str, str | None]]:
        """
        Get paths from spec.

        Returns
        -------
        list[tuple[str, str | None]]
            List of paths.
        """
        # Try to download from file infos in status
        paths = self.status.get_file_paths()

        # Fallback to spec path
        if not paths:
            paths = [(self.spec.path, None)]

        return paths

    def _update_file_infos(self, file_infos: list[dict] | None = None) -> None:
        """
        Update file infos.

        Parameters
        ----------
        file_infos : list[dict] | None
            File infos.

        Returns
        -------
        None
        """
        if file_infos is None:
            return
        self.refresh()
        self.status.add_file(file_infos)
        self.save(update=True)
