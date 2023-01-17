import os
import mne
from mne.annotations import read_annotations
from mne.event import read_events
import read_antcnt
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, butter, filtfilt
import numpy as np
import CartoolFiles as CF


path = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\LL\CNT'
name = r'BABBLE_LL_Practice_Pre.cnt'
raw = read_antcnt.read_raw_antcnt(r"%s\%s" %(path, name),  preload=True, start_n_times=0, stop_n_times=-1)
data = raw.get_data().T

eeg = data[:,:-1]
evt = data[:,-1]

start = -200
ending = 1000

# 1) Notch filter
print ('notch filter')
b,a = iirnotch(60.0, 30.0, 1000.0)
for e in range(eeg.shape[1]):
    eeg[:,e] = filtfilt(b,a,eeg[:,e])

# 2) band pass to brain wave
print ('band pass')
b, a = butter(2, [0.3*2/1000.0, 40*2/1000.0], btype='band')
for e in range(eeg.shape[1]):
    eeg[:,e] = filtfilt(b,a,eeg[:,e])

# 3) average reference
print ('average reference')
average = np.mean(eeg, axis=1)
for e in range(eeg.shape[1]):
    eeg[:,e] = eeg[:,e] - average

print ('saving intermediate data')
tmp = CF.Eph('')
tmp.Electrodes = eeg.shape[1]
tmp.TF = eeg.shape[0]
tmp.Fs = 1000.0
tmp.Data = eeg
tmp.write(r'%s\tmp.eph' %path)

# 4) segement data by trigger
print ('segmentation')
try:
    os.makedirs(r'%s\tmp_event' %path)
except:
    print ('folder already exist')

tmp = CF.Eph('')
tmp.Electrodes = eeg.shape[1]
tmp.TF = ending - start
tmp.Fs = 1000.0

names = np.unique(evt)[1:]
for name in names:
    try:
        os.makedirs(r'%s\tmp_event\trig_%d' %(path, name))
    except:
        pass
    print ('\tsegmentation trigger: %d' %name)
    e = np.array(np.argwhere(evt == name))
    trigger = 1
    for index in e:
        index = index[0]
        
        tmp.Data = eeg[index+start:index+ending,:]
        tmp.write(r'%s\tmp_event\trig_%d\event_%03d.eph' %(path, name, trigger))
        trigger = trigger + 1

print ('done')




# print (data.shape)

# plt.plot(data[:,-1])
# plt.show()


# evt = data[-2,:]
# plt.plot(evt)
# plt.show()
# print (evt)
# raw.plot()

# plt.show()