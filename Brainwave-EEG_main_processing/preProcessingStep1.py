import os
import mne
from mne.annotations import read_annotations
from mne.event import read_events
import read_antcnt
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, butter, filtfilt
import numpy as np
import CartoolFiles as CF


path_folder = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\Subject\RawCNT'
path_out = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\Subject\Step1'

listes = os.listdir(path_folder)
output = []
for liste in listes:
    output.append(liste.split('.')[0])
listes = np.unique(output)

# to go through files from behind
# listes = listes[::-1]

try:
    os.makedirs(path_out)
except:
    pass

for liste in listes:
    name = r'%s.cnt' %(liste)
    
    # name = r'APPLE_TEST_good_pre.cnt'
    print ('loading data')
    raw = read_antcnt.read_raw_antcnt(r"%s\%s" %(path_folder, name),  preload=True, start_n_times=0, stop_n_times=-1)
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

    # print ('saving intermediate data')
    # tmp = CF.Eph('')
    # tmp.Electrodes = eeg.shape[1]
    # tmp.TF = eeg.shape[0]
    # tmp.Fs = 1000.0
    # tmp.Data = eeg
    # tmp.write(r'%s\%s\tmp.eph' %path)

    # 4) segement data by trigger
    print ('segmentation')
    # try:
    #     os.makedirs(r'%s\tmp_event' %path)
    # except:
    #     print ('folder already exist')

    tmp = CF.Eph('')
    tmp.Electrodes = eeg.shape[1]
    tmp.TF = ending - start
    tmp.Fs = int(1000)

    triggers = np.unique(evt)[1:]

    for trigger in triggers:
        
        try:
            os.makedirs(r'%s\%s\trig_%d' %(path_out, name, trigger))
        except:
            pass
        print ('\tsegmentation trigger: %d' %trigger)
        e = np.array(np.argwhere(evt == trigger))
        trig = 1
        for index in e:
            index = index[0]
            
            tmp.Data = eeg[index+start:index+ending,:]
            tmp.write(r'%s\%s\trig_%d\event_%03d.eph' %(path_out, name,trigger,  trig))
            trig = trig + 1
            # print ('saving')
    print ('done')




# # print (data.shape)

# # plt.plot(data[:,-1])
# # plt.show()


# # evt = data[-2,:]
# # plt.plot(evt)
# # plt.show()
# # print (evt)
# # raw.plot()

# # plt.show()
