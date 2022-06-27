
import pandas as pd
import os
import networkx as nx
import operator
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt 

def drawing(df):
    
    centrality = nx.Graph()
    lower_w_bound = 2
    
    for ind in range(len(np.where(dataset['weight'] >= lower_w_bound)[0])):
        centrality.add_edge(dataset['src'][ind], dataset['trg'][ind], weight = int(dataset['weight'][ind]))
    
    # multiple centrality 
    dgr = nx.degree_centrality(centrality)
    btw = nx.betweenness_centrality(centrality)
    cls = nx.closeness_centrality(centrality)
    egv = nx.eigenvector_centrality(centrality)
    pgr = nx.pagerank(centrality)

    sorted_dgr = sorted(dgr.items(), key=operator.itemgetter(1), reverse = True)
    sorted_btw = sorted(btw.items(), key=operator.itemgetter(1), reverse = True)
    sorted_cls = sorted(cls.items(), key=operator.itemgetter(1), reverse = True)
    sorted_egv = sorted(egv.items(), key=operator.itemgetter(1), reverse = True)
    sorted_pgr = sorted(pgr.items(), key=operator.itemgetter(1), reverse = True)
    
    # Graph drawing words network
    G = nx.Graph()
    
    for i in range(len(sorted_pgr)):
        G.add_node(sorted_pgr[i][0], nodesize = sorted_dgr[i][1])
    for ind in range(len(np.where(dataset['weight']>lower_w_bound)[0])):
        G.add_weighted_edges_from([(dataset['src'][ind], dataset['trg'][ind], int(dataset['weight'][ind]))])
        
    # resize the node
    sizes = [G.nodes[node]['nodesize'] * 500 for node in G]
    
    options = {
        'edge_color' : '#FFDEA2',
        'width' : 1,
        'with_labels' : True,
        'font_weight' : 'regular',
    }
    
    nx.draw(G, node_size = sizes, pos = nx.spring_layout(G, k=3.5), **options)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#555555")
    plt.show()
    

if __name__ == "__main__":
    
    debug = True
    root = "parsing/news/Islam_parsed"
    if debug:
        file_names = os.listdir(os.path.join(root, 'debug'))
    else:
        file_names = os.listdir(root)

    if debug:
        dataset = pd.read_excel(os.path.join(root, 'debug',file_names[0]))
        drawing(dataset)
    else:
        for file_name in file_names:
            dataset = pd.read_excel(os.path.join(root, file_name))
            drawing(dataset)
        
    