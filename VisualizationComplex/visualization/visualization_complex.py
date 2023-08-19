from abc import abstractclassmethod
import json
import random
from django.template.loader import render_to_string
from project_core.models import Graph, Node, Edge
from project_core.services.loader import Visualization

class VisualizationComplex(Visualization):

    def name(self):
        return "Visualize simple representation of the graph."

    def identifier(self):
        return "visualization_complex"

    def display(self,graph=None):
        # Retrieve the graph object
    
        if graph == None :
            graph = Graph.objects.last()

        # Retrieve the nodes and edges for the graph
        nodes = Node.objects.filter(graph=graph)
        edges = Edge.objects.filter(graph=graph)

        # Pass the data to the template
        context = {
            'graph': json.dumps(self.graph_to_dict(graph)),
            'nodes': json.dumps([node.id for node in nodes]),
            'edges': json.dumps([edge.id for edge in edges]),
        }

        return render_to_string('visualization_complex.html', context)


    def graph_to_dict(self,graph):
        root = graph.root
        print(root)
        if (not graph.root) :
            root ='none'
        else:
            root = graph.root.id
        print(root)
        print(graph.nodes.all())
        return {
            'id': graph.id,
            'root': root,
            'nodes': [{'name': node.id, 'attributes': node.attributes} for node in graph.nodes.all()],
            'edges': [{'source': edge.source.id, 'target': edge.destination.id} for edge in graph.edges.all()],
    }