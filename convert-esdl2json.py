#!/usr/bin/env python

from argparse import ArgumentParser
from datetime import datetime
import json

from esdl.esdl_handler import EnergySystemHandler
from pyecore.resources.json import JsonResource


class JSONEncoderDT(json.JSONEncoder):
    def default(self, obj):
        match obj:
            case datetime():
                return obj.isoformat()
        return super().default(obj)


class JsonResourceDT(JsonResource):
    """FIXME: hack to serialise datetime objects by overriding save"""

    def save(self, output=None, options=None):
        self.options = options or {}
        stream = self.open_out_stream(output)
        dict_list = []
        for root in self.contents:
            dict_list.append(self.to_dict(root))
        if len(dict_list) <= 1:
            dict_list = dict_list[0]

        stream.write(
            json.dumps(dict_list, indent=self.indent, cls=JSONEncoderDT).encode("utf-8")
        )
        stream.flush()
        self.uri.close_stream()
        self.options = None


def convert(esdl_file: str):
    esh = EnergySystemHandler()
    esh.create_empty_energy_system(name="Test")
    esh.load_file(esdl_file)
    esh.rset.resource_factory["json"] = lambda uri: JsonResourceDT(uri)

    json_file = esdl_file.replace(".esdl", ".json")
    esh.save(json_file)
    print(f"{esdl_file} -> {json_file}")

    return esh


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("esdl_file")
    opts = parser.parse_args()
    esh = convert(opts.esdl_file)
