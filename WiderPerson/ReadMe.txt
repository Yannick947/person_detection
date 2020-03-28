WiderPerson: A Diverse Dataset for Dense Pedestrian Detection in the Wild


########## Introduction ##########
The WiderPerson dataset is a pedestrian detection benchmark dataset in the wild, of which images are selected from a wide range of scenarios, no longer limited to the traffic scenario. We choose 13,382 images and label about 400K annotations with various kinds of occlusions. We randomly select 8000/1000/4382 images as training, validation and testing subsets. Similar to CityPersons and WIDER FACE datasets, we do not release the bounding box ground truths for the test images. Users are required to submit final prediction files, which we shall proceed to evaluate.


##########  Contest ##########
"./Images":          13,382 images of this dataset.
"./Annotations":     9,000 annotation text files of training and valiadation subsets.
"./Evaluation":      evaluation codes.
"./train.txt":       file list of training subset.
"./test.txt":        file list of testing subset.
"./val.txt":         file list of validation subset.
"./ReadMe.txt":      this file.


########## Annotation Format ##########
Each image of training and valiadation subsets in the "./Images" folder (e.g., 000001.jpg) has a corresponding annotation text file in the "./Annotations" folder (e.g., 000001.jpg.txt). The annotation file structure is in the following format:
    '''
    < number of annotations in this image = N > 
    < anno 1 >
    < anno 2 >
    ......
    < anno N >
    '''
where one object instance per row is [class_label, x1, y1, x2, y2], and the class label definition is:
    '''
    class_label =1: pedestrians
    class_label =2: riders
    class_label =3: partially-visible persons
    class_label =4: ignore regions
    class_label =5: crowd
    '''


########## Detection Output ##########
The detection results for each image should be a text file with the same prefix of the image but with ".txt" suffix, e.g., 000001.jpg -> 000001.txt. All the detection text files should be put in a folder for evaluation. The detection output file is expected in the follwing format: 
    '''
    <number of detections in this image = N>
    <det 1>
    <det 2>
    ......
    <det N>
    '''
Each detected bounding box is expected in the format [x1, y1, x2, y2, score].


########## Evaluation ##########
After getting the folder of detection results (e.g., vgg_frcnn), put this folder into the "./Evaluation" folder, then modify the 'legend_name' and 'pred_dir' correspondingly in the "wider_eval.m", finally run the "wider_eval.m" to get evaluation metrics.