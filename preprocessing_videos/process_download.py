import numpy as np
import urllib
import os
import csv
import time
from zipfile import ZipFile

# Data has to be donwloaded manually to process it, probably doesnt work on linux due to slashes

CRAWL_DIR = './'
PCDS_DIR = 'C:/Users/Yannick/OneDrive/Dokumente/Python/PCDS_videos/downloads/'
DESTINATION_DIR = 'C:/Users/Yannick/OneDrive/Dokumente/Python/PCDS_videos/pcds_dataset/'

def main(): 
    for file_name in os.listdir(PCDS_DIR):
        extract_zip(file_name, PCDS_DIR)

    for file_name in os.listdir(PCDS_DIR):
        remove_depth_videos(PCDS_DIR + file_name)
        move_videos(PCDS_DIR + file_name, DESTINATION_DIR)

def set_crawl_dir(dir):
    '''
    Set the directory where shall be crawled
    Arguments: 
        dir: Directory which shall be set
    '''
    global CRAWL_DIR
    CRAWL_DIR = dir 

def extract_zip(file_name, file_dir):
    ''''''

    if file_name[-4:] == '.zip':
        with ZipFile(file_dir + file_name, 'r') as zipObj:
            zipObj.extractall(file_dir + file_name[0:-4])

def remove_depth_videos(video_dir):
    '''
    Romve all depth videos from directory and subdirectories

    Arguments: 
        video_dir: Directory which shall be searched for depth videos
    '''

    for root, dirs, files in os.walk(video_dir):
        for name in files: 
            if 'Depth' in name: 
                os.remove(root + '/' + name.replace('\\','/'))
                print('Removed: ', name)
            
def move_videos(source_dir, destination_dir):
    '''
    Move videos and label files to another folder. Folder structure
    remains the same and videos stay at their place, label files are
    placed at the destination directory. 

    Arguements: 
        source_dir: Path to the directory which shall be moved
        destination_dir: Directory where files shall be placed in 
    
    '''

    existing_files = list()
    for _, _, files in os.walk(destination_dir):
        existing_files += files

    for root, dirs, files in os.walk(source_dir):
        for file_name in files: 
            full_path_file = os.path.join(root, file_name)
            destination_path = get_destination(full_path_file, destination_dir)
            os.replace(full_path_file, destination_path)

def get_destination(full_path_file, destination_dir):
    '''
    Returns the exact destination of the file where it shall be placed. 

    Arguments: 
        full_path_file: Full absolute path of the fall which shall be moved
        destination_dir: Top level folder where files are placed in

        returns: The exact absolute path to the directory within the destination_dir
        where the file shall be placed
    '''
    
    if 'label' in file_name: 
        return destination_dir + full_path_file[full_path_file.find('\\'):].replace('\\', '_')

    elif 'back' in full_path_name: 
        return destination_dir + 'back_out' + full_path_file[find_nth(full_path_file, '\\', 2):]

    elif 'front' in full_path_name: 
        return destination_dir + 'front_in' + full_path_file[find_nth(full_path_file, '\\', 2):]


def find_nth(string, search, n):
    '''
    Find the start poisiton of the nth character in a given string

    Arguments: 
        string: String in which will be searched
        search: charcater which will be searched in string
        n: The nth number of the string which shall be found

        returns: start position of nth char in given string, -1 if this 
        amount of strings doesnt exist in string
    '''

    start = string.find(search)
    while start >= 0 and n > 1:
        start = haystack.find(search, start+len(search))
        n -= 1
    return start

if __name__ == "__main__":
 main()


