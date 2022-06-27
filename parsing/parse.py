
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
        # 불용어를 처리해준다.
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
    try:
        df.to_csv(os.path.join(path, name), index = False)
    except:
        print(f"Error arise while saving to excel {name}...")
    
if __name__ == "__main__":
    
    root = 'parsing/news/Islam'
    religion = 'Islam'
    debuggued = True
    
    path = "parsing/news/Islam_parsed"
    
    file_names = os.listdir(root)
    
    for file_name in file_names:
        
        frame = defaultdict(int)
        
        data = excel_open(file_name, root, debug = False)
        
        # using only keyword column
        print(f"parsing the {file_name}...")
        parsed = parsing_data(data, debug = False)
        print(f"{file_name} parsing finished...")
        
        print(f"spliting the {file_name}...")
        if debuggued:
            split_src_target(parsed[:10], frame)
        else:
            split_src_target(parsed, frame)
        print(f"{file_name} spliting finished...")
        
        print(f"saving the {file_name}...")
        if debuggued:
            save_to_excel(frame, path, file_name + '_debug')
        else:
            save_to_excel(frame, path, file_name)
        print(f"{file_name} saving finished...")
        print(f"{file_name} finished!!!")
        print()
   
    