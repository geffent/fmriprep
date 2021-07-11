# fMRIprep

### heudiconv command
`heudiconv -d /mnt/s/.../DICOM/{subject}/*/* -o ~/data/bids/ -f ~/code/fmriprep/heuristic.py -s SUBJECTID1 SUBJECT2 -ss T1 -c dcm2niix -b --minmeta --overwrite`

### or better yet:
```
subjectIDs = ($(cat ~/data/subjectIDs.txt))
heudiconv -d /mnt/s/.../DICOM/{subject}/*/* -o ~/data/bids/ -f ~/code/fmriprep/heuristic.py -s "${subjectIDs[@]}" -c dcm2niix -b --minmeta --overwrite
```
