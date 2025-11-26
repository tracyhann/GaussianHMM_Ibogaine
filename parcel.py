import nibabel as nib
from nilearn import image
import numpy as np
import pandas as pd
from nilearn.maskers import NiftiLabelsMasker

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

idxs = [order - 1 for order in dmn_map.keys()]


ex_bold_path = 'data/sub-54095s001/filtreg_sm_dspk_sk_sub-54095s001_ses-V2_task-Resting1NewHB6scan_space-MNI152NLin2009cAsym_desc-preproc_bold.nii'
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

data = []
T_t = []

sub_fmri = {'sub-54095s001':['data/sub-54095s001/filtreg_sm_dspk_sk_sub-54095s001_ses-V2_task-Resting1NewHB6scan_space-MNI152NLin2009cAsym_desc-preproc_bold.nii',
                             'data/sub-54095s001/filtreg_sm_dspk_sk_sub-54095s001_ses-V2_task-Resting2NewHB6scan_space-MNI152NLin2009cAsym_desc-preproc_bold.nii']}
start, end = 0, 0

for sub in sub_fmri.keys():
    bold_paths = sub_fmri[sub]
    T_t.append([start,end])
    for bold_path in bold_paths:
        bold_img = nib.load(bold_path)
        dts = generate_dmn_ts(bold_img, atlas_resamp_img, idxs)
        data.append(dts)
        T_t[-1][1] += dts.shape[0]

np.concat()

data = np.concat(data)
np.save('ts/data.npy', data)
T_t = np.array(T_t)
np.save('ts/T_t.npy', T_t)