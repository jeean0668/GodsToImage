
from distutils.log import debug
import pandas as pd
import os
import openpyxl
import warnings
from collections import defaultdict

def excel_open(name, root = 'parsing/news/Islam', debug = False):
    
    with warnings.catch_warnings(record = True):
        warnings.simplefilter('always')
        file = pd.read_excel(os.path.join(root, name), engine="openpyxl")
        if debug:
            print(file['키워드'].head())
        return file['키워드']

def parsing_data(excel, debug = False):
    if debug:
        sentence = excel.iloc[0]
        keywords = sentence.split(',')
        print(keywords)
        return keywords
    else:
        ret = []
        for _, row in excel.iteritems():
            keywords = row.split(',')
            ret.append(keywords)
        return ret
    
def split_src_target(news, frame):
    # split the src and target 
    for new_ in news:
        for i in range(len(new_)-1):
            src = new_[i]
            for j in range(1, len(new_)):
                trg = new_[j]
                frame[(src, trg)] += 1
                
def save_to_excel(frame, path, name):

    columns = ['src', 'trg', 'weight']
    df = pd.DataFrame([(k[0], k[1], v) for k, v in frame.items()], columns = columns)
    df.to_csv(os.path.join(path, name), index = False)
    
if __name__ == "__main__":
    
    root = 'parsing/news/Islam'
    religion = 'Islam'
    debuggued = True
    frame = defaultdict(int)
    path = "parsing/news/Islam_parsed"
    
    file_names = os.listdir(root)
    
    data = excel_open(file_names[0], root, debug = False)
    # using only keyword column
    parsed = parsing_data(data, debug = False)
    
    if debuggued:
        split_src_target(parsed[:10], frame)
    else:
        split_src_target(parsed, frame)
        
    if debuggued:
        save_to_excel(frame, path, file_names[0] + '_debug')
    else:
        save_to_excel(frame, path, file_names[0])
   
    