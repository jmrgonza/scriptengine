import pkg_resources
import logging
import functools

from scriptengine.exceptions import ScriptEngineTaskLoaderError


# The load function goest through entry points, searching for ScriptEngine
# tasks. Since the function can be called quite frequently and modules are
# *usually* not loaded while SE is run, the result is cached.
# Note that this means that dynamic module is *not supported* by the loading
# mechanism!
@functools.lru_cache(maxsize=None)
def load():

    entry_point = 'scriptengine.tasks'

    loaded_tasks = dict()
    for ep in pkg_resources.iter_entry_points(entry_point):
        if ep.name not in loaded_tasks:
            loaded_tasks[ep.name] = ep.load()
        else:
            clash = next(clash_ep.module_name
                         for clash_ep
                         in pkg_resources.iter_entry_points(entry_point)
                         if clash_ep.name == ep.name)
            msg = f'Same task name "{ep.name}" defined in modules ' \
                  f'"{ep.module_name}" and "{clash}"'
            logging.getLogger('se.task').error(msg, extra={'id': 'loader'})
            raise ScriptEngineTaskLoaderError(msg)

    return loaded_tasks