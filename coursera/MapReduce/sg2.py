import sys
import random
import networkx
import MapReduce

def get_label(g, node):
    return g.node[node]['label']

def data(gml):
    results = {}
    g = networkx.read_gml(gml)

    g = networkx.DiGraph(g)
    del_edges = random.sample(g.edges(), len(g.edges()) / 2)
    g.remove_edges_from(del_edges)

    nodes = g.nodes()
    for node in nodes:
        label = get_label(g, node)
        if label in results:
            raise Exception('namespace collision!')
        else:
            results[label] = []
        neighbors = g.neighbors(node)
        for neighbor in neighbors:
            results[label].append(get_label(g,neighbor))

    return results

def mapper(mr, person, friends):
    for friend in friends:
        mr.emit_intermediate(person, friend)
        mr.emit_intermediate(friend, person)

def reducer(mr, person, friend_list):
    counts = {}
    for friend in friend_list:
        counts.setdefault(friend, 0)
        counts[friend] = counts[friend] + 1

    nonsym = filter(lambda x : counts[x] == 1, counts.keys())

    for i in nonsym:
        mr.emit((person, i))

def main():
    persons = data(sys.argv[1])
    MapReduce.execute(persons, mapper, reducer)

if __name__ == '__main__':
    main()
