import numpy as np
import os
import pickle


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
print(sub_fmri)

start, end = 0, 0
T_t_visits = {'V2': [], 'V3': [], 'V4': []}
for sub in sub_fmri.keys():
    ts_visits = sub_fmri[sub]
    v2, v3, v4 = 0, 0, 0
    for ts in ts_visits:
        if 'V2' in ts:
            v2 += 1
        if 'V3' in ts:
            v3 += 1
        if 'V4' in ts:
            v4 += 1
    print(sub, v2, v3, v4)
    T_t_visits['V2'].append([int(start), int(v2*369+start)])
    start = int(v2*369+start)
    T_t_visits['V3'].append([int(start), int(v3*369+start)])
    start = int(v3*369+start)
    T_t_visits['V4'].append([int(start), int(v4*369+start)])
    start = int(v4*369+start)

print(T_t_visits)


np.save('ts/T_t_visits.npy', T_t_visits)

with open('ts/T_t_visits.pkl', 'wb') as f:
    pickle.dump(T_t_visits, f)

