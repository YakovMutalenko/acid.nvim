import types
from acid.nvim.log import log_warning, log_debug

def transform_meta(transform):
    if isinstance(transform, types.FunctionType):
        return transform.__code__.co_varnames
    return ('this', )


def doc_transform(definition):
    "Takes a definition of msg->doc and returns a fn that transforms it."
    def print_doc(msg):
        outcome = {}
        lines = []
        for key, value in definition['data'].items():
            log_debug("Working with key {}", key)
            if 'default' in value:
                obj = msg.get(key, value['default'])
            else:
                obj = msg[key]

            if obj:
                if 'transform' in value:
                    this, *other = transform_meta(value['transform'])
                    obj = value['transform'](obj, *[outcome[i] for i in other])

                if 'prepend' in value:
                    prepend = value['prepend']
                    if type(obj) == list:
                        obj = [prepend, *obj]
                    else:
                        obj = '{} {}'.format(prepend, obj)

                if 'rename' in value:
                    key = value['rename']
                outcome[key] = obj

        log_debug("current data: {}", outcome)

        for key in definition['format']:
            if type(key) == list and lines[-1] != '':
                lines.append('')
            elif key in outcome:
                obj = outcome[key]
                if obj:
                    obj_type = type(obj)
                    if obj_type == str:
                        lines.append(obj)
                    elif obj_type == list:
                        lines = [*lines, *obj]
                    else:
                        log_warning('Unknown obj type, skipping.')
        return lines
    return print_doc
