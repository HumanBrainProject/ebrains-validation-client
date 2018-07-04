"""
Defines classes for interacting with remote data stores.

Currently supported:
    - HBP Collaboratory storage
    - Swift CSCS storage
    - ModelDB

Other possibilities:
    - Fenix storage
    - Zenodo
    - Open Science Framework
    - Figshare
    - Dropbox
    - OwnCloud
    - ...
"""

import os
import json
try:
    input = raw_input  # Py2
    from urllib import urlretrieve
    from urlparse import urlparse
except (NameError, ImportError):
    from urllib.request import urlretrieve  # Py3
    from urllib.parse import urlparse
import mimetypes
import requests
from hbp_service_client.storage_service.api import ApiClient

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # Python 2 backport

mimetypes.init()


class FileSystemDataStore(object):
    """
    A class for interacting with the local file system
    """

    def __init__(self, **kwargs):
        pass

    def load_data(self, local_path):
        with open(local_path) as fp:
            observation_data = json.load(fp)


class CollabDataStore(object):
    """
    A class for uploading and downloading data from HBP Collaboratory storage.
    """

    def __init__(self, collab_id=None, base_folder=None, auth=None, **kwargs):
        self.collab_id = collab_id
        self.base_folder = base_folder
        self._auth = auth  # we defer authorization until needed
        self._authorized = False

    @property
    def authorized(self):
        return self._authorized

    def authorize(self, auth=None):
        if auth is None:
            auth = self._auth
        self.doc_client = ApiClient.new(auth.token)
        self._authorized = True

    def _translate_URL_to_UUID(self, path):
        """
        Can take a path such as `collab://5165/hippoCircuit_20171027-142713`
        with 5165 being the Collab ID and the latter part being the collab path,
        and translate this to the UUID on the HBP Collaboratory storage.
        """
        if not self.authorized:
            self.authorize(self._auth)
        try:
            entity = self.doc_client.get_entity_by_query(path=path)
        except Exception as e:
            print(e)
        return path

    def _translate_UUID_to_URL(self, uuid):
        """
        Can take a UUID on the HBP Collaboratory storage path and translate this
        to a path such as `collab://5165/hippoCircuit_20171027-142713` with 5165
        being the Collab ID and the latter part being the collab storage path.
        """
        if not self.authorized:
            self.authorize(self._auth)
        try:
            path = self.doc_client.get_entity_path(uuid)
        except Exception as e:
            print(e)
        return "collab:/{}".format(path)

    def upload_data(self, file_paths):
        if not self.authorized:
            self.authorize(self._auth)
        projects_in_collab = self.doc_client.list_projects(collab_id=self.collab_id,
                                                           access='write')["results"]
        assert len(projects_in_collab) == 1
        project_id = projects_in_collab[0]["uuid"]
        base_folder_id = self._make_folders(self.base_folder, parent=project_id)

        if len(file_paths) > 1:
            common_base_dir = os.path.dirname(os.path.commonprefix(file_paths))
        else:
            common_base_dir = os.path.dirname(file_paths[0])
        relative_paths = [os.path.relpath(p, common_base_dir) for p in file_paths]

        cached_folders = {}  # avoid unnecessary network calls
        for local_path, relative_path in zip(file_paths, relative_paths):

            parent = base_folder_id
            folder_path = os.path.dirname(relative_path)

            # temporary fix: all files in a single directory in Collab storage
            # if subdirs, then saved filename = `subdir1_subdir2_....subdirN_filename`
            name = ""
            if folder_path:  # if there are subdirectories...
                for subdir in folder_path.split("/"):
                    name  = name + subdir + "_"
                """
                if folder_path in cached_folders:
                    parent = cached_folders[folder_path]
                else:
                    parent = self._make_folders(folder_path, parent=parent)
                    cached_folders[folder_path] = parent
                """

            name = name + os.path.basename(relative_path)
            content_type = mimetypes.guess_type(local_path)[0]
            file_entity = self.doc_client.create_file(name, content_type, parent)
            etag = self.doc_client.upload_file_content(file_entity['uuid'],
                                                       source=local_path)

        return "collab://{}".format(self.doc_client.get_entity_path(base_folder_id))

    def _make_folders(self, folder_path, parent):
        for i, folder_name in enumerate(folder_path.split(os.path.sep)):
            folders = self.doc_client.list_folder_content(parent, entity_type="folder")["results"]
            folder_exists = False
            for f in folders:
                if folder_name in f["name"]:
                    child = f['uuid']
                    folder_exists = True
                    break
            if not folder_exists:
                child = self.doc_client.create_folder(folder_name, parent=parent)['uuid']
            parent = child
        return child

    def _download_data_content(self, remote_path):
        if not self.authorized:
            self.authorize(self._auth)
        # need to support other formats besides JSON
        if remote_path.startswith("collab:/"):
            remote_path = remote_path[len("collab:/"):]

        entity = self.doc_client.get_entity_by_query(path=remote_path)
        if entity["entity_type"] == 'file':
            etag, content = self.doc_client.download_file_content(entity["uuid"])
        else:
            raise IOError("Can only load data from individual files, not from {}".format(entity["entity_type"]))
        return content

    def download_data(self, remote_paths, local_directory="."):
        if isinstance(remote_paths, str):
            remote_paths = [remote_paths]
        local_paths = []
        for remote_path in remote_paths:
            local_path = os.path.join(local_directory, os.path.basename(remote_path))
            Path(os.path.dirname(local_path)).mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as fp:
                fp.write(self._download_data_content(remote_path))
            local_paths.append(local_path)
        return local_paths

    def download_data_using_uuid(self, uuid, local_directory="."):
        """
        Downloads the resource specified by the UUID on the HBP Collaboratory.
        Target can be a file or a folder. Returns a list containing absolute
        filepaths of all downloaded files.
        """
        file_uuids = []

        if not self.authorized:
            self.authorize(self._auth)
        entity = self.doc_client.get_entity_details(uuid)
        if entity["entity_type"] == 'file':
            file_uuids.append(uuid)
        elif entity["entity_type"] == 'folder':
            items = self.doc_client.list_folder_content(uuid)["results"]
            for item in items:
                file_uuids.extend(self.download_data_using_uuid(item["uuid"], local_directory=os.path.join(local_directory, entity["name"])))
            return file_uuids
        else:
            raise Exception("Downloading of resources currently supported only for files and folders!")

        remote_paths = []
        local_paths = []
        for uuid in file_uuids:
            remote_paths.append(self._translate_UUID_to_URL(uuid))
        local_paths.extend(self.download_data(remote_paths=remote_paths, local_directory=local_directory))
        return local_paths

    def load_data(self, remote_path):
        content = self._download_data_content(remote_path)
        content_type = mimetypes.guess_type(remote_path)[0]
        if content_type == "application/json":
            return json.loads(content)
        else:
            return content


class HTTPDataStore(object):
    """
    A class for downloading data from the web.
    """

    def __init__(self, **kwargs):
        pass

    def upload_data(self, file_paths):
        raise NotImplementedError("The HTTPDataStore does not support uploading data.")

    def download_data(self, remote_paths, local_directory="."):
        local_paths = []
        for url in remote_paths:
            local_path = os.path.join(local_directory, os.path.basename(urlparse(url).path))
            filename, headers = urlretrieve(url, local_path)
            local_paths.append(filename)
        return local_paths

    def load_data(self, remote_path):
        content_type, encoding = mimetypes.guess_type(remote_path)
        if content_type == "application/json":
            return requests.get(remote_path).json()
        else:
            local_paths = self.download_data([remote_path])
            return local_paths[0]


URI_SCHEME_MAP = {
    "collab": CollabDataStore,
    "http": HTTPDataStore,
    "https": HTTPDataStore
}
