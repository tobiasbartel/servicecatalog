from models import *
from pprint import pprint
import pydotplus
import re

def module(module_name):

    #
    # Compile a list of modules to include in this graph
    #

    my_nodes = []
    add_the_internet = False

    my_module = Module.objects.get(slug=module_name)
    my_nodes.append(my_module)
    if my_module.customer_facing:
        add_the_internet = True

    for one_module in my_module.depending_on.iterator():
        if one_module not in my_nodes:
            my_nodes.append(one_module)
            if one_module.customer_facing is True:
                add_the_internet = True

    parent_module = Module.objects.all()
    parent_module = parent_module.filter(depending_on=my_module)
    for one_module in parent_module:
        if one_module not in my_nodes:
            my_nodes.append(one_module)

            if one_module.customer_facing:
                add_the_internet = True

    #
    # Build the graph
    #
    graph = pydotplus.Dot(graph_type='digraph')
    graph.set('splines', 'ortho')
    graph.set('newrank', True)

    if add_the_internet:
        node = pydotplus.Node()
        node.set_name('Merchant')
        node.set('shape', 'box3d')
        graph.add_node(node)

    for one_node in my_nodes:
        node = pydotplus.Node()
        node.set_name(one_node.__unicode__())
        node.set('URL', '/module/%s/' % one_node.slug)
        node.set('shape', 'component')
        if one_node is my_module:
            node.set('style', 'filled')
        graph.add_node(node)

        if one_node.customer_facing:
            edge = pydotplus.Edge('Merchant', one_node.__unicode__())
            graph.add_edge(edge)

        for dependency in one_node.depending_on.iterator():
            if dependency in my_nodes:
                 edge = pydotplus.Edge(one_node.__unicode__(), dependency.__unicode__())
                 graph.add_edge(edge)

    #
    # Workaround to make SVG responsive
    #
    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph )
    my_graph = re.sub(r"( height=)", " min-height=", my_graph )

    return my_graph


def instance(instance_name):

    #
    # Compile a list of all hardware and instances to include in this graph
    #

    my_hardware_nodes = {}
    my_instance_nodes = []
    add_the_internet = False

    my_hardware = Hardware.objects.all()
    my_hardware = my_hardware.filter(instance__slug=instance_name)

    my_instance = Instance.objects.get(slug=instance_name)



    for one in my_hardware:
        if not one.type in my_hardware_nodes:
            my_hardware_nodes[one.type] = []
        if one not in my_hardware_nodes[one.type]:
            my_hardware_nodes[one.type].append(one)

        for dependency in one.hardware_on_hardware.iterator():
            if not dependency.type in my_hardware_nodes:
                my_hardware_nodes[dependency.type] = []
            if dependency not in my_hardware_nodes[dependency.type]:
                my_hardware_nodes[dependency.type].append(dependency)

        for dependency in one.depending_on_instance.iterator():
            if dependency not in my_instance_nodes:
                my_instance_nodes.append(dependency)
                if dependency.customer_accesable:
                    add_the_internet = True

    #
    # Build the graph
    #
    graph = pydotplus.Dot(graph_type='digraph')
    graph.set_prog('dot')
    #graph.set('mode', 'hier')
    graph.set('splines', 'polyline')
    graph.set('remincross', 'true')
    graph.set('overlap', 'false')

    graph.set('newrank', True)

    if add_the_internet:
        node = pydotplus.Node()
        node.set_name('Merchant')
        node.set('shape', 'box3d')
        graph.add_node(node)

    for hardware_type in my_hardware_nodes:
        if hardware_type != Hardware.LB:
            subgraph = pydotplus.Cluster(graph_name=hardware_type)
            subgraph.set('rank', 'same')
        for to_hardware in my_hardware_nodes[hardware_type]:
            node = pydotplus.Node()
            node.set_name(to_hardware.name)
            node.set('shape', 'box')
            if hardware_type != Hardware.LB:
                subgraph.add_node(node)
            else:
                graph.add_node(node)


            for from_hardware in to_hardware.hardware_on_hardware.iterator():
                for key in my_hardware_nodes:
                    if from_hardware in my_hardware_nodes[key]:
                        my_dependency = hardware_depending_on_hardware.objects.get(hardware_from=from_hardware, hardware_to=to_hardware)
                        edge = pydotplus.Edge(from_hardware.name, to_hardware.name)
                        edge.set(
                            'label', my_dependency.port_numbers.replace(',', ';')
                        )
                        graph.add_edge(edge)
        if hardware_type != Hardware.LB:
            graph.add_subgraph(subgraph)

    for to_instance in my_instance_nodes:
        node = pydotplus.Node()
        node.set_name(to_instance.__unicode__())
        node.set('URL', '/instance/%s/' % to_instance.slug)
        node.set('shape', 'component')
        graph.add_node(node)
        for key in my_hardware_nodes:
            for from_hardware in my_hardware_nodes[key]:
                if to_instance in from_hardware.depending_on_instance.iterator():
                    my_dependency = hardware_depending_on_instance.objects.get(from_hardware=from_hardware, to_instance=to_instance)
                    pprint(my_dependency.port_numbers)
                    edge = pydotplus.Edge(from_hardware.name, to_instance.__unicode__())
                    edge.set('headlabel', my_dependency.port_numbers)
                    graph.add_edge(edge)

        if to_instance.customer_accesable:
            edge = pydotplus.Edge('Merchant', to_instance.__unicode__())
            graph.add_edge(edge)

    #
    # Workaround to make SVG responsive
    #
    my_graph = graph.create(format='svg', )
    my_graph = re.sub(r"( width=)", " min-width=", my_graph)
    my_graph = re.sub(r"( height=)", " min-height=", my_graph)

    return my_graph