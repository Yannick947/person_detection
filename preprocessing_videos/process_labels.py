import pandas as pd
import csv
import os 
import numpy as np 

# import tensorflow as tf

'''

Label files from original dataset have following structure: 
DepthVideoName, EnteringNumber, ExitingNumber, VideoType

DepthVideoName: the depth video name
EnteringNumber: the number of people entering the bus
ExitingNumber: the number of people exiting the bus
VideoType: the video type. There are 4 video types represented by the index (0: N-C-, 1: N-C+, 2: N+C-, 3: N+C+)

'''

HEADER = ['file_name', 'entering', 'exiting', 'video_type']
TOP_PATH = 'C:/Users/Yannick/OneDrive/Dokumente/Python/PCDS_videos/pcds_dataset'

def main():
    unite_labels(TOP_PATH)

def unite_labels(top_path):
    '''
    Add content of all existing label.txt files to the labels_united.csv file

    Arguments: 
        top_path: Path where labels_united.csv must be placed and where shall 
        be searched for label.txt files 
    '''

    df_labels = load_labels(top_path)

    for file_name in os.listdir(top_path): 
        if 'label' in file_name and not ('crowd' in file_name) and not (file_name == 'labels_united.csv'):
            labels_singlefile = get_labels(top_path, file_name)
            df_labels = pd.concat([df_labels, labels_singlefile],
                                    axis=0).drop_duplicates(subset='file_name')

    df_labels.to_csv(top_path + '/labels_united.csv', header = None, index=None)
                
                
def load_labels(top_path):
    '''
    Checks in top path if there is an already existing 'labels_united.csv', 
    otherwise return an empty df with correct header names

    Arguments: 
        top_path: Path where shall be searched for the labels_united.csv file

        returns: The previously stored labels_united file as pandas Dataframe, 
                 and an empty Dataframe if no such file exists
    '''

    files = os.listdir(top_path)

    if 'labels_united.csv' in files: 
        return pd.read_csv(top_path + '/labels_united.csv', names=HEADER)

    else: 
        return pd.DataFrame(columns=HEADER) 


def get_labels(root, file_name):
    '''
    Gets the labels of a single txt file
    Arguments: 
        file_name: The name of the file which shall be returned
    '''
    full_path = os.path.join(root, file_name)
    with open(full_path, mode='r') as label:
        lines_after_header = label.readlines()[4:]
        lines_splitted = [i.split() for i in lines_after_header]
        assert len(lines_splitted[1]) == 4
        return pd.DataFrame(lines_splitted, columns=HEADER)

if __name__ == '__main__':
    main()