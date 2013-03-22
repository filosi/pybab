from pyhive.decorators import serializable
from pyhive.serializers import GenericObjectSerializer

@serializable(GenericObjectSerializer(), serialize_method_name='render')
class SingleValueInput(object):
    def __init__(self, name, widget_type, values, *args, **kwargs):
        self.name = name
        self.type = widget_type
        self.values = values

    def get_value(self, data_dict):
        assert self.name is not None
        out_name = u'{0}_out'.format
        value = data_dict.get(out_name(self.name), None)
        return value

@serializable(GenericObjectSerializer(), serialize_method_name='render')
class DoubleValueInput(object):
    def __init__(self, name, widget_type, suffix_one, suffix_two, values, *args, **kwargs):
        self.name = name
        self.suffixes = suffix_one, suffix_two
        self.type = widget_type
        self.values = values

    def get_value(self, data_dict):
        assert self.name is not None
        out_name = lambda s: u'{0}_{1}'.format(self.name, s)
        val1 = data_dict.get(out_name(self.suffixes[0]), None)
        val2 = data_dict.get(out_name(self.suffixes[1]), None)
        return val1, val2
