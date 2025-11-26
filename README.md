This repo experimented a state analysis model using Hidden Markov Model (HMM), using the code from a public repo: https://github.com/vidaurre/glhmm/blob/main/docs/notebooks/GaussianHMM_example.ipynb

`parcel.py`
- Concatnated the sub-54095s001_ses-V2 resting state data (2 x 6 minutes fMRI scans at resting state). Each scan has 369 T, and is registered to the MNI152 space.
- Parcellated by Schaefer2018 200 ROIs x 17 Networks atlas. To standardize the dimensions between the template and raw data, the atlas (182, 218, 182) is sampled using nearest neighbor to the same dimensions of the fMRI (108, 128, 108).
- 37 ROIs of the Default Mode Network (DMN) are kept for analysis.



<pre>
.
├── atlas
│   ├── Schaefer2018_200Parcels_17Networks_order_FSLMNI152_1mm.nii.gz
│   ├── Schaefer2018_200Parcels_17Networks_order_FSLMNI152_2mm.nii.gz
│   └── schaefer2018_200parcels_17networks_order.csv
├── data
│   ├── 54095s001.zip
│   └── sub-54095s001
│       ├── 54095s001_V2_task-Resting1NewHB6scan_FD_INFO.mat
│       ├── 54095s001_V2_task-Resting2NewHB6scan_FD_INFO.mat
│       ├── filtreg_sm_dspk_sk_sub-54095s001_ses-V2_task-Resting1NewHB6scan_space-MNI152NLin2009cAsym_desc-preproc_bold.nii
│       └── filtreg_sm_dspk_sk_sub-54095s001_ses-V2_task-Resting2NewHB6scan_space-MNI152NLin2009cAsym_desc-preproc_bold.nii
├── GaussianHMM_example_in DMN\nsub-54095s001_ses-V2.ipynb - Colab.pdf
├── parcel.py
├── README.md
└── ts
    ├── data.npy
    └── T_t.npy
</pre>