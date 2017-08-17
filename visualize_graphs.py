from graph_tool.all import *
from itertools import product
import parikh_sets
import parikh_monotonicity


def contains(a, b):
    """Return true iff b <= a (where a and b are vectors)."""
    for i in xrange(len(a)):
        if b[i] > a[i]:
            return False
    return True


def visualize_parikh_set(pi):
    """Visualizes the given Parikh sets (pi_k) - creates a graph where each node is a Parikh vector and the edges are
    the connections between each pi_i, pi_{i+1} levels (for i=1..k-1)."""
    assert len(pi) > 0
    sigma_size = len(next(iter(pi[1])))
    # each pi_k needs to have an ordering (for the nodes in the graph)
    pi = {i: sorted(pi[i]) for i in pi.iterkeys()}
    g = Graph()
    # vertex property for the labels
    v_prop = g.new_vertex_property("string")
    # vertex property for the positions of the nodes
    pos = g.new_vertex_property("vector<double>")
    width = max(pi.iterkeys())
    # vector that holds the nodes of the "previous" line
    pv1 = [g.add_vertex() for _ in xrange(sigma_size)]
    # build the first "line" of nodes vertex properties
    for l in xrange(sigma_size):
        v_prop[pv1[l]] = parikh_sets.tuple_to_str(pi[1][l])
        pos[pv1[l]] = (-width / float(sigma_size) * l, 1)
    for j in xrange(2, width + 1):
        # vector that holds the nodes of the "actual" line
        pv2 = [g.add_vertex() for _ in xrange(len(pi[j]))]
        # build the actual "line" of nodes vertex properties
        for l in xrange(len(pv2)):
            v_prop[pv2[l]] = parikh_sets.tuple_to_str(pi[j][l])
            pos[pv2[l]] = (-width / float(len(pv2)) * l, j)
        # add edges between the nodes of the previous and the current line
        for p in xrange(len(pi[j - 1])):
            for q in xrange(len(pi[j])):
                if contains(pi[j][q], pi[j - 1][p]):
                    g.add_edge(pv1[p], pv2[q])
        pv1 = pv2

    return g, v_prop, pos


for pi in parikh_monotonicity.find_exception(2):
    g, v_prop, pos = visualize_parikh_set(pi)
    graph_draw(g, vertex_text=v_prop, vertex_font_size=18, pos=pos)
