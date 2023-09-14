# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:27:39 2022

@author: ZacharyAugenfeld
"""
import sys, os, glob
import numpy as np
import pandas as pd
from tifffile import imread, imwrite


# %%
input_color_amts = dict()
#output_color_amts = dict()
"""
The following section is for parameters of the psuedo-color definition.

"""

pulse_times_list = [20, 100]

# (R, G, B)
input_color_amts["365"]  = (  0,   0, 1) #pick Blue channel from 365-excitation image
input_color_amts["445"]  = (  0,   0, 1) #pick Blue channel from 445-excitation image
input_color_amts["525"]  = (  0,   1, 0) #pick Green channel from 525-excitation image
input_color_amts["590"]  = (0.5, 0.5, 0) #weighted average of Red and Green channels of 590-excitation image
input_color_amts["645"]  = (  1,   0, 0) #ie pick Red channel from 645-excitation image

excitations = sorted(list(input_color_amts.keys()))

#if not excitations == excitations_check:
#    raise ValueError("Need definitions for all wavelength excitations!")

nExcitations = len(excitations)
nPulsetimes = len(pulse_times_list)

if __name__ == "__main__":

    if len(sys.argv)<2:
        raise Exception("No target directory given!")

#    if len(sys.argv)<3:
#        raise Exception("No output file name given!")

    target_dir = sys.argv[1]
#    output_filename = sys.argv[2]

    target_dir = os.path.realpath(target_dir)
    print("Working in directory " + target_dir)

    if not os.path.exists(target_dir):
        raise ValueError(f"{target_dir} does not exist!")

    for wl in excitations:
        wl_filelist = sorted(glob.glob(os.path.join(target_dir, f"*_{wl}_*.tiff")))

    # Input images into X, a 4-D array:
        if not wl_filelist:
            raise ValueError(f"No .tiff files or wavelength {wl} in given directory!")
        #print(wl_filelist)
    #Need to cycle though pulse time values to separate data
        data_list = [[] for _ in range(nPulsetimes)]
        index_list = [[] for _ in range(nPulsetimes)]
        pt_idx = -1
        for file_idx, tiff_file in enumerate(wl_filelist):
            pt_idx += 1
            if pt_idx == nPulsetimes:
                #print(f"pt_idx = {pt_idx}. Resetting to 0")
                pt_idx = 0
            pulsetime = str(pulse_times_list[pt_idx])
            splitfile = tiff_file.split('_')
            file_timestamp = splitfile[-1].split('.')[0]
            img = imread(tiff_file)
            data_list[pt_idx].append( np.mean(img @ input_color_amts[wl]) )
            #print(f"Appending wavelength {wl} to datalist {pt_idx} with data")
            index_list[pt_idx].append(file_timestamp)
        #print(index_list)

        for pt_idx, pt in enumerate(pulse_times_list):
            series = pd.Series(data = data_list[pt_idx], index = index_list[pt_idx], name=wl+'_'+str(pt))
            series.to_csv(os.path.join(target_dir, wl+'_'+str(pt)+'.csv'))