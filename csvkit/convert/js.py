#!/usr/bin/env python

try:
    from collections import OrderedDict
    import json
except ImportError:
    from ordereddict import OrderedDict
    import simplejson as json

import agate
import six


def parse_object(obj, path=''):
    """
    Recursively parse JSON objects and a dictionary of paths/keys and values.

    Inspired by JSONPipe (https://github.com/dvxhouse/jsonpipe).
    """
    if isinstance(obj, dict):
        iterator = obj.items()
    elif isinstance(obj, (list, tuple)):
        iterator = enumerate(obj)
    else:
        return {path.strip('/'): obj}

    d = OrderedDict()

    for key, value in iterator:
        key = six.text_type(key)
        d.update(parse_object(value, path + key + '/'))

    return d


def json2csv(f, key=None, **kwargs):
    """
    Convert a JSON document into CSV format.

    The top-level element of the input must be a list or a dictionary. If it is a dictionary, a key must be provided which is an item of the dictionary which contains a list.
    """
    js = json.load(f, object_pairs_hook=OrderedDict)

    if isinstance(js, dict):
        if not key:
            raise TypeError('When converting a JSON document with a top-level dictionary element, a key must be specified.')

        js = js[key]

    fields = []
    flat = []

    for obj in js:
        parsed_object = parse_object(obj)
        flat.append(parsed_object)

        for key in parsed_object.keys():
            if key not in fields:
                fields.append(key)

    o = six.StringIO()
    writer = agate.writer(o)

    writer.writerow(fields)

    for i in flat:
        row = []

        for field in fields:
            row.append(i.get(field, None))

        writer.writerow(row)

    output = o.getvalue()
    o.close()

    return output
