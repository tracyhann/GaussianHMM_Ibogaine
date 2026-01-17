import nibabel as nib
from nilearn import image
import numpy as np
import pandas as pd
from nilearn.maskers import NiftiLabelsMasker
import os

# Path /oak/stanford/groups/nolanw/TBI/PP_BOLD/PP_USE_IN_ANALYSIS
os.makedirs('ts', exist_ok=True)

def generate_dmn_ts(bold_img, atlas_resamp_img, dmn_idxs):
    print("resampled atlas:", atlas_resamp_img.shape)   
    print("bold:", bold_img.shape)

    masker = NiftiLabelsMasker(
    labels_img=atlas_resamp_img,
    standardize=True,        # optional, z-score per region
    detrend=True             
)

    ts = masker.fit_transform(bold_img)
    ts_parcels = ts.T   # shape (200, 369)
    dts = ts_parcels[dmn_idxs].T # 1 subject T x feature (network nodes), 369, 37

    return dts



map = pd.read_csv('atlas/schaefer2018_200parcels_17networks_order.csv')
# Default 75-98, 184-196
dmn_map = {}
for i, row in map.iterrows():
    if 'Default' in row['network']:
        dmn_map[row['order']] = row['network']
dmn_map
idxs = [order - 1 for order in dmn_map.keys()]
dmn_idx = {}
for i, val in enumerate(dmn_map.values()):
    dmn_idx[i] = val 
pd.DataFrame.from_dict(dmn_idx, orient='index').to_csv('atlas/schaefer2018_DMNrois.csv')


root = 'data'

sub_fmri = {}
for sub in os.listdir(root):
    if '54095s' in sub:
        sub_fmri[sub] = []
        sub_dir = os.path.join(root, sub)
        for visit in os.listdir(sub_dir):
            visit_func_dir = os.path.join(sub_dir, visit)
            for file in os.listdir(visit_func_dir):
                if '_desc-preproc_bold.nii' in file:
                    sub_fmri[sub].append(os.path.join(visit_func_dir, file))
sub_fmri
ex_bold_path = list(sub_fmri.items())[0][1][0] # first subject first path as example for checkpoint
bold_img = nib.load(ex_bold_path)
atlas_path = 'atlas/Schaefer2018_200Parcels_17Networks_order_FSLMNI152_1mm.nii.gz'
atlas_img = nib.load(atlas_path) # 3D: 182 x 218 x 182
# Resample atlas into BOLD grid (nearest to keep integer labels)
atlas_resamp_img = image.resample_to_img(
    atlas_img,
    bold_img,
    interpolation='nearest'
)

print('bold_img.shape', bold_img.shape)
print('atlas_img.shape', atlas_img.shape)
print('atlas_resamp_img.shape', atlas_resamp_img.shape)


start, end = 0, 0
data = []
T_t = []
num_sub = len(list(sub_fmri.keys()))
i = 1
for sub in sub_fmri.keys():
    print(f'\n{i}/{num_sub}  Subject: ', sub)
    bold_paths = sub_fmri[sub]
    for bold_path in bold_paths:
        print('Loading: ', bold_path)
        bold_img = nib.load(bold_path)
        dts = generate_dmn_ts(bold_img, atlas_resamp_img, idxs)
        data.append(dts)
        end += dts.shape[0]
        T_t.append([int(start),int(end)])
        start = end
    i += 1

data = np.concat(data)
np.save('ts/data.npy', data)
T_t = np.array(T_t)
np.save('ts/T_t.npy', T_t)
