# -*- coding: utf-8 -*-
"""EffectiveStrain_calculation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zlf3Q7aMMIQsXKizu4kzGK-mtm7GtDJL

# Comparing Deformation Metrics
PDA can be used to calculate the following deformation metrics:
1. Effective Strain (strain)
2. Shear Strain (shear)
3. Non-affine Strain (non_affine)
4. Local Distance Difference Test (lddt)
5. Local Distance Difference (ldd)
6. Neighborhood Distance (neighbor_distance)
7. Root Mean Square Deviation (rmsd)

The original code can be found in the "Original Code" section. We modified the code to calculate only the Effective Strain Score and compare the models.
"""

from google.colab import drive
drive.mount('/content/drive')

"""## Modified Code"""

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

"""### Calculate Effective Strain"""

# Setting the parameters to use in the deformation calculation

# We will include residues in local neighborhoods if their Alpha-carbon
# positions are within 13 Angstroms of each other (neigh_cut).

# We will use a exclude any residues with pLDDT lower than 70 (min_plddt).
# This is only appropriate for AlphaFold-generated structures.
# protein_kwargs = {"neigh_cut":13.0, "min_plddt":70}

# For each residue we will calculate Effective Strain (strain),
# and the distance to the nearest mutated residue (mut_dist)
deform_kwargs = {'method':'all'}

def calculation_ES(pathA, pathB):
  ### Calculate mutliple deformation metrics

  # Load each protein, with the parameters specified before (protein_kwargs)
  # protA = Protein(pathA, **protein_kwargs)
  # protB = Protein(pathB, **protein_kwargs)
  protA = Protein(pathA)
  protB = Protein(pathB)

  # Initialize the Deformation object
  deform = Deformation(protA, protB, **deform_kwargs)
  # Run the calculations outlined in deform_kwargs['method']
  deform.run()

  metrics = ["Effective Strain", "RMSD"]
  deformation_metrics = [deform.strain, deform.rmsd_per_residue]

  for i, dm in enumerate(deformation_metrics):
      print(metrics[i], ':', np.nanmean(dm))

  EF_score = np.nanmean(deformation_metrics[0])
  return EF_score

"""#### ESMFold"""

import os

# ESMFOLD
folder_path = "/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold"

# NOLA
ESM_ES_nola_single = {}
ESM_ES_nola_double = {}
noal_original = f'{folder_path}/IL31R_Nola_Original.pdb'
all_files = os.listdir(folder_path)
for file in all_files:
    # single-mutated
    if file.startswith("IL31R_Nola_Single_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        ESM_ES_nola_single[file] = ES_score
    # double-mutated
    elif file.startswith("IL31R_Nola_Double_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        ESM_ES_nola_double[file] = ES_score

# Loki
ESM_ES_loki_single = {}
ESM_ES_loki_double = {}
loki_original = f'{folder_path}/IL31_Loki_Original.pdb'
for file in all_files:
    if file.startswith("IL31_Loki_Single_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        ESM_ES_loki_single[file] = ES_score
    elif file.startswith("IL31_Loki_Double_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        ESM_ES_loki_double[file] = ES_score

ESM_ES_loki_single

print("Model Name: ESMFold")

ES_nola = list(ESM_ES_nola_single.values())
avg_ES_nola_single = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-single)", avg_ES_nola_single)

ES_nola = list(ESM_ES_nola_double.values())
avg_ES_nola_double = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-double)", avg_ES_nola_double)

ES_loki = list(ESM_ES_loki_single.values())
avg_ES_loki_single = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-single)", avg_ES_loki_single)

ES_loki = list(ESM_ES_loki_double.values())
avg_ES_loki_double = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-double)", avg_ES_loki_double)

print(avg_ES_nola_single, avg_ES_nola_double, avg_ES_loki_single, avg_ES_loki_double)

"""#### OmegaFold"""

import os

# Omegafold
folder_path = "/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold"

# NOLA
Omega_ES_nola_single = {}
Omega_ES_nola_double = {}
noal_original = f'{folder_path}/IL31R_Nola_Original.pdb'
all_files = os.listdir(folder_path)
for file in all_files:
    # single-mutated
    if file.startswith("IL31R_Nola_Single_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        Omega_ES_nola_single[file] = ES_score
    # double-mutated
    elif file.startswith("IL31R_Nola_Double_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        Omega_ES_nola_double[file] = ES_score

# Loki
Omega_ES_loki_single = {}
Omega_ES_loki_double = {}
loki_original = f'{folder_path}/IL31_Loki_Original.pdb'
for file in all_files:
    if file.startswith("IL31_Loki_Single_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        Omega_ES_loki_single[file] = ES_score
    elif file.startswith("IL31_Loki_Double_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        Omega_ES_loki_double[file] = ES_score

print("Model Name: OmegaFold")

ES_nola = list(Omega_ES_nola_single.values())
avg_ES_nola_single = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-single)", avg_ES_nola_single)

ES_nola = list(Omega_ES_nola_double.values())
avg_ES_nola_double = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-double)", avg_ES_nola_double)

ES_loki = list(Omega_ES_loki_single.values())
avg_ES_loki_single = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-single)", avg_ES_loki_single)

ES_loki = list(Omega_ES_loki_double.values())
avg_ES_loki_double = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-double)", avg_ES_loki_double)

print(avg_ES_nola_single, avg_ES_nola_double, avg_ES_loki_single, avg_ES_loki_double)

"""#### AlphaFold"""

import os

# Omegafold
folder_path = "/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold"
all_files = os.listdir(folder_path)

# NOLA
Alpha_ES_nola_single = {}
Alpha_ES_nola_double = {}
noal_original = f'{folder_path}/IL31R_Nola_Original.pdb'
for file in all_files:
    # single-mutated
    if file.startswith("IL31R_Nola_Single_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        Alpha_ES_nola_single[file] = ES_score
    # double-mutated
    elif file.startswith("IL31R_Nola_Double_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        Alpha_ES_nola_double[file] = ES_score

# Loki
Alpha_ES_loki_single = {}
Alpha_ES_loki_double = {}
loki_original = f'{folder_path}/IL31_Loki_Original.pdb'
for file in all_files:
    if file.startswith("IL31_Loki_Single_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)
        print("compare file: ", compare_file_path)
        ES_score = calculation_ES(loki_original, compare_file_path)
        Alpha_ES_loki_single[file] = ES_score
    elif file.startswith("IL31_Loki_Double_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        Alpha_ES_loki_double[file] = ES_score

print("Model Name: AlphaFold")

ES_nola = list(Alpha_ES_nola_single.values())
avg_ES_nola_single = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-single)", avg_ES_nola_single)

ES_nola = list(Alpha_ES_nola_double.values())
avg_ES_nola_double = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-double)", avg_ES_nola_double)

ES_loki = list(Alpha_ES_loki_single.values())
avg_ES_loki_single = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-single)", avg_ES_loki_single)

ES_loki = list(Alpha_ES_loki_double.values())
avg_ES_loki_double = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-double)", avg_ES_loki_double)

print(avg_ES_nola_single, avg_ES_nola_double, avg_ES_loki_single, avg_ES_loki_double)
# print(avg_ES_loki_single, avg_ES_loki_double)

"""#### RosettaFold"""

import os

# Omegafold
folder_path = "/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold"

# NOLA
Rosetta_ES_nola_single = {}
Rosetta_ES_nola_double = {}
noal_original = f'{folder_path}/IL31R_Nola_Original.pdb'
all_files = os.listdir(folder_path)
for file in all_files:
    # single-mutated
    if file.startswith("IL31R_Nola_Single_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        Rosetta_ES_nola_single[file] = ES_score
    # double-mutated
    elif file.startswith("IL31R_Nola_Double_") and file.endswith(".pdb") and file != "IL31R_Nola_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(noal_original, compare_file_path)
        Rosetta_ES_nola_double[file] = ES_score

# Loki
Rosetta_ES_loki_single = {}
Rosetta_ES_loki_double = {}
loki_original = f'{folder_path}/IL31_Loki_Original.pdb'
for file in all_files:
    if file.startswith("IL31_Loki_single_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        Rosetta_ES_loki_single[file] = ES_score
    elif file.startswith("IL31_Loki_double_") and file.endswith(".pdb") and file != "IL31_Loki_Original.pdb":
        compare_file_path = os.path.join(folder_path, file)

        ES_score = calculation_ES(loki_original, compare_file_path)
        Rosetta_ES_loki_double[file] = ES_score

print("Model Name: RosettaFold")

ES_nola = list(Rosetta_ES_nola_single.values())
avg_ES_nola = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-single)", avg_ES_nola)

ES_nola = list(Rosetta_ES_nola_double.values())
avg_ES_nola = sum(ES_nola) / len(ES_nola)
print("Average Effective Strain (Nola-double)", avg_ES_nola)

ES_loki = list(Rosetta_ES_loki_single.values())
avg_ES_loki = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-single)", avg_ES_loki)

ES_loki = list(Rosetta_ES_loki_double.values())
avg_ES_loki = sum(ES_loki) / len(ES_loki)
print("Average Effective Strain (Loki-double)", avg_ES_loki)

"""### Results table

#### ESMFold
"""

import pandas as pd

print("Model Name: ESMFold")

df_loki_double = pd.DataFrame(list(ESM_ES_loki_double.items()), columns=['Sequence', 'Effective Strain'])
df_loki_double['Mutation Type'] = 'Double'

df_loki_single = pd.DataFrame(list(ESM_ES_loki_single.items()), columns=['Sequence', 'Effective Strain'])
df_loki_single['Mutation Type'] = 'Single'

df_nola_double = pd.DataFrame(list(ESM_ES_nola_double.items()), columns=['Sequence', 'Effective Strain'])
df_nola_double['Mutation Type'] = 'Double'

df_nola_single = pd.DataFrame(list(ESM_ES_nola_single.items()), columns=['Sequence', 'Effective Strain'])
df_nola_single['Mutation Type'] = 'Single'

# Combine DataFrames
ESM_loki_data = pd.concat([df_loki_double, df_loki_single])
ESM_nola_data = pd.concat([df_nola_double, df_nola_single])


print("Antibody: Loki")
ESM_loki_data

print("Antibody: Nola")
ESM_nola_data

"""#### OmegaFold"""

import pandas as pd

print("Model Name: OmegaFold")

df_loki_double = pd.DataFrame(list(Omega_ES_loki_double.items()), columns=['Sequence', 'Effective Strain'])
df_loki_double['Mutation Type'] = 'Double'

df_loki_single = pd.DataFrame(list(Omega_ES_loki_single.items()), columns=['Sequence', 'Effective Strain'])
df_loki_single['Mutation Type'] = 'Single'

df_nola_double = pd.DataFrame(list(Omega_ES_nola_double.items()), columns=['Sequence', 'Effective Strain'])
df_nola_double['Mutation Type'] = 'Double'

df_nola_single = pd.DataFrame(list(Omega_ES_nola_single.items()), columns=['Sequence', 'Effective Strain'])
df_nola_single['Mutation Type'] = 'Single'

# Combine DataFrames
Omega_loki_data = pd.concat([df_loki_double, df_loki_single])
Omega_nola_data = pd.concat([df_nola_double, df_nola_single])

print("Antibody: Loki")
Omega_loki_data

print("Antibody: Nola")
Omega_nola_data

"""#### AlphaFold"""

import pandas as pd

print("Model Name: RosettaFold")

df_loki_double = pd.DataFrame(list(Alpha_ES_loki_double.items()), columns=['Sequence', 'Effective Strain'])
df_loki_double['Mutation Type'] = 'Double'
# df_loki_double['Antibody'] = 'Loki'

df_loki_single = pd.DataFrame(list(Alpha_ES_loki_single.items()), columns=['Sequence', 'Effective Strain'])
df_loki_single['Mutation Type'] = 'Single'
# df_loki_single['Antibody'] = 'Loki'

df_nola_double = pd.DataFrame(list(Alpha_ES_nola_double.items()), columns=['Sequence', 'Effective Strain'])
df_nola_double['Mutation Type'] = 'Double'

df_nola_single = pd.DataFrame(list(Alpha_ES_nola_single.items()), columns=['Sequence', 'Effective Strain'])
df_nola_single['Mutation Type'] = 'Single'

# Combine DataFrames
Alpha_loki_data = pd.concat([df_loki_double, df_loki_single])
Alpha_nola_data = pd.concat([df_nola_double, df_nola_single])

print("Antibody: Loki")
print(Alpha_loki_data)

print("Antibody: Nola")
Alpha_nola_data

"""#### RosettaFold"""

import pandas as pd

print("Model Name: RosettaFold")

df_loki_double = pd.DataFrame(list(Rosetta_ES_loki_double.items()), columns=['Sequence', 'Effective Strain'])
df_loki_double['Mutation Type'] = 'Double'

df_loki_single = pd.DataFrame(list(Rosetta_ES_loki_single.items()), columns=['Sequence', 'Effective Strain'])
df_loki_single['Mutation Type'] = 'Single'

df_nola_double = pd.DataFrame(list(Rosetta_ES_nola_double.items()), columns=['Sequence', 'Effective Strain'])
df_nola_double['Mutation Type'] = 'Double'

df_nola_single = pd.DataFrame(list(Rosetta_ES_nola_single.items()), columns=['Sequence', 'Effective Strain'])
df_nola_single['Mutation Type'] = 'Single'

# Combine DataFrames
Rosetta_loki_data = pd.concat([df_loki_double, df_loki_single])
Rosetta_nola_data = pd.concat([df_nola_double, df_nola_single])

print("Antibody: Loki")
Rosetta_loki_data

print("Antibody: Nola")
Rosetta_nola_data

"""#### Summary table"""

data = {
    "Model Name": ["ESMFold", "ESMFold", "ESMFold", "ESMFold", "OmegaFold", "OmegaFold", "OmegaFold", "OmegaFold", "RosettaFold", "RosettaFold", "RosettaFold", "RosettaFold", "AlphaFold", "AlphaFold", "AlphaFold", "AlphaFold"],
    "Antibody": ["Nola", "Nola", "Loki", "Loki", "Nola", "Nola", "Loki", "Loki", "Nola", "Nola", "Loki", "Loki", "Nola", "Nola", "Loki", "Loki"],
    "Mutation Type": ["Single", "Double", "Single", "Double", "Single", "Double", "Single", "Double", "Single", "Double", "Single", "Double", "Single", "Double", "Single", "Double"],
    "Avg ES Score": [0.0044189909934518268, 0.007449968529055222, 0.007121678411588941, 0.012285539172850055,
                                 0.003484402680259029, 0.005229302624595818, 0.0044219169789931935, 0.008078077486631682,
                                 0.0082048392830536, 0.010176956071124559, 0.008759510394012134, 0.014311514845380397,
                      0.011177946960730399, 0.01076222519171302, 0.008258396408918097, 0.010277533881095553
                     ]
}

df = pd.DataFrame(data)

print("Summary")
df

# @title Model Name vs Avg ES Score

from matplotlib import pyplot as plt
import seaborn as sns
figsize = (12, 1.2 * len(df['Model Name'].unique()))
plt.figure(figsize=figsize)
sns.violinplot(df, x='Avg ES Score', y='Model Name', inner='stick', palette='Dark2')
sns.despine(top=True, right=True, bottom=True, left=True)

"""### Plots

#### Nola

Nola Original vs Nola Single 3
"""

### Calculate mutliple deformation metrics
model_paths = [
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31R_Nola_Single_3_D151Y.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31R_Nola_Single_3_D151Y.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31R_Nola_Single_3_.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31R_Nola_Single_3_D151Y.pdb')
]

mutation_positions = [151]

fig, ax = plt.subplots(figsize=(14, 7))

colors = ['blue', 'orange', 'green', 'purple']  # Colors for each model
labels = ['ESMfold', 'OmegaFold', 'RosettaFold', 'AlphaFold']  # Labels for each model

# Loop through each pair of paths and process deformation metrics
for (pathA, pathB), color, label in zip(model_paths, colors, labels):

    protA = Protein(pathA)
    protB = Protein(pathB)
    deform = Deformation(protA, protB, **deform_kwargs)
    deform.run()

    # Assuming 'strain' is a method or attribute returning the strain data
    strain = deform.strain
    X = np.arange(len(strain)) + 1  # Create a sequence position array

    # Plot the data
    ax.plot(X, strain, label=label, color=color)

    for pos in mutation_positions:
        ax.axvline(x=pos, color='black', linestyle='--', linewidth=1, alpha=0.5)


# Annotate the x-axis
nstep = 10
ax.set_xticks(X[::nstep])
ax.set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
ax.set_xlabel("Protein Sequence (position / amino acid)", fontsize=14)
ax.set_ylabel('Effective Strain',  fontsize=14)
ax.legend(title_fontsize = 'large',  fontsize=14)


plt.tight_layout()
plt.show()

"""Nola Original vs Nola Double 4"""

### Calculate mutliple deformation metrics
model_paths = [
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31R_Nola_Double_4_Y174Q_S32Y.pdb'),

    ('/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31R_Nola_Double_4_Y174Q_S32Y.pdb'),

    ('/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31R_Nola_Double_4_.pdb'),

    ('/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31R_Nola_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31R_Nola_Double_4_Y174Q_S32Y.pdb')
]

mutation_positions = [32, 174]

fig, ax = plt.subplots(figsize=(14, 7))

colors = ['blue', 'orange', 'green', 'purple']  # Colors for each model
labels = ['ESMfold', 'OmegaFold', 'RosettaFold', 'AlphaFold']  # Labels for each model

# Loop through each pair of paths and process deformation metrics
for (pathA, pathB), color, label in zip(model_paths, colors, labels):

    protA = Protein(pathA)
    protB = Protein(pathB)
    deform = Deformation(protA, protB, **deform_kwargs)
    deform.run()

    # Assuming 'strain' is a method or attribute returning the strain data
    strain = deform.strain
    X = np.arange(len(strain)) + 1  # Create a sequence position array

    # Plot the data
    ax.plot(X, strain, label=label, color=color)

    for pos in mutation_positions:
        ax.axvline(x=pos, color='black', linestyle='--', linewidth=1, alpha=0.5)


# Annotate the x-axis
nstep = 10
ax.set_xticks(X[::nstep])
ax.set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
ax.set_xlabel("Protein Sequence (position / amino acid)", fontsize=14)
ax.set_ylabel('Effective Strain',  fontsize=14)
ax.legend(title_fontsize = 'large',  fontsize=14)


plt.tight_layout()
plt.show()

"""#### Loki

Loki Original vs Single 3
"""

### Calculate mutliple deformation metrics
model_paths = [
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31_Loki_Single_3_A178S.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31_Loki_Single_3_A178S.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31_Loki_single_3_.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31_Loki_Single_3_A178S.pdb')
]

mutation_positions = [178]

fig, ax = plt.subplots(figsize=(14, 7))

colors = ['blue', 'orange', 'green', 'purple']  # Colors for each model
labels = ['ESMfold', 'OmegaFold', 'RosettaFold', 'AlphaFold']  # Labels for each model

# Loop through each pair of paths and process deformation metrics
for (pathA, pathB), color, label in zip(model_paths, colors, labels):

    protA = Protein(pathA)
    protB = Protein(pathB)
    deform = Deformation(protA, protB, **deform_kwargs)
    deform.run()

    # Assuming 'strain' is a method or attribute returning the strain data
    strain = deform.strain
    X = np.arange(len(strain)) + 1  # Create a sequence position array

    # Plot the data
    ax.plot(X, strain, label=label, color=color)

    for pos in mutation_positions:
        ax.axvline(x=pos, color='black', linestyle='--', linewidth=1)


# Annotate the x-axis
nstep = 10
ax.set_xticks(X[::nstep])
ax.set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
ax.set_xlabel("Protein Sequence (position / amino acid)", fontsize=14)
ax.set_ylabel('Effective Strain',  fontsize=14)
ax.legend(title_fontsize = 'large',  fontsize=14)


plt.tight_layout()
plt.show()

"""Loki Original vs Double 4"""

### Calculate mutliple deformation metrics
model_paths = [
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31_Loki_Double_4_N31S_F149S.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31_Loki_Double_4_N31S_F149S.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31_Loki_double_4_.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31_Loki_Double_4_N31S_F149S.pdb')
]

mutation_positions = [31, 149]

fig, ax = plt.subplots(figsize=(14, 7))

colors = ['blue', 'orange', 'green', 'purple']  # Colors for each model
labels = ['ESMfold', 'OmegaFold', 'RosettaFold', 'AlphaFold']  # Labels for each model

# Loop through each pair of paths and process deformation metrics
for (pathA, pathB), color, label in zip(model_paths, colors, labels):

    protA = Protein(pathA)
    protB = Protein(pathB)
    deform = Deformation(protA, protB, **deform_kwargs)
    deform.run()

    # Assuming 'strain' is a method or attribute returning the strain data
    strain = deform.strain
    X = np.arange(len(strain)) + 1  # Create a sequence position array

    # Plot the data
    ax.plot(X, strain, label=label, color=color)

    for pos in mutation_positions:
        ax.axvline(x=pos, color='black', linestyle='--', linewidth=1)


# Annotate the x-axis
nstep = 10
ax.set_xticks(X[::nstep])
ax.set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
ax.set_xlabel("Protein Sequence (position / amino acid)", fontsize=14)
ax.set_ylabel('Effective Strain',  fontsize=14)
ax.legend(title_fontsize = 'large',  fontsize=14)


plt.tight_layout()
plt.show()

"""Loki Original vs Single 9"""

### Calculate mutliple deformation metrics
model_paths = [
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31_Loki_Single_9_G153Y.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31_Loki_Single_9_G153Y.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_rosettafold/IL31_Loki_single_9_.pdb'),
    ('/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31_Loki_Original.pdb',
     '/content/drive/MyDrive/output_omegafold_esmfold/output_alphafold/IL31_Loki_Single_9_G153Y.pdb')
]

mutation_positions = [153]

fig, ax = plt.subplots(figsize=(14, 7))

colors = ['blue', 'orange', 'green', 'purple']  # Colors for each model
labels = ['ESMfold', 'OmegaFold', 'RosettaFold', 'AlphaFold']  # Labels for each model

# Loop through each pair of paths and process deformation metrics
for (pathA, pathB), color, label in zip(model_paths, colors, labels):

    protA = Protein(pathA)
    protB = Protein(pathB)
    deform = Deformation(protA, protB, **deform_kwargs)
    deform.run()

    # Assuming 'strain' is a method or attribute returning the strain data
    strain = deform.strain
    X = np.arange(len(strain)) + 1  # Create a sequence position array

    # Plot the data
    ax.plot(X, strain, label=label, color=color)

    for pos in mutation_positions:
        ax.axvline(x=pos, color='black', linestyle='--', linewidth=1)


# Annotate the x-axis
nstep = 10
ax.set_xticks(X[::nstep])
ax.set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
ax.set_xlabel("Protein Sequence (position / amino acid)", fontsize=14)
ax.set_ylabel('Effective Strain',  fontsize=14)
ax.legend(title_fontsize = 'large',  fontsize=14)


plt.tight_layout()
plt.show()

"""## ORIGINAL CODE"""

# Commented out IPython magic to ensure Python compatibility.
### Loading the data for the tutorial
# %cd /content
!git clone https://github.com/mirabdi/PDAnalysis.git

# Change directory into the PDAnalysis repository
# %cd /content/PDAnalysis/
!git pull origin main
!ls

# The following paths lead to structures from the AlphaFold Database,
# for human and gorilla Lysozyme C
# pathA = '/content/IL31R_Nola_Original.pdb'
# pathB = '/content/IL31R_Nola_Double_1.pdb'


# If you wish to calculate strain using your own files,
# replace this code block with paths to your own files
# that you have uploaded to Google drive, for example:
#pathA = 'myDrive/myProtein/protein_A.pdb'
#pathB = 'myDrive/myProtein/protein_B.pdb'

# For reference, the structure of the data used in this analysis can be found here:
# https://github.com/mirabdi/PDAnalysis/tree/main/test_data/Lysozyme

# Install PDAnalysis and load modules
!pip install PDAnalysis --upgrade
from PDAnalysis import Protein, AverageProtein, Deformation
import matplotlib.pyplot as plt
import numpy as np

# Setting the parameters to use in the deformation calculation

# We will include residues in local neighborhoods if their Alpha-carbon
# positions are within 13 Angstroms of each other (neigh_cut).

# We will use a exclude any residues with pLDDT lower than 70 (min_plddt).
# This is only appropriate for AlphaFold-generated structures.
# protein_kwargs = {"neigh_cut":13.0, "min_plddt":70}

# For each residue we will calculate Effective Strain (strain),
# and the distance to the nearest mutated residue (mut_dist)
deform_kwargs = {'method':'all'}

### Calculate mutliple deformation metrics
pathA = '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31R_Nola_Original.pdb'
pathB = '/content/drive/MyDrive/output_omegafold_esmfold/output_esmfold/IL31R_Nola_Double_1_F55S_S144A.pdb'

# Load each protein, with the parameters specified before (protein_kwargs)
# protA = Protein(pathA, **protein_kwargs)
# protB = Protein(pathB, **protein_kwargs)
protA = Protein(pathA)
protB = Protein(pathB)

# Initialize the Deformation object
deform = Deformation(protA, protB, **deform_kwargs)
# Run the calculations outlined in deform_kwargs['method']
deform.run()

metrics = ["Effective Strain", "Shear Strain", "Non-affine Strain",
           "LDDT", "LDD", "Neighborhood Distance", "RMSD"]
deformation_metrics = [deform.strain, deform.shear, deform.non_affine,
                       deform.lddt, deform.ldd, deform.neighbor_distance,
                       deform.rmsd_per_residue]

fig, ax = plt.subplots(len(deformation_metrics), 1, figsize=(12,14))
fig.subplots_adjust(hspace=0.7)
X = np.arange(protA.seq_len) + 1
for i, dm in enumerate(deformation_metrics):
    print(metrics[i], ':', np.nanmean(dm))
    ax[i].plot(X, dm)

    # Annotate the x-axis
    nstep = 10
    ax[i].set_xticks(X[::nstep])
    ax[i].set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
    ax[i].set_xlabel("Protein Sequence (position / amino acid)")
    ax[i].set_ylabel(metrics[i])

### Calculate mutliple deformation metrics
pathA = '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31R_Nola_Original.pdb'
pathB = '/content/drive/MyDrive/output_omegafold_esmfold/output_omegafold/IL31R_Nola_Double_1_F55S_S144A.pdb'

# Load each protein, with the parameters specified before (protein_kwargs)
# protA = Protein(pathA, **protein_kwargs)
# protB = Protein(pathB, **protein_kwargs)
protA = Protein(pathA)
protB = Protein(pathB)

# Initialize the Deformation object
deform = Deformation(protA, protB, **deform_kwargs)
# Run the calculations outlined in deform_kwargs['method']
deform.run()

metrics = ["Effective Strain", "Shear Strain", "Non-affine Strain",
           "LDDT", "LDD", "Neighborhood Distance", "RMSD"]
deformation_metrics = [deform.strain, deform.shear, deform.non_affine,
                       deform.lddt, deform.ldd, deform.neighbor_distance,
                       deform.rmsd_per_residue]

fig, ax = plt.subplots(len(deformation_metrics), 1, figsize=(12,14))
fig.subplots_adjust(hspace=0.7)
X = np.arange(protA.seq_len) + 1
for i, dm in enumerate(deformation_metrics):
    print(metrics[i], ':', np.nanmean(dm))
    ax[i].plot(X, dm)

    # Annotate the x-axis
    nstep = 10
    ax[i].set_xticks(X[::nstep])
    ax[i].set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
    ax[i].set_xlabel("Protein Sequence (position / amino acid)")
    ax[i].set_ylabel(metrics[i])

### LDDT thresholds can be modified to make it more sensitive to small changes

# Default thresholds = [0.5, 1, 2, 4]
deform_kwargs = {'method':'lddt'}
deform = Deformation(protA, protB, **deform_kwargs)
deform.run()
lddt_original = deform.lddt

deform_kwargs = {'method':'lddt', 'lddt_cutoffs':[0.125, 0.25, 0.5, 1]}
deform = Deformation(protA, protB, **deform_kwargs)
deform.run()
lddt_sensitive = deform.lddt

fig, ax = plt.subplots()
ax.plot(X, lddt_original, label='original LDDT')
ax.plot(X, lddt_sensitive, label='sensitive LDDT')
ax.legend(loc='best', frameon=False)

# Annotate the x-axis
ax.set_xticks(X[::nstep])
ax.set_xticklabels([f"{i}\n{s}" for i, s in enumerate(protA.sequence) if (i % nstep == 0)])
ax.set_xlabel("Protein Sequence (position / amino acid)")
ax.set_ylabel("LDDT")