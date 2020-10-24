# Person Detection for Person Counting

This work contains various github repositories with different possibilities to implement person detections algorithms. The overall goal of this work is to provide a preprocessing step for another algorithm to count persons in videos. Especially counting persons in a bus entrance using the [pcds dataset](https://github.com/shijieS/people-counting-dataset) is implemented.

The code is currently optimized to use the RetinaNet implementation and further work or public contribution is necessary to make the repo compatible with multiple algorithms. The EfficientDet [implementation](https://github.com/xuannianz/EfficientDet) of xuannianz is already working to train on the pcds dataset. Some implementation effort is necessary to smoothly integrate the person counting algorithm. 

## Related repositories

This repository aims to provide a preprocessing step for the following person counting [algorithm](https://github.com/Yannick947/person_counting).

This repo contains forks from different open source repositories. These repositories must be added after cloning this repo as git submodules if you wish to use one of the algorithms:

* Object Detection with Keras RetinaNet [implementation](https://github.com/fizyr/keras-retinanet). 
* Object Detection with Keras EfficientDet [implementation](https://github.com/xuannianz/EfficientDet).
* Anchor Optimization for RetinaNet and EfficientDet from the [anchor-optimization](https://github.com/martinzlocha/anchor-optimization/) repository.  

Data repos: 
* [pcds dataset](https://github.com/shijieS/people-counting-dataset) for Person counting repo was used to generate a new [image dataset](https://github.com/Yannick947/pcds_images) for detecting persons in crowded situations in a bus entrance.

* The official WiderPerson [dataset](http://www.cbsr.ia.ac.cn/users/sfzhang/WiderPerson/) was adjusted to fit [our purpose](https://github.com/Yannick947/WiderPerson) for pretraining the weights on persons only. 

## Train and evaluate in Google Colab 

The training logging and further usage with the person counting algorithm was optimized to train in the Google Colaboratory environment. Mounting this folder in The notebooks provided can be directly used to train the algorithms and the logging and saving of the weights will be done in the related Google Drive folder. 

Different Colab notebooks are provided for different purposes which can be found in the notebooks folder: 
* efficientdet_pcds_images_trainer Trainer for pcds images with EfficientDet family
* evaluation_retinanet_models Evaluating RetinaNet and Inference time tests
* trainer_WiderPerson Colab trainer for RetinaNet on the WiderPerson dataset
* trainer_pcds_images Colab trainer for RetinaNet on the pcds images dataset
* preprocessing_wider_person Preprocessing utils for the WiderPerson dataset
* generate_detection_files The detection notebook to load all videos in a specified folder structure and create the detection frames (explained in the next section)

## Detection Frames

Detection Frames are the inputs for the person counting algorithm. You can create those .npy files for every video in a specified folder with the generate_detection_files.ipynb notebook. All x- and y-coordinates of person centers which were detected by a specified RetinaNet model will be saved in a .npy file. You can load this .npy file into a numpy array. For further information see the [person_counting repository](https://github.com/Yannick947/person_counting). An example detection frame for x- y- and time-coordinate can be seen here: 

<p float="left">
  <img src="images/entering_persons_x_t_coordinate.png" width="200" />
  <img src="images/entering_persons_y_t_coordinate.png" width="200" /> 
</p>

An example for 3D-detections can be seen here: 

![alt-text-1](/images/8persons_3d_plot.png "8 Persons entering the bus for x- y- and t-coordinate")

## Anchor optimization

In some cases, the default anchor configuration is not suitable for detecting objects in your dataset, for example, if your objects are smaller than the 32x32px (size of the smallest anchors). In this case, it might be suitable to modify the anchor configuration, this can be done automatically by following the steps in the [anchor-optimization](https://github.com/martinzlocha/anchor-optimization/) repository. To use the generated configuration check [here](https://github.com/fizyr/keras-retinanet-test-data/blob/master/config/config.ini) for an example config file and then pass it to `train.py` using the `--config` parameter.
