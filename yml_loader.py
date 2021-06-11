from typing import List
import pprint

import yaml
from yaml import safe_load, ScalarNode


class ConcatTag(yaml.YAMLObject):
    """
    This class is responsible for loading concat tags from yaml and processing them.

    Attributes:
        value (str): a concatinated string
    """
    yaml_tag = u'!concat'

    def __init__(self, param_list: List[ScalarNode]) -> None:
        """
        The constructor for the ConcatTag class.

        @param param_list:
        """
        self.value = self._process_inputs(input_list=param_list)

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def _process_inputs(input_list: List[ScalarNode]) -> str:
        """
        Takes the list of inputs and concats them to a string.

        @param input_list: (List[ScalarNode]) a list of values that have been passed in
        @return: (str) a string consisting of all the parameters passed in
        """
        buffer: List = []
        for node in input_list:
            buffer.append(node.value)
        return "".join(buffer)

    @classmethod
    def from_yaml(cls, loader, node):
        return ConcatTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.value)


# Required for safe_load
yaml.SafeLoader.add_constructor('!concat', ConcatTag.from_yaml)
# Required for safe_dump
yaml.SafeDumper.add_multi_representer(ConcatTag, ConcatTag.to_yaml)


if __name__ == "__main__":
    with open("./example.yml") as f:
        data = safe_load(f.read())
    print("This is the file path: ", data["step_definition"]["peril"]["parameters"]["file_path"])
    pprint.pprint(data)
