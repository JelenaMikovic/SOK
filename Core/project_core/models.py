from django.db import models

class Graph(models.Model):
    root=models.OneToOneField('Node', on_delete=models.CASCADE, related_name='tree', blank=True, null=True, default=None)

class Node(models.Model):
    attributes=models.TextField()
    graph=models.ForeignKey(Graph,  on_delete=models.CASCADE, related_name='nodes')

class Edge(models.Model):
    is_directed=models.BooleanField(False)
    source=models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_outgoing')
    destination=models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_incoming')
    graph=models.ForeignKey(Graph,  on_delete=models.CASCADE, related_name='edges')
    





