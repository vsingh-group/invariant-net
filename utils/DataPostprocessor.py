import json
import cv2
import numpy as np
from ast import literal_eval

class DataPostprocessor:

  def __init__(self):
    
    with open('./dat/reducedIntToColors.json') as infile:
      self.classNumberToColor = json.load(infile)

  def segmentation_colors(self, image):
    HEIGHT = image.shape[0]
    WIDTH = image.shape[1]
    seg_color = np.zeros((HEIGHT,WIDTH,3),dtype=np.int32)
    for i in range(HEIGHT):
      for j in range(WIDTH):
        if image[i][j]==0:
          seg_color[i][j] = [0,0,0]
        else:
          key = str(int(image[i][j]))
          color = literal_eval(self.classNumberToColor[key])
          seg_color[i][j] = [color[0], color[1], color[2]]
    return seg_color

  def write_out(self, i, image, segmentation, ground_truth, iterations):
    """
      Args: 
        i: Image index
        image: The original image
        segmentation: A numpy array that represents a semantic segmentation of an image
        ground_truth: The corresponding ground truth
        iterations: Number of training steps

      Writes a colored segmentation, and its corresponding ground truth to disk
    """
    cv2.imwrite('./outputs/image-' + str(i) + '.png', image)
    colored_segmentation = self.segmentation_colors(segmentation)
    cv2.imwrite('./outputs/predicted-' + str(i) + '-iter' + str(iterations) + '.png', colored_segmentation)
    colored_ground_truth = self.segmentation_colors(ground_truth)
    cv2.imwrite('./outputs/ground_truth-' + str(i) + '.png', colored_ground_truth)



