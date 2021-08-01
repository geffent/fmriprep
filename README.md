# fMRIprep

### heudiconv command
` heudiconv --dicom_dir_template .../DICOM_raw_data/{subject}{session}_*/*/* --outdir ~/data/bids/ --heuristic /home/tal/code/fmriprep/heuristic.py --subjects BS001 --ses T1 -c dcm2niix -b --minmeta --overwrite`

`heudiconv -d /mnt/s/.../DICOM/{subject}/*/* -o ~/data/bids/ -f ~/code/fmriprep/heuristic.py -s SUBJECTID1 SUBJECTID2 -ss T1 -c dcm2niix -b --minmeta --overwrite`

### or better yet:
```
subjectIDs = ($(cat ~/data/subjectIDs.txt))
heudiconv -d /mnt/s/.../DICOM/{subject}/*/* -o ~/data/bids/ -f ~/code/fmriprep/heuristic.py -s "${subjectIDs[@]}" -c dcm2niix -b --minmeta --overwrite
```
