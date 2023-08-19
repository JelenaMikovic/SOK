from abc import abstractclassmethod
import json
import random
from django.template.loader import render_to_string
from project_core.models import Graph, Node, Edge
from project_core.services.loader import Visualization
import ast

class VisualizationSimple(Visualization):

    def name(self):
        return "Visualize simple representation of the graph."

    def identifier(self):
        return "visualization_simple"

    def display(self,graph=None):
        if graph == None :
            graph = Graph.objects.last()
        nodes = Node.objects.filter(graph=graph)
        edges = Edge.objects.filter(graph=graph)

        # Pass the data to the template
        context = {
            'graph': json.dumps(self.graph_to_dict(graph)),
            'nodes': json.dumps([node.id for node in nodes]),
            'edges': json.dumps([edge.id for edge in edges]),
        }

        return render_to_string('visualization_simple.html', context)

    def random_graph_view(self): 
        # Create a new graph object
        graph = Graph.objects.create()

        # Create some random nodes
        for i in range(10):
            node = Node.objects.create(attributes={'x': random.randint(0, 800), 'y': random.randint(0, 600), 'size': random.randint(5, 20)}, graph=graph)

        # Create some random edges
        for i in range(20):
            source = Node.objects.get(id=random.randint(1, 10))
            destination = Node.objects.get(id=random.randint(1, 10))
            while destination == source:
                destination = Node.objects.get(id=random.randint(1, 10))
            Edge.objects.create(source=source, destination=destination, graph=graph,is_directed=random.choice([True, False]))

        graph.save()
        return graph

    def graph_to_dict(self,graph):
        root = graph.root
        print(root)
        if (not graph.root) :
            root ='none'
        else:
            root = graph.root.id
        print(root)
        return {
            'id': graph.id,
            'root': root,
            'nodes': [{'name': self.getNodeName(node) , 'id' : node.id ,'attributes' : json.loads(node.attributes)} for node in graph.nodes.all()],
            'edges': [{'source': edge.source.id, 'target': edge.destination.id} for edge in graph.edges.all()],
    }

    def getNodeName(self,node) :
        print(node.attributes)
        attributes = json.loads(node.attributes)
        if "name" in attributes:
                return attributes['name']
        return "⬤"