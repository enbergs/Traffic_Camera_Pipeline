from __future__ import unicode_literals

import sys, os
import cv2

import numpy as np

#from AbstractDetector import AbstractDetector
from tcp.registration.homography import Homography
from tcp.registration.obs_filtering import ObsFiltering
from tcp.registration.viz_regristration import VizRegristration
from tcp.configs.alberta_config import Config
import IPython
import glob
import cPickle as pickle

cnfg = Config()
vr = VizRegristration(cnfg)
hm = Homography(cnfg)
of = ObsFiltering(cnfg)

###GET VIDEOS
VIDEO_FILE = 'Train_Videos/*.mp4'
videos = glob.glob(VIDEO_FILE)

###LABEL VIDEOS
for video_path in sorted(videos):
    print 'Filtering video: %s' % video_path
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    camera_view_trajectory_pickle = '{0}/{1}/{1}_trajectories.cpkl'.format(cnfg.save_debug_pickles_path, video_name)
    camera_view_trajectory = pickle.load(open(camera_view_trajectory_pickle,'r'))

    assert camera_view_trajectory is not None, "%s doesn't have a trajectories pickle file" % video_name
    simulator_view_trajectory = hm.transform_trajectory(camera_view_trajectory)\

    filtered_trajectory = of.heuristic_label(simulator_view_trajectory)
        
    vr.visualize_trajectory_dots(filtered_trajectory, plot_traffic_images=False, video_name=video_name)

    raw_input('\nPress enter to continue...\n')

IPython.embed()
