### FOR SHERLOCK ###

from pathlib import Path
import subprocess   
import os

project_data_root = 'data'
os.makedirs(project_data_root, exist_ok = True)
study_root = '/oak/stanford/groups/nolanw/TBI/PP_BOLD/PP_USE_IN_ANALYSIS'
visits = ['V2', 'V3', 'V4']
# subjects under visit folder: 54095s0xx
# we want the resting state scans, ending in *_bold.nii
# copy them to project dir, /data/{sub}/{visit}/*

for visit in visits[1:]:
    visit_dir = os.path.join(study_root, visit)
    print('\n=====\n', visit_dir, '\n=====\n')
    for sub in os.listdir(visit_dir):
        if '54095s' in sub:
            print('\n=====\n', sub, '\n=====\n')
            try:
                sub_dir = os.path.join(visit_dir, sub)
                for filename in os.listdir(sub_dir):
                    if '_desc-preproc_bold.nii' in filename:
                        try:
                            file_path = os.path.join(sub_dir, filename)
                            src = Path(file_path)
                            os.makedirs(os.path.join(project_data_root, sub), exist_ok = True)
                            os.makedirs(os.path.join(project_data_root, sub, visit), exist_ok = True)
                            dst_dir = Path(os.path.join(project_data_root, sub, visit))
                            dst = dst_dir / src.name      
                            subprocess.run(["cp", "-p", str(src), str(dst_dir)], check=True)
                            print("Copied to:", dst_dir / src.name)
                        except:
                            print('Cannot copy ', sub, visit, filename)
            except:
                print('')