# -*- coding: utf-8 -*-
from topology import topology
from json import load, dump


def convert(geojson, topojson, object_name=False, *args, **kwargs):
    if isinstance(geojson, dict):
        input_dict = geojson
    elif isinstance(geojson, str) or isinstance(geojson, unicode):
        inFile = open(geojson)
        input_dict = load(inFile)
        if not object_name and 'type' in input_dict and hasattr(
                inFile,
                'collection') and inFile.name.lower().endswith('.geojson'):
            input_dict = {inFile.name[:-8].split('/')[-1]: input_dict}
    elif isinstance(geojson, file):
        input_dict = load(geojson)
    #NOTE::适配从AMAP获取的行政区域geoJSON数据
    if 'type' in input_dict and input_dict['type'] == "Feature":
        input_dict = {"type": "FeatureCollection", "features": [input_dict]}
    if 'type' in input_dict:
        if object_name:
            input_dict = {object_name: input_dict}
        else:
            input_dict = {'collection': input_dict}
    output_dict = topology(input_dict, *args, **kwargs)
    if isinstance(topojson, str) or isinstance(topojson, unicode):
        with open(topojson, 'w') as f:
            dump(output_dict, f, separators=(',', ':'))#use the most compact JSON representation
    elif isinstance(topojson, file):
        dump(output_dict, topojson, separators=(',', ':'))
    else:
        return output_dict
