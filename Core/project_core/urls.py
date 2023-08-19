from django.urls import path

from . import views

urlpatterns = [
    path('visualization/<str:id>', views.visualization, name="visualization"),
    path('tree', views.getTreeRoots, name="tree"),
    path('getTreeNode/<int:nodeId>', views.getTreeNode, name="treeNodeDetails"),
    path('visualizationChange/<str:id>/<str:query>', views.visualizationChange, name="visualizationChange"),
    path('visualizationSearch/<str:id>/<str:query>', views.visualizationSearch, name="visualizationSearch"),
    path('', views.home, name="simple"),
    path('parser/<str:id>/<str:filename>', views.parser, name="parser"),

]