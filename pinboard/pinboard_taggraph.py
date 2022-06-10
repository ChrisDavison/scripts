#!/usr/bin/env python3
"""Pinboard tag graph"""
import sys

import matplotlib.pyplot as plt
import numpy as np
import pinboard
import networkx as nx
from pathlib import Path


def label_sum(graph, label):
    return sum(d['weight'] for n, d in graph[label].items())


def main():
    token = Path("~/.pinboard").expanduser().read_text().strip()
    pb = pinboard.Pinboard(token)

    tag_to_find = sys.argv[1]
    posts = pb.posts.all(tag=tag_to_find)

    g2 = nx.Graph()
    for bookmark in posts:
        for tag in bookmark.tags:
            g2.add_node(tag)
            for other_tag in bookmark.tags:
                if tag == other_tag:
                    continue
                if other_tag not in g2:
                    g2.add_node(other_tag)
                if other_tag in g2[tag]:
                    g2[tag][other_tag]['weight'] += 1
                else:
                    g2.add_edge(tag, other_tag, weight=1)

    width = np.log(len(g2)) * 10
    height = width
    if len(g2) == 1:
        width = height = 4
    f, ax = plt.subplots(1, figsize=(width, height))

    pos = nx.drawing.spring_layout(g2, scale=2, k=1.5/np.sqrt(len(g2)),
                                   iterations=500)
    nx.draw_networkx_nodes(g2, pos, node_size=10000, ax=ax)

    weights = set(d['weight'] for (_, _, d) in g2.edges(data=True))
    for weight in weights:
        edgelist = [(u, v) for (u, v, d) in g2.edges(data=True)
                    if d['weight'] == weight]
        nx.draw_networkx_edges(g2, pos, edgelist=edgelist,
                               width=np.log(weight) * 3, ax=ax)

    labels = [f'{n}\n{label_sum(g2, n)}' for n in g2.nodes]
    edgelabels = dict(zip(g2, labels))
    nx.draw_networkx_labels(g2, pos,
                            labels=edgelabels,
                            font_size=20, font_family='sans-serif',
                            ax=ax)
    plt.axis('off')
    plt.show()
    f.savefig(f"pbtg_{tag_to_find}.svg", dpi=10000,
              facecolor='w', edgecolor='w',
              orientation='portrait',
              papertype=None,
              format=None,
              transparent=False,
              bbox_inches=None, pad_inches=0.1)


if __name__ == "__main__":
    main()
