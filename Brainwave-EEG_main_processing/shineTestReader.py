import os
import mne
from mne.annotations import read_annotations
from mne.event import read_events
import read_antcnt
import matplotlib.pyplot as plt

from scipy.signal import iirnotch, butter, filtfilt
import numpy as np


path = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\CNT'
name = r'APPLE_TEST_good_pre.cnt'
raw = read_antcnt.read_raw_antcnt(r"%s\%s" %(path, name),  preload=True, start_n_times=0, stop_n_times=-1)
data = raw.get_data().T

eeg = data[:,:-1]
evt = data[:,-1]

# 1 ) applied notch filter



# print (data.shape)

# plt.plot(data[:,-1])
# plt.show()


# evt = data[-2,:]
# plt.plot(evt)
# plt.show()
# print (evt)
# raw.plot()

# plt.show()
