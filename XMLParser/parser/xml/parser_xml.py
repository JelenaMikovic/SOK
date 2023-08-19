import json
import xml.etree.ElementTree as ET
import os
from project_core.models import Graph, Node, Edge
from project_core.services.loader import Parser

def get_absolute_path(file_path):
    return os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "files", file_path)

def parse_xml(file):

    graph = Graph.objects.create()
    root = None
    nodes_dict = {}
    tree = ET.parse(file)
    root = tree.getroot()

    attrib = {}
    for key, value in root.attrib.items():
        attrib[key] = value

    attrib["name"] = root.tag
    if root.text and root.text.strip() != "":
        attrib["text"] = root.text.strip()

    root_node = Node.objects.create(attributes=json.dumps(attrib), graph=graph)
    nodes_dict[root] = root_node

    for child in root:
        parse_element(child, root_node, graph, nodes_dict)

    graph.root = root_node
    graph.save()
    return graph

def parse_element(element, parent_node, graph, nodes_dict):

    attrib = {}
    for key, value in element.attrib.items():
        attrib[key] = value

    attrib["name"] = element.tag
    if element.text and element.text.strip() != "":
        attrib["text"] = element.text.strip()

    node = Node.objects.create(attributes=json.dumps(attrib), graph=graph)
    nodes_dict[element] = node

    Edge.objects.create(is_directed=False, source=parent_node, destination=node, graph=graph)

    for child in element:
        parse_element(child, node, graph, nodes_dict)

class XMLParser(Parser):

    def identifier(self):
        return "xml_parser"

    def name(self):
        return "Loading source from xml file and parsing it to a graph"

    def load(self, file_path):
        absolute_path = get_absolute_path(file_path)
        self.__save_to_graph(absolute_path)

    def __save_to_graph(self, source):
        parse_xml(source)
    