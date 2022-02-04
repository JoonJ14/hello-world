import os
import mne
from mne.annotations import read_annotations
from mne.event import read_events
import read_antcnt
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, butter, filtfilt
import numpy as np
import CartoolFiles as CF
import pandas as pd

def loadCap():
    matrix = pd.read_csv(r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\practice\HydroCel129Python.xyz', sep='\t', header=None)
    matrix = matrix.values

    x = matrix[:,0]
    y = matrix[:,1]
    z = matrix[:,2]
    z = z-np.max(z)

    x_cap = []
    y_cap = []
    for e in range(len(x)):
        distance = np.sqrt(x[e]**2 + y[e]**2 + z[e]**2)
        phase = np.arctan2(y[e], x[e])
        if (phase> np.pi):
            x_cap.append(-distance*np.cos(phase))
        else:
            x_cap.append(distance*np.cos(phase))
        
        if (phase < np.pi):
            y_cap.append(distance*np.sin(phase))
        else:
            y_cap.append(-distance*np.sin(phase))
    
    x_cap = np.array(x_cap)
    y_cap = np.array(y_cap)
    return x_cap, y_cap


def findBadElectrodes(data, starting, mini, maxi):
    bad = []
    for electrode in range(data.shape[1]):
        e = data[starting:,electrode]
        diff = np.max(e) - np.min(e)
        # print (diff)
      
        if diff < mini or diff > maxi:
            bad.append(int(electrode))
    return bad

def interpolationBadElectrodes(data, bads, surroundElectrodes, x, y):
    for bad in bads:
        bs_x = x[bad]
        bs_y = y[bad]

        distance = []
        for e in range(len(x)-1):
            if e != bad:
                distance.append([np.sqrt((x[e]-bs_x)**2 + (y[e]-bs_y)**2), e])
        distance = sorted(distance, key=lambda x:x[0])
        electrodes = np.zeros(data.shape[0])
        divided = 0
        for i in range(surroundElectrodes):
            electrodes = electrodes + distance[i][0]*data[:,distance[i][1]]
            divided = divided + distance[i][0]
        electrodes = electrodes/divided
        data[:,bad] = electrodes
    
    return data

path_folder = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\Subject\Step1'
path_out = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\Subject\Step2'
path_average = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\Subject\Average'
path_log = r'C:\Users\jjung31\OneDrive - Emory University\Desktop\EEG\Subject'
listes = os.listdir(path_folder)

try:
    os.makedirs(path_average)
except:
    pass

# threshold for detection
mini = 0.000000
maxi = 0.000120
starting = 200 # in millisecond
numberOfBadElectrodes = 50
surroundElectrodes = 5  # number of electrodes around the electrode for interpollation
minimumAcceptance = 12

# create log file if not exist
try:
    open('%s\log.txt' %path_log, 'r')
except:
    file = open('%s\log.txt' %path_log, 'w')
    file.write('name,triggers,numberOfTrials,goodTrials\n')
else:
    file = open('%s\log.txt' %path_log, 'a')

x_cap, y_cap = loadCap()

for liste in listes:
    folders = os.listdir(r'%s\%s' %(path_folder, liste))
    # print (folders)
    for folder in folders:
        eegs = os.listdir('%s\%s\%s' %(path_folder, liste, folder))
        output = []
        for eeg in eegs:
            try:
                tmp = CF.Eph('%s\%s\%s\%s' %(path_folder, liste, folder, eeg))
            except:
                print ('%s - bad reshape - %s - %s' %(liste, eeg, folder))
            else:
                data = tmp.Data
                bad = findBadElectrodes(data, starting, mini, maxi)
                if len(bad) <= numberOfBadElectrodes:
                    print ('%s - interpolation - %s - %s' %(liste, eeg, folder))
                    data = interpolationBadElectrodes(data, bad, surroundElectrodes, x_cap, y_cap)
                    output.append(data)
                    tmp.Data = data
                    try:
                        os.makedirs(r'%s\%s\%s' %(path_out, liste, folder))
                    except:
                        pass
                    tmp.write(r'%s\%s\%s\%s' %(path_out, liste, folder,  eeg))
                else:
                    print ('%s - too bad - %s - %s' %(liste, eeg, folder))
        
        file.write('%s,%s,%d,%d\n' %(liste, folder, len(eegs), len(output)))
        if len(output)>minimumAcceptance:
            output = np.array(output).mean(axis=0)
            tmp.Data = output
            tmp.write('%s\%s_%s.eph' %(path_average, liste, folder))


print ('done')


file.close()

    



