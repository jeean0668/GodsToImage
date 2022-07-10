
import pandas as pd
import os
import networkx as nx
import operator
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt 
from matplotlib import rc
from sqlite3 import connect

def drawing(dataset, lower_w_bound = 1000):
    
    centrality = nx.Graph()
    lower_w_bound = lower_w_bound
    dataset = dataset.sort_values(by=['weight'], ascending=False)
    dataset = dataset.reset_index(drop=True)
    
    for ind in range(len(np.where(dataset['weight'] >= lower_w_bound)[0])):
        # print(dataset['src'][ind], dataset['trg'][ind], int(dataset['weight'][ind]))
        centrality.add_edge(dataset['src'][ind], dataset['trg'][ind], weight = int(dataset['weight'][ind]))
    
    # multiple centrality 
    dgr = nx.degree_centrality(centrality)
    btw = nx.betweenness_centrality(centrality)
    cls = nx.closeness_centrality(centrality)
    #egv = nx.eigenvector_centrality(centrality)
    pgr = nx.pagerank(centrality)

    sorted_dgr = sorted(dgr.items(), key=operator.itemgetter(1), reverse = True)
    sorted_btw = sorted(btw.items(), key=operator.itemgetter(1), reverse = True)
    sorted_cls = sorted(cls.items(), key=operator.itemgetter(1), reverse = True)
    #sorted_egv = sorted(egv.items(), key=operator.itemgetter(1), reverse = True)
    sorted_pgr = sorted(pgr.items(), key=operator.itemgetter(1), reverse = True)
    
    # Graph drawing words network
    G = nx.Graph()
    
    for i in range(len(sorted_pgr)):
        G.add_node(sorted_pgr[i][0], nodesize = sorted_dgr[i][1])
    # print(np.where(dataset['weight']>lower_w_bound))
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
    # font setting
    
    fm._rebuild()
    font_fname = "C:/Windows/Fonts/Hancom Gothic Regular.ttf"
    fontprop = fm.FontProperties(fname = font_fname, size = 18).get_name()
    # rc('font', family = 'NanumBarunGothicOTF')
    nx.draw(G, node_size = sizes, pos = nx.spring_layout(G, k=3.5, iterations = 100), font_family = fontprop, **options)
    ax = plt.gca()
    # ax.collections[0].set_edgecolor("#555555")
    plt.show()
    
if __name__ == "__main__":
    
    debug = False
    root = "parsing/news/Islam_parsed"
    if debug:
        file_names = os.listdir(os.path.join(root, 'debug'))
    else:
        file_names = os.listdir(os.path.join(root, 'normal'))

    if debug:
        
        for file_name in file_names:
        
            conn = connect(os.path.join(root, 'debug', file_name))
            dataset = pd.read_sql("SELECT src, trg, weight FROM 'mytable'",
                                  conn)
            drawing(dataset)
            conn.close()
    else:
        for file_name in file_names:
            
            conn = connect(os.path.join(root, 'normal', file_name))
            
            dataset = pd.read_sql(f"SELECT src, trg, weight FROM 'mytable'",
                                  conn)
            drawing(dataset)
            conn.close()
        
    