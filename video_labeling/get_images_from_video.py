import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time

video_parent_path = 'C:/Users/Yannick/OneDrive/Dokumente/Python/PCDS_videos/detection_videos'
save_path = 'C:/Users/Yannick/Google Drive/person_detection/video_labeling/video_images'

#Set factor how much of the video shall be used, because end of video doesnt contain persons
UPPER_LENGTH = 0.8
#Every nth frame will be saved indicated in NTH_FRAME (25fps)
NTH_FRAME = 35

def main():
    save_images_videos(video_parent_path, save_path)

def save_images_videos(video_parent_path, save_path):
    ''' Crawl parent path, search for videos and save images for labeling from videos
    Arguments: 
        video_parent_path: Path to the parent directory where shall be crawled
        save_path: Path to parent directory where images shall be saved
    '''

    for video_name in os.listdir(video_parent_path):

        if video_name[-4:] != '.avi':
            continue

        video_path = os.path.join(video_parent_path, video_name)
        output_path = os.path.join(save_path, video_name)[:-4]
        print('Processing ', video_path, ' ..')
        vcapture = cv2.VideoCapture(video_path)

        num_frames = int(vcapture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(vcapture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
        height = int(vcapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if (height == 240) and (width == 320):
            save_images(vcapture, output_path, num_frames)

        else: 
            print('Video ', video_name, 'has wrong dimensions, skip!')
            continue

def save_images(v_capture, output_path, num_frames):
    '''Save images from given video 
    Arguments: 


    '''
    print('number of frames in this video: ', num_frames)
    frame_index = 0
    success = True
    start = time.time()

    while success:
        if frame_index > int(UPPER_LENGTH * num_frames):
            break

        success, image = v_capture.read()

        if success and ((frame_index % NTH_FRAME) == 0):

            save_image = image.copy()
            #TODO: Check if this line should be uncommented
            # save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2RGB)

            cv2.imwrite ('{output_path}_{frame_index}.jpg'.format(output_path=output_path,frame_index=frame_index), save_image)
            
        frame_index += 1

    v_capture.release()
    end = time.time()
    print("Total Time: ", end - start)

if __name__ == '__main__': 
    main()