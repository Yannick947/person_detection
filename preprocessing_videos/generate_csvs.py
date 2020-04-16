import pandas as pd
import csv
import os 
import time
import numpy as np 

import keras
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

TOP_PATH = 'C:/Users/Yannick/OneDrive/Dokumente/Python/PCDS_videos/pcds_dataset'
MODEL_PATH = '/content/drive/My Drive/person_detection/keras-retinanet/snapshots/13-04-2020_103546_resnet152_13_0.h5'    
labels_to_names = {0: 'pedestrian'}                                     
FPS = 20
BACKBONE = 'resnet50'
THRESH = 0.4

def main():
    lower_video_length, upper_video_length = get_video_stats(TOP_PATH, lower_quantile=0.1,
                                                             upper_quantile=0.7, print=True)

    keras.backend.tensorflow_backend.set_session(get_session())
    model = models.load_model(MODEL_PATH, backbone_name=BACKBONE)
    model = models.convert_model(model)

    generate_csvs(TOP_PATH, model,
                  filter_lower_frames=lower_video_length,
                  filter_upper_frames=upper_video_length)


def get_session():
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.compat.v1.Session(config=config)


def generate_csvs(TOP_PATH, model, **kwargs):
    for root, _, files in os.walk(TOP_PATH):
        for file_name in files: 
            if file_name[-4:] == '.avi':
                generate_csv(root, file_name, model, **kwargs)

def generate_csv(root, file_name, model, filter_lower_frames=0, filter_upper_frames=1000):

    video_path = os.path.join(root, file_name)
    vcapture = cv2.VideoCapture(video_path)
    num_frames = int(vcapture.get(cv2.CAP_PROP_FRAME_COUNT))

    #skip if video is too short or too long
    if num_frames < filter_lower_frames or num_frames > filter_upper_frames:
        return

    height = int(vcapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    min_side_factor = 2
    downscale_factor_y = 2

    #create empty df for predictions.
    # Filter_upper_frame will set the length until where will be padded
    df_detections = create_zeroed_df(downscale_factor_y, filter_upper_frames, height)
    df_detections = fill_pred_image(model, min_side_factor, df_detections, vcapture, downscale_factor_y)
    df_detections.to_csv(video_path [0:-4] + '.csv', header=None)

    vcapture.release()

def fill_pred_image(model, min_side_factor, df_detections, vcapture, downscale_factor_y):
    success = True
    frame_index = 0
    width = int(vcapture.get(cv2.CAP_PROP_FRAME_WIDTH))  

    while success:
        if frame_index % 200 == 0:
            print("frame: ", frame_index)
        frame_index += 1
        # Read next image
        success, image = vcapture.read()

        if success:
            image = preprocess_image(image)
            image, scale = resize_image(image, min_side=width * min_side_factor, max_side=1333)
            boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
            boxes /= scale

            for box, score, label in zip(boxes[0], scores[0], labels[0]):
                # scores are sorted so we can break
                if score < THRESH:
                    break

                b = box.astype(int)

                #fill df with probability at the center of y axis, consider rezizing with min_side_factor
                df_detections.iloc[frame_index, int((b[3] + b[1]) / downscale_factor_y / 2 )] = score
    return df_detections

def create_zeroed_df(factor_y, num_frames, height):
  return pd.DataFrame(np.zeros((num_frames, int(height / factor_y))))

def get_video_stats(TOP_PATH, lower_quantile, upper_quantile, print=False): 
    video_length = pd.Series()
    for root, _, files in os.walk(TOP_PATH):
        for file_name in files: 
            if file_name[-4:] == '.avi':
                video_path = os.path.join(root, file_name)
                vcapture = cv2.VideoCapture(video_path)
                video_length = video_length.append(pd.Series(int(vcapture.get(cv2.CAP_PROP_FRAME_COUNT))))
                vcapture.release()
    if print == True: 
        print('First 10 number of frames of videos: ', video_length.iloc[0:10])
        print('Std of num video frames: ', video_length.std())
        print('Avg of num video frames: ', video_length.mean())

        for quantile in range(0, 10, 1):
            print('{} quantile of num video frames '.format(quantile / 10),
                video_length.quantile(quantile / 10))
    
    return video_length.quantile(lower_quantile), video_length.quantile(upper_quantile)


if __name__ == '__main__':
    main()