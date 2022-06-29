
from ast import operator
from distutils.log import debug
import pandas as pd
import os
import openpyxl
import pymysql
import warnings
from collections import defaultdict

import sqlite3
from sqlite3 import connect

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
    print(len(news))
    
    for new_ in news:
        for i in range(len(new_)-1):
            src = new_[i]
            for j in range(i+1, len(new_)):
                trg = new_[j]
                if src == trg : continue
                frame[(src, trg)] += 1
         
def save_to_excel(frame, path, name):

    columns = ['src', 'trg', 'weight']
    df = pd.DataFrame([(k[0], k[1], v) for k, v in frame.items()], columns = columns)
    df = df.sort_values(by=['weight'], ascending=False)
    df = df.drop_duplicates(subset=['src', 'trg'], keep = 'last')
    try: 
        p = os.path.join(path, name + '.db')
        conn = connect(p)
        df.to_sql("SELECT src, trg, weight FROM '{name}'", conn)
        conn.close()
    except Exception as e:
        print(f"Error arise while saving to excel {name}...")
        print(e)
        print()
        conn.close()
    
if __name__ == "__main__":
    
    root = 'parsing/news/Islam'
    religion = 'Islam'
    debuggued = False
    
   
    path = "parsing/news/Islam_parsed"
    
    file_names = os.listdir(root)
    
    for file_name in file_names:
        
        frame = defaultdict(int)
    
        data = excel_open(file_name, root, debug = False)
        print(path)
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
            save_to_excel(frame, path + '/debug', '_debug_'+file_name)
        else:
            save_to_excel(frame, path + '/normal', '_parsed_'+file_name)
        print(f"{file_name} saving finished...")
        print(f"{file_name} finished!!!")
        print()
   
    