try:
    from ujson import loads as json_loads, dumps as json_dumps
except ImportError:
    from json import loads as json_loads, dumps as json_dumps
