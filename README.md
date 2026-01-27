This repo experimented a state analysis model using Hidden Markov Model (HMM), using the code from: https://github.com/vidaurre/glhmm/blob/main/docs/notebooks/GaussianHMM_example.ipynb

## Info
- N = 29 subjects expected at 3 visits, V = {V2, V3, V4}. 
- V2: Baseline pre-treatment; V3: 1 week post-treatment; V4: 1 month post-treatment (yes, some people are missing data; see table below).
- Each run of rs-fMRI is 6-minutes long, producing timeseries of T = 369 timepoints. 
- Each visit collects 2 rs-fMRI runs, producing timeseries of T = 2 x 369 = 738 timepoints per visit.


<pre>
subject    V2   V3   V4
------------------------
54095s001  738  738  738
54095s002  738  738  738
54095s003  738  738  738
54095s004  738  738  738
54095s005  738  738  738
54095s006  738  738  738
54095s007  738  738  738
54095s008  738  738    0
54095s009  738  738  738
54095s010  738  738    0
54095s011  738  738  738
54095s012  738    0    0
54095s013  738  738  738
54095s014  738  738  738
54095s015  738  738  738
54095s016  738  738  738
54095s017  738  738  738
54095s018  738  738  738
54095s019  738  738  738
54095s020  738  738  738
54095s021  738  738  738
54095s022  738  738    0
54095s023  738  738  738
54095s024  738  738  738
54095s025  738  738  738
54095s026  738  738  738
54095s027  738  738  738
54095s028  738  738  738
54095s029  738  738  738
</pre>

## Project organization
<pre>
.
├── all_sub_by_visits   # HMM model analysis outputs
│   ├── FO  # shaped (29, 4); Fractional Occupancy of K=4 states per subject per visit in DMN ROIs
│   │   ├── all_sub_DMN_FO_V2.npy
│   │   ├── all_sub_DMN_FO_V3.npy
│   │   └── all_sub_DMN_FO_V4.npy
│   ├── SR  # shaped (29, 4); Switching Rates of K=4 states per subject per visit in DMN ROIs
│   │   ├── all_sub_DMN_SR_V2.npy
│   │   ├── all_sub_DMN_SR_V3.npy
│   │   └── all_sub_DMN_SR_V4.npy
│   └── TS  # shaped (29, 738, 37); 738-D rs-fMRI time series of 37 DMN ROIs per subject per visit
│       ├── all_sub_DMN_TS_V2.npy
│       ├── all_sub_DMN_TS_V3.npy
│       └── all_sub_DMN_TS_V4.npy
├── atlas
│   ├── Schaefer2018_200Parcels_17Networks_order_FSLMNI152_1mm.nii.gz
│   ├── Schaefer2018_200Parcels_17Networks_order_FSLMNI152_2mm.nii.gz
│   ├── schaefer2018_200parcels_17networks_order.csv
│   └── schaefer2018_DMNrois.csv
├── data
│   ├── 54095s0*
│   │   ├── ses-V2
│   │   ├── ses-V3
│   │   └── ses-V4
│   ├── ...
│   │   ...
├── DMN_GaussianHMM_all_subjects.ipynb  # HMM notebook; hit 'run all' to reproduce analysis
├── hmm # HMM training outputs
│   ├── FE.pkl
│   ├── Gamma.pkl
│   ├── hmm.pkl # HMM model config
│   └── Xi.pkl
├── parcel.py
├── README.md
└── ts  # outputs of parcel.py
    ├── data.npy    # concatenated TS
    ├── T_t_visits.pkl  # T indices by visits
    └── T_t.npy # concatenated T indices
</pre>


## Scripts
### `parcel.py`
- Concatnated resting state data of all 29 subjects.
- Parcellated by Schaefer2018 200 ROIs x 17 Networks atlas. To standardize the dimensions between the template and raw data, the atlas (182, 218, 182) is sampled using nearest neighbor to the same dimensions of the fMRI (108, 128, 108).
- 37 ROIs of the Default Mode Network (DMN) are kept for HMM analysis.
- .csv in atlas converted from [.txt](https://github.com/ThomasYeoLab/CBIG/blob/v0.14.3-Update_Yeo2011_Schaefer2018_labelname/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/Schaefer2018_200Parcels_17Networks_order.txt)
- Outputs saved in ./ts . Ready for HMM analysis.

### `DMN_GaussianHMM_all_subjects.ipynb`
- HMM analysis. 
- Code adopted from: https://github.com/vidaurre/glhmm/blob/main/docs/notebooks/GaussianHMM_example.ipynb
- Hit `run all` to reproduce analysis and plots. 
- Outputs model training results to `hmm/*` (`hmm.zip`) and analysis results to `all_sub_by_visits/*` (`all_sub_by_visits.zip`).

