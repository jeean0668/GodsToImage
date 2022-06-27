
import pandas as pd
import os
import networkx as nx
import operator
import numpy as np

def drawing(df):
    
    centrality = nx.Graph()
    
    

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
        dataset = pd.read_excel(os.path.join(root, file_names))
        
    