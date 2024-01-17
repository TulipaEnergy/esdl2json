#!/usr/bin/env python

from argparse import ArgumentParser

from esdl.esdl_handler import EnergySystemHandler
from pyecore.resources.json import JsonResource


def convert(esdl_file: str):
    esh = EnergySystemHandler()
    esh.create_empty_energy_system(name="Test")
    esh.load_file(esdl_file)
    esh.rset.resource_factory["json"] = lambda uri: JsonResource(uri)

    json_file = esdl_file.replace(".esdl", ".json")
    esh.save(json_file)
    print(f"{esdl_file} -> {json_file}")

    return esh


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("esdl_file")
    opts = parser.parse_args()
    esh = convert(opts.esdl_file)
