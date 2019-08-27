"""Configuration task for ScriptEngine."""

from se.tasks import Task
from se.helpers import render_string

from deepmerge import always_merger


class Configuration(Task):
    """Configuration task, sets configuration parameters.

    The tasks run() method returns all name-value pairs passed at creation time
    in a dict.
    """
    def __init__(self, parameters):
        super().__init__(__name__, parameters)

    def __str__(self):
        return f"Configuration: {self.__dict__}"

    def run(self, context):
        parameters = {key: value for key, value in self.__dict__.items() if key[0]!="_"}
        self.log_info(f"{parameters}")
        always_merger.merge(context, parameters)
