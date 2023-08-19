import os
import json
from collections.abc import ValuesView

from project_core.models import Graph, Node, Edge
from project_core.services.loader import Parser

def get_absolute_path(file_path):
    return os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "files", file_path)

def load_source(file_path):
    file = open(file_path)
    source = json.load(file)
    file.close() 
    return source


def create_dict_from_node(node):
    if type(node) == str:
        return {'key':node}
    values = {}
    if len(node) == 1:
        for key, value in node.items():
            if type(value) == list:
                values['list_name'] = key
            else:
                values[key] = value
    else:
        for key, value in node.items():
            if type(value) != list and type(value) != dict:
                values[key] = value
    if values == {}:
        return json.dumps({'collection':'collection'})
    return json.dumps(values)

def traverse(child, node_to_compare, source_nodes, edges):
    if child is None:
        for _, value in node_to_compare.items():
            if type(value) == list or type(value) == dict:
                traverse(value, node_to_compare, source_nodes, edges)

    elif type(child) == dict:

        exists = False
        for node in source_nodes:
            if child.items() <= node.items():
                exists = True
                if (node, node_to_compare) not in edges and (node_to_compare, node) not in edges:
                    edges.append((node_to_compare, node))
                    traverse(child.items(), child, source_nodes, edges)
        if exists is False and child not in source_nodes:
            if child != '{}':
                source_nodes.append(child)
            if child != '{}' and node_to_compare != '{}':
                edges.append((node_to_compare, child))
    elif type(child) == list:

        for item in child:
            if type(item) != str:
                traverse(item, node_to_compare, source_nodes, edges)
            else:
                if (node_to_compare, item) not in edges and (item, node_to_compare) not in edges:
                    edges.append((node_to_compare, item))

    elif isinstance(child, ValuesView):
        source_nodes.append(child)
        if (child, node_to_compare) not in edges and (node_to_compare, child) not in edges:
            edges.append((node_to_compare, child))
    else:
        return


def save_edges(graph, new_edges):
    nodes = Node.objects.all()
    for i in range(0, len(nodes) - 1):
        for j in range(i, len(nodes)):
            for (my_source, destination) in new_edges:

                first_node_value = nodes[i].attributes
                second_node_value = nodes[j].attributes
                if first_node_value == my_source and second_node_value == destination:
                    edge = Edge(is_directed=False, source=nodes[i], destination=nodes[j], graph=graph)
                    edge.save()
                    break
                elif second_node_value == my_source and first_node_value == destination:
                    edge = Edge(is_directed=False, source=nodes[j], destination=nodes[i], graph=graph)
                    edge.save()
                    break


def save_nodes(graph, source_nodes):
    for node in source_nodes:
        new_node = Node(attributes=create_dict_from_node(node), graph=graph)

        new_node.save()


class JsonParser(Parser):
    def identifier(self):
        return "json_parser"

    def name(self):
        return "Loading source from json file and parsing it to a graph"

    def load(self, file_path):
        absolute_path = get_absolute_path(file_path)
        source = load_source(absolute_path)
        self.__save_to_graph(source)

    def __traverse_source(self, source, source_nodes):
        if isinstance(source, dict):
            source_nodes.append(source)
            self.__traverse_source(source.values(), source_nodes)

        elif isinstance(source, list):
            for item in source:
                source_nodes.append(item)
        
        elif isinstance(source, ValuesView):
            for value in source:
                self.__traverse_source(value, source_nodes)

    def __save_to_graph(self, source):
        graph = Graph()
        graph.save()
        source_nodes = []
        edges = []
        self.__traverse_source(source, source_nodes)

        for node in source_nodes:
            traverse(None, node, source_nodes, edges)

        save_nodes(graph, source_nodes)

        new_edges = []
        for (source, destination) in edges:
            new_edges.append((create_dict_from_node(source), create_dict_from_node(destination)))

        save_edges(graph, new_edges)
