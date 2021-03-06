from django.forms.widgets import Widget

# @serializable(GenericObjectSerializer(), serialize_method_name='render')
# class SingleValueInput(object):
#     def __init__(self, name, widget_type, values, *args, **kwargs):
#         self.name = name
#         self.type = widget_type
#         self.values = values
#
#     def get_value(self, data_dict):
#         assert self.name is not None
#         out_name = u'{0}_out'.format
#         value = data_dict.get(out_name(self.name), None)
#         return value


class SingleValueInput(Widget):
    def __init__(self, type, values):
        self.values = values
        self.type = type
        super(SingleValueInput, self).__init__()

    def render(self, name, value, attrs=None, choices=()):
        return {'name': name,
                'type': self.type,
                'values': self.values}

    def value_from_datadict(self, data, files, name):
        out_name = u'{0}_out'.format(name)
        value = data.get(out_name, None)
        return value


class DoubleValueInput(Widget):
    def __init__(self, type, values, suffixes):
        self.values = values
        self.suffixes = suffixes
        self.type = type
        super(DoubleValueInput, self).__init__()

    def render(self, name, value, attrs=None, choices=()):
        return {'name': name,
                'suffixes': self.suffixes,
                'type': self.type,
                'values': self.values}

    def value_from_datadict(self, data, files, name):
        out_name = lambda s: u'{0}_{1}'.format(name, s)
        val1 = data.get(out_name(self.suffixes[0]), None)
        val2 = data.get(out_name(self.suffixes[1]), None)
        return val1, val2

# @serializable(GenericObjectSerializer(), serialize_method_name='render')
# class DoubleValueInput(object):
#     def __init__(self, name, widget_type, suffix_one, suffix_two, values, *args, **kwargs):
#         self.name = name
#         self.suffixes = suffix_one, suffix_two
#         self.type = widget_type
#         self.values = values
#
#     def get_value(self, data_dict):
#         assert self.name is not None
#         out_name = lambda s: u'{0}_{1}'.format(self.name, s)
#         val1 = data_dict.get(out_name(self.suffixes[0]), None)
#         val2 = data_dict.get(out_name(self.suffixes[1]), None)
#         return val1, val2


