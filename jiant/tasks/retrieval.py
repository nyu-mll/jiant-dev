import os

from jiant.tasks.lib.cola import ColaTask
from jiant.tasks.lib.mnli import MnliTask
from jiant.tasks.lib.mrpc import MrpcTask
from jiant.tasks.lib.qqp import QqpTask
from jiant.tasks.lib.qnli import QnliTask
from jiant.tasks.lib.rte import RteTask
from jiant.tasks.lib.snli import SnliTask
from jiant.tasks.lib.sst import SstTask
from jiant.tasks.lib.stsb import StsbTask
from jiant.tasks.lib.wnli import WnliTask
from jiant.tasks.core import Task
from jiant.utils.python.io import read_json


TASK_DICT = {
    "cola": ColaTask,
    "mnli": MnliTask,
    "mrpc": MrpcTask,
    "qnli": QnliTask,
    "qqp": QqpTask,
    "rte": RteTask,
    "snli": SnliTask,
    "sst": SstTask,
    "stsb": StsbTask,
    "wnli": WnliTask,
}


def get_task(task_name, data_dir):
    task_name = task_name.lower()
    task_class = TASK_DICT[task_name]
    return task_class(task_name, data_dir)


def get_task_class(task_name):
    task_class = TASK_DICT[task_name]
    assert issubclass(task_class, Task)
    return task_class


def create_task_from_config(config: dict, base_path=None, verbose=False):
    task_class = get_task_class(config["task"])
    for k in config["paths"].keys():
        path = config["paths"][k]
        # Todo: Refactor paths
        if isinstance(path, str) and not os.path.isabs(path):
            assert base_path
            config["paths"][k] = os.path.join(base_path, path)
    task_kwargs = config.get("kwargs", {})
    if verbose:
        print(task_class.__name__)
        for k, v in config["paths"].items():
            print(f"  [{k}]: {v}")
    # noinspection PyArgumentList
    return task_class(name=config["name"], path_dict=config["paths"], **task_kwargs)


def create_task_from_config_path(config_path: str, verbose=False):
    return create_task_from_config(
        read_json(config_path),
        base_path=os.path.split(config_path)[0],
        verbose=verbose,
    )