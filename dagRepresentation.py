import networkx as nx
from matplotlib import pyplot as plt
class Graph:
    def __init__(self,workflow):
        self.workflow=workflow


if __name__=='__main__':
    graph = nx.DiGraph()
    graph.add_edges_from([("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")])
    plt.tight_layout()
    nx.draw_networkx(graph, arrows=True)
    plt.savefig("g1.png", format="PNG")
    # tell matplotlib you're done with the plot: https://stackoverflow.com/questions/741877/how-do-i-tell-matplotlib-that-i-am-done-with-a-plot
    plt.clf()