import pkg_resources
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'project_core'
    plugins_parse = []
    plugins_visualization = []

    def ready(self):
        self.plugins_parse = load_plugins("parse.load")
        self.plugins_visualization = load_plugins("visualization.display")
        


def load_plugins(group_tag):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=group_tag):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        print(group_tag)
        plugin = p()
        plugins.append(plugin)
    return plugins

