# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json


def _compute_path(base_dir, element):
    if isinstance(element, str):
        return os.path.normpath(os.path.join(base_dir, element))
    elif isinstance(element, list):
        for e in element:
            if not isinstance(e, str):
                raise ValueError("file path must be a string.")
        return [os.path.normpath(os.path.join(base_dir, e)) for e in element]
    else:
        raise ValueError("file path must be a string or a list of string.")


def _append_paths(base_dir, is_segmentation, items):
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("data item must be dict.")
        for k, v in item.items():
            if k == "image":
                item[k] = _compute_path(base_dir, v)
            elif is_segmentation and k == "label":
                item[k] = _compute_path(base_dir, v)
    return items


def load_decathalon_datalist(data_list_file_path, is_segmentation=True, data_list_key="training", base_dir=None):
    """Load image/label paths of decathalon challenge from JSON file

    Json file is similar to what you get from http://medicaldecathlon.com/
    Those dataset.json files

    Args:
        data_list_file_path (str): the path to the json file of datalist
        is_segmentation (bool): whether the datalist is for segmentation task, default is True
        data_list_key (str): the key to get a list of dictionary to be used, default is "training"
        base_dir (str): the base directory of the dataset, if None, use the datalist directory

    Returns a list of data items, each of which is a dict keyed by element names, for example:

    .. code-block::

        [
            {'image': '/workspace/data/chest_19.nii.gz',  'label': 0}, 
            {'image': '/workspace/data/chest_31.nii.gz',  'label': 1}
        ]

    """
    if not os.path.isfile(data_list_file_path):
        raise ValueError(f"data list file {data_list_file_path} does not exist.")
    with open(data_list_file_path) as json_file:
        json_data = json.load(json_file)
    if data_list_key not in json_data:
        raise ValueError(f"data list {data_list_key} not specified in '{data_list_file_path}'.")
    expected_data = json_data[data_list_key]
    if data_list_key == "test":
        expected_data = [{"image": i} for i in expected_data]

    if base_dir is None:
        base_dir = os.path.dirname(data_list_file_path)

    return _append_paths(base_dir, is_segmentation, expected_data)
