import csv
import numpy as np
import pandas as pd

def main():
    reader = pd.read_csv("data_mejora.csv",sep = ';')
    new_data = pd.DataFrame(columns=['bytes','Tamaño en bytes','Recibido en bytes','tiempo tardado','bw '])
    for i in range(1,9990):
        temp = None
        subData = reader[reader['bytes'] == i] 
        if not subData.empty:#empty dataFrame
            dataSelect = subData[subData['bw '] == max(subData['bw '])]
            new_data = pd.concat([new_data,dataSelect])
    new_data.to_csv('preProsData.csv')
    
main()