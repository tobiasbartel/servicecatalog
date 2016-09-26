from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import datetime
from models import *
from pprint import pprint
import pydotplus
import re
import graphgenerator

def index(request):
    all_module = Module.objects.all().order_by('name')
    all_instances = Instance.objects.all().order_by('name')

    my_graph = all_module_graph(request, raw=True)

    return render_to_response('servicecatalog/index.html', {'modules':all_module, 'instances': all_instances, 'my_graph': my_graph})

def module_overview(request, module_name):
    all_module = Module.objects.all().order_by('name')
    all_instances = Instance.objects.all().order_by('name')
    my_module = Module.objects.get(slug=module_name)
    my_graph = module_graph(request=request, module_name=module_name, raw=True)
    return render_to_response('servicecatalog/module.html', {'my_module': my_module, 'my_graph':my_graph, 'modules':all_module, 'instances': all_instances})

def instance_overview(request, instance_name):
    all_module = Module.objects.all().order_by('name')
    all_instances = Instance.objects.all().order_by('name')
    my_instance = Instance.objects.get(slug=instance_name)
    my_graph = instance_graph(request=request, instance_name=instance_name, raw=True)
    return render_to_response('servicecatalog/instance.html', {'my_instance': my_instance, 'my_graph':my_graph, 'modules':all_module, 'instances': all_instances})

def module_graph(request, module_name, raw=False):
    my_graph = graphgenerator.module(module_name)

    if raw:
        return my_graph
    else:
        response = HttpResponse(my_graph, content_type='image/svg+xml')
        response['Content-Length'] = len(my_graph)
        return response




def instance_graph(request, instance_name, raw=False):
    my_graph = graphgenerator.instance(instance_name)

    if raw:
        return my_graph
    else:
        response = HttpResponse(my_graph, content_type='image/svg+xml')
        response['Content-Length'] = len(my_graph)
        return response


def all_module_graph(request, raw=False):
    all_modules = Module.objects.all()

    graph = pydotplus.Dot(graph_type='digraph')
    node = pydotplus.Node()
    node.set_name('The Interweb')
    node.set('shape', 'box')
    graph.add_node(node)

    for my_module in all_modules:
        node = pydotplus.Node()
        node.set('shape', 'box')
        node.set_name(my_module.__unicode__())
        node.set('URL', '/module/%s/' % my_module.slug)
        graph.add_node(node)
        if my_module.customer_facing:
            edge = pydotplus.Edge('The Interweb', my_module.__unicode__())
            graph.add_edge(edge)

        for dependency in my_module.depending_on.iterator():
            node = pydotplus.Node()
            node.set('shape', 'box')
            node.set_name(dependency.__unicode__())
            node.set('URL', '/module/%s/' % dependency.slug)
            edge = pydotplus.Edge(my_module.__unicode__(), dependency.__unicode__())
            graph.add_node(node)
            graph.add_edge(edge)
            #if dependency.customer_facing:
            #    edge = pydotplus.Edge('The Interweb', dependency.__unicode__())
            #    graph.add_edge(edge)

    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph )
    my_graph = re.sub(r"( height=)", " min-height=", my_graph )

    if raw:
        return my_graph
    else:
        response = HttpResponse(my_graph, content_type='image/svg+xml')
        response['Content-Length'] = len(my_graph)
        return response