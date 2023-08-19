from collections import defaultdict
from project_core.models import Graph,Node,Edge
from django.apps.registry import apps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
import ast
import json
from .models import Graph, Node, Edge

def visualizationChange(request,id,query):
    plugins = apps.get_app_config('project_core').plugins_visualization
    request.session['plugin'] = id

    graph = Graph.objects.last()
    subgraph = filteredGraph(graph,query)
    
    for plugin in plugins :
        if plugin.identifier() == id:
            graph = plugin.display(subgraph)
    context = {}
    context['graph'] = graph
    context['plugins'] = plugins
    
    return HttpResponse(graph)

def visualization(request,id):

    plugins = apps.get_app_config('project_core').plugins_visualization
    request.session['plugin'] = id
    
    graph = ""
    for plugin in plugins :
        if plugin.identifier() == id:
            graph = plugin.display()
    print(graph)
    context = {}
    context['graph'] = graph
    context['plugins'] = plugins
    
    return HttpResponse(graph)

def home(request):
    plugins = apps.get_app_config('project_core').plugins_visualization
    pluginsP = apps.get_app_config('project_core').plugins_parse
    files = ["source.xml", "android.xml", "foodmenu.xml", "cds.xml", "source.json", "employees.json", "products.json", "rides.json"]
    context = {'plugins': plugins, 'files' : files}
    context['pluginsP'] = pluginsP
    return render(request, 'index.html', context=context)
    
    
def parser(request, id, filename):
    Graph.objects.all().delete()
    Edge.objects.all().delete()
    Node.objects.all().delete()
    plugins = apps.get_app_config('project_core').plugins_parse
    request.session['plugin'] = id

    graph = ""
    for plugin in plugins:
        if plugin.identifier() == id:
            plugin.load(filename)
    return render(request, 'graph.html', context={})


def get_subgraph(graph,attr_key,comp,attr_value):
    nodes = get_nodes_with_attribute(graph, attr_key,attr_value,comp)
    new_graph = Graph.objects.create()
    new_nodes = [Node.objects.create(attributes=node.attributes, graph=new_graph) for node in nodes]
    new_edges = []
    for node in nodes:
        node_edges = Edge.objects.filter(source=node)
        for edge in node_edges:
            indexs = nodes.index(edge.source)
            if edge.destination in nodes:
                index = nodes.index(edge.destination)
                new_destination = new_nodes[index]
                Edge.objects.create(is_directed=edge.is_directed, source=new_nodes[indexs], destination=new_destination, graph=new_graph)
    return new_graph

def get_nodes_with_attribute(graph, attr_key, attr_value,attr_comp):
    print(attr_key, attr_value,attr_comp)
    nodes = graph.nodes.all()
    result = []
    for node in nodes:
        print(node.attributes)
        attributes = json.loads(node.attributes)
        if attr_comp == "==" :
            if attr_key in attributes and attributes[attr_key] == attr_value:
                print(attr_comp)
                result.append(node)
        if attr_comp == ">=" :
            if attr_key in attributes and attributes[attr_key] >= attr_value:
                result.append(node)
        if attr_comp == "<=" :
            if attr_key in attributes and attributes[attr_key] <= attr_value:
                result.append(node)
        if attr_comp == ">" :
            if attr_key in attributes and attributes[attr_key] > attr_value:
                result.append(node)
        if attr_comp == "<" :
            if attr_key in attributes and attributes[attr_key] < attr_value:
                result.append(node)
        if attr_comp == "!=" :
            if attr_key in attributes and attributes[attr_key] != attr_value:
                result.append(node)
    print(result)
    return result

def filteredGraph(graph,query):
    print("query",query)
    args = query.split(" ")
    if args[2].lower() == 'true':
        args[2] = 1
    elif args[2].lower() == 'false':
        args[2] = 0
    else:
        try:
            args[2] = int(args[2])
        except ValueError:
            args[2] = args[2]
    return get_subgraph(graph,args[0],args[1],args[2])

def visualizationSearch(request,id,query):
    plugins = apps.get_app_config('project_core').plugins_visualization
    request.session['plugin'] = id

    graph = Graph.objects.last()
    subgraph = get_sub_graph_query(graph, query)
    
    for plugin in plugins :
        if plugin.identifier() == id:
            graph = plugin.display(subgraph)
    context = {}
    context['graph'] = graph
    context['plugins'] = plugins
    
    return HttpResponse(graph)

def get_sub_graph_query(graph, word):
    
    sub_graph = Graph.objects.create()
    nodes = Node.objects.filter(Q(attributes__contains=word) | Q(attributes__icontains=word), graph=graph)
    new_nodes = []

    for node in nodes:
        newNode = Node.objects.create(attributes=node.attributes, graph=sub_graph)
        newNode.save()
        new_nodes.append(newNode)

    for edge in Edge.objects.filter(graph=graph):
        if edge.source in nodes and edge.destination in nodes:
            source_node = next(new_node for new_node in new_nodes if new_node.attributes == edge.source.attributes)
            destination_node = next(new_node for new_node in new_nodes if new_node.attributes == edge.destination.attributes)
            newEdge = Edge.objects.create(source=source_node, destination=destination_node, graph=sub_graph,is_directed=edge.is_directed)
            newEdge.save()

    in_degree = defaultdict(int)
    for edge in  Edge.objects.filter(graph=sub_graph):
        in_degree[edge.destination.id] += 1
        
    root = None
    for node in Node.objects.filter(graph=sub_graph):
        if in_degree[node.id] == 0:
            if root:
                return sub_graph
            else:
                root = node
    if root:
        sub_graph.root = root
        sub_graph.save()

    return sub_graph

def getTreeRoots(request):
    graph = Graph.objects.last()
    print("EVO")
    print(graph)
    print("EVO")

    subgraphs = []

    print("\n\n\n\n\n\n\n")
    if (graph.root is not None):
        print("ROOT")
        subgraphs.append(displayTreeNode(graph, graph.root))
    else:
        roots = getGraphRoots(graph)
        if len(roots) == 0:
            print("SVI POVEZANI, EVO GA PRVI:")
            print(Node.objects.first())
            subgraphs.append(displayTreeNode(graph, Node.objects.first()))
        else:
            print("IMA VISE KORENA:" + str(len(roots)) + "\n")
            for root in roots:
                subgraphs.append(displayTreeNode(graph, root))
    
    print("\n\n\n\n\n\n\n*********************************************************")
    print(subgraphs)
    print("\n\n\n\n\n\n\n*********************************************************")
    return render(request, 'tree_view.html', context={'subgraphs': subgraphs})

def displayTreeNode(graph, node: Node):
    print("\nkoren:")
    children = []
    attributes = json.loads(node.attributes)
    for node in getDestinationNodes(graph, node):
        print(node)
        children.append(node.id)
    
    return TreeNode(node.id, True, attributes, children)

def getTreeNode(request, nodeId: int):
    graph = Graph.objects.last()
    node = Node.objects.get(id=nodeId)
    return HttpResponse(json.dumps(displayTreeNode(graph, node).to_dict()), content_type='application/json')

def getDestinationNodes(graph, node):
    edges = Edge.objects.filter(source=node, graph=graph)
    destination_nodes = [edge.destination for edge in edges]
    return destination_nodes

# nodes that are never destination nodes == 'roots'
def getGraphRoots(graph):
    all_nodes = Node.objects.filter(graph=graph)
    destination_nodes =  Node.objects.filter(edges_incoming__isnull=False).distinct()
    never_destination_nodes = all_nodes.exclude(pk__in=destination_nodes)
    return never_destination_nodes


class TreeNode():
    def __init__(self, id, is_root, attributes, children):
        self.id = id
        self.is_root = is_root
        self.attributes = attributes
        self.children = children
    
    def from_node(self, node: Node, is_root, children):
        self.id = node.id
        self.is_root = is_root
        self.attributes = node.attributes
        self.children = children

    def to_dict(self):
        return {
            'id': self.id,
            'is_root': self.is_root,
            'attributes': self.attributes,
            'children': self.children
        }

    def __str__(self) -> str:
        return str(self.id) + " " + str(self.is_root) + " " + str(self.attributes) + str(self.children)


