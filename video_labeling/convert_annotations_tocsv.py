from pandas.io.json import json_normalize
import json
import pandas as pd

from sklearn.model_selection import train_test_split

path_json_labels = 'C:/Users/Yannick/Google Drive/person_detection/video_labeling/labels.json'
training_path = '/content/sample_data/pcds_images/'

def main():
    
    with open(path_json_labels) as json_file:
        data = json.load(json_file)
        df_flattened = json_normalize(data['images'])

    df_lists = get_lists(df_flattened)

    df_annot = pd.concat(df_lists, ignore_index=True)
    df_annot= df_annot.apply(unroll_bbox, axis=1).drop(columns=['polygon', 'mask', 'z_index', 'bbox'])

    #Add static path to filename for training 
    df_annot['image_name'] = training_path + df_annot['image_name']  
    df_annot = df_annot[df_annot['image_status'] == 'DONE']
    #reorder
    df_annot = df_annot[['image_name', 'x_min', 'y_min', 'x_max', 'y_max', 'class_name']]

    df_annot_train, df_annot_test = split_on_filenames(df_annot)

    df_annot_train.to_csv('annot_train_pcds.csv', index=None, header=None, sep=",", line_terminator='\n', encoding='utf-8')
    df_annot_test.to_csv('annot_test_pcds.csv', index=None, header=None, sep=",", line_terminator='\n', encoding='utf-8')

def split_on_filenames(df):
    '''
    '''
    df_names = df['image_name'].unique()
    df_names_train, df_names_test = train_test_split(df_names)

    df_train = df[df.image_name.isin(df_names_train)]
    df_test = df[df.image_name.isin(df_names_test)]

    return df_train, df_test

def get_lists(df_flattened):
    ret_list = list()
    for x in df_flattened['labels']:
        if x == []:
            continue
        ret_df = pd.DataFrame(json_normalize(x))
        ret_df['image_name'] = df_flattened['image_name']
        ret_df['image_status'] = df_flattened['image_status']
        ret_list.append(ret_df)

    return ret_list

def unroll_bbox(row): 
    try: 
        row['x_min'] = row[0][0]
        row['y_min'] = row[0][1]
        row['x_max'] = row[0][2]
        row['y_max'] = row[0][3]
    except: 
        return None
    return row
    # row.drop(0, inplace=True)

if __name__ == '__main__': 
    main()


