# -*- coding: utf-8 -*-
"""RMSD.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xvVcGmS9CuBe3pvqhZYx2FsXCRY_G7Ae

# Comparing Deformation Metrics - Between models, RMSD
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

# Commented out IPython magic to ensure Python compatibility.
# %cd /content
!git clone https://github.com/mirabdi/PDAnalysis.git

# Change directory into the PDAnalysis repository
# %cd /content/PDAnalysis/
!git pull origin main
!ls

!pip install PDAnalysis --upgrade
from PDAnalysis import Protein, AverageProtein, Deformation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def calculation_RMSD(pathA, pathB):
    ### Calculate RMSD

    # Load each protein, with the parameters specified before (protein_kwargs)
    # protA = Protein(pathA, **protein_kwargs)
    # protB = Protein(pathB, **protein_kwargs)
    protA = Protein(pathA)
    protB = Protein(pathB)

    # Initialize the Deformation object
    deform_kwargs = {'method':'rmsd'}
    deform = Deformation(protA, protB, **deform_kwargs)
    # Run the calculations outlined in deform_kwargs['method']
    deform.run()

    rmsd_all = deform.rmsd_per_residue
    rmsd = np.nanmean(rmsd_all)

    return rmsd

"""Pairwise RMSD across all models"""

root = '/content/drive/MyDrive/capstone/output_omegafold_esmfold/'
model_names = ['esmfold', 'omegafold', 'rosettafold', 'alphafold']
model_num = len(model_names)
columns = [f'{model_names[i]}_vs_{model_names[j]}' for i in range(len(model_names)) for j in range(i+1, len(model_names))]

nola_rmsd = pd.DataFrame(np.zeros((19, model_num*(model_num-1)//2)), columns = columns)
loki_rmsd = pd.DataFrame(np.zeros((17, model_num*(model_num-1)//2)), columns = columns)

nola_row_idx = 0
loki_row_idx = 0

for file in os.listdir(root + 'output_alphafold'):
    file = file.lower()
    match_char = '_'.join(file.split('_')[1:4]) if 'original' not in file else '_'.join(file.split('_')[1:3])[:-4]
    print(match_char) # 'loki_single_3', 'nola_original', etc

    scores_for_each_row = []
    for i in range(len(model_names)):
        model1 = model_names[i]

        # find match_char in model1 sequences
        for path in os.listdir(root + f'output_{model1}/'):
            if (('original' in path.lower()) and (match_char in path.lower())) or (('original' not in match_char) and (match_char + '_' in path.lower())):
                seq_model1_path = root + f'output_{model1}/' + path
                break

        for j in range(i+1, len(model_names)):
            model2 = model_names[j]
            for path in os.listdir(root + f'output_{model2}/'):
                if (('original' in path.lower()) and (match_char in path.lower())) or (('original' not in match_char) and (match_char + '_' in path.lower())):
                    seq_model2_path = root + f'output_{model2}/' + path

                    print(seq_model1_path, seq_model2_path, ('original' and match_char) in path.lower())
                    RMSD_score = calculation_RMSD(seq_model1_path, seq_model2_path)
                    scores_for_each_row.append(RMSD_score)
                    break

    if match_char.startswith('nola'):
        print(scores_for_each_row)
        nola_rmsd.loc[nola_row_idx, :] = scores_for_each_row
        nola_rmsd = nola_rmsd.rename(index={nola_row_idx: match_char})
        nola_row_idx += 1
    else:
        print(scores_for_each_row)
        loki_rmsd.loc[loki_row_idx, :] = scores_for_each_row
        loki_rmsd = loki_rmsd.rename(index={loki_row_idx: match_char})
        loki_row_idx += 1


# Add an avg row
avg_row = nola_rmsd.mean()
nola_rmsd.loc[len(nola_rmsd)] = avg_row.tolist()
nola_rmsd = nola_rmsd.rename(index={len(nola_rmsd)-1: 'Average'})
avg_row = loki_rmsd.mean()
loki_rmsd.loc[len(loki_rmsd)] = avg_row.tolist()
loki_rmsd = loki_rmsd.rename(index={len(loki_rmsd)-1: 'Average'})

print('\nNola:')
print(nola_rmsd.shape)
nola_rmsd

print('\nLoki:')
loki_rmsd

"""---"""