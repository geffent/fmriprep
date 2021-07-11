import os
import numpy as np

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):

    anat_t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
    func_mid1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MID_run-1_bold')
    func_mid2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MID_run-2_bold')
    func_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-resting_bold')
    func_reversal = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-reversal_bold')
    fm_AP_mid = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_task-MID_epi')
    fm_PA_mid = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_task-MID_epi')
    fm_AP_rest = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_task-resting_epi')
    fm_PA_rest = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_task-resting_epi')
    fm_AP_reversal = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_task-reversal_epi')
    fm_PA_reversal = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_task-reversal_epi')

    info = {
        anat_t1w: [],
        func_mid1: [],
        func_mid2: [],
        func_rest: [],
        func_reversal: [],
        fm_AP_mid: [],
        fm_PA_mid: [],
        fm_AP_rest: [],
        fm_PA_rest: [],
        fm_AP_reversal: [],
        fm_PA_reversal: []
    }

    fmap_candidates_id = {'AP': [], 'PA': []}
    fmap_keys = {'AP': fm_AP_mid, 'PA': fm_PA_mid}
    
    ### Get all series ID of interest
    ### For fieldmaps, only get candidates
    for s in seqinfo: 
        # python debugger which allows you to breakpoint and look around in the running program:
        # import pdb; pdb.set_trace()
        if '008_t1_mprage' in s.dcm_dir_name.lower():
            info[anat_t1w].append(s.series_id)
#        if '012_fmri_mid' in s.dcm_dir_name.lower():
#            info[func_mid1].append(s.series_id)
#        if '013_fmri_mid' in s.dcm_dir_name.lower():
#            info[func_mid2].append(s.series_id)
        if 'resting' in s.dcm_dir_name.lower():
            info[func_rest].append(s.series_id)
#        if 'reversal' in s.dcm_dir_name.lower():
#            info[func_reversal].append(s.series_id)
#        if '005_SpinEchoFieldMap_AP' in s.dcm_dir_name:
#            info[fm_AP_reversal].append(s.series_id)
#        if '006_SpinEchoFieldMap_PA' in s.dcm_dir_name:
#            info[fm_PA_reversal].append(s.series_id)
#        if '014_SpinEchoFieldMap_AP' in s.dcm_dir_name:
#            info[fm_AP_rest].append(s.series_id)
#        if '015_SpinEchoFieldMap_PA' in s.dcm_dir_name:
#            info[fm_PA_rest].append(s.series_id)
#        if '010_SpinEchoFieldMap_AP' in s.dcm_dir_name:
#            info[fm_AP_mid].append(s.series_id)
#        if '011_SpinEchoFieldMap_PA' in s.dcm_dir_name:
#            info[fm_PA_mid].append(s.series_id)

        # if ('AP' in s.protocol_name) and ('NORM' in s.image_type):
        #     fmap_candidates_id['AP'].append(s.series_id)
        # if ('PA' in s.protocol_name) and ('NORM' in s.image_type):
        #     fmap_candidates_id['PA'].append(s.series_id)

    ### Now select correct fieldmaps within candidates,
    ### i.e. those with the closest sequence id after the 2nd run of the task fmri

    # # Get integer id of the run of the resting fmri sequence
    # fmri_rest_id_int = int(fmri_rest_id.split('-')[0])
    # # For each acquisition direction, find the correct sequence id and save it into info dict
    # for acq_dir in ['AP', 'PA']:
    #     candidate_ids = fmap_candidates_id[acq_dir]
    #     # For fieldmap candidates, get integer id as well as associated full sequence id
    #     if len(candidate_ids) != 0:
    #         candidate_ids_int = {int(cid.split('-')[0]): cid for cid in candidate_ids}
    #     else:
    #         raise ValueError("Empty list of candidate field maps.")
    #     # Get minimum id after eliminating those occuring before fmri seq id
    #     fmap_id_int = [cid for cid in candidate_ids_int.keys() if (fmri_rest_id_int - cid) in [1,2]][0]
    #     # Save identified fieldmap using the correct key according to the acquisition direction
    #     info[fmap_keys[acq_dir]].append(candidate_ids_int[fmap_id_int])

    return info


    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group

    heudiconv -d {subject}/scans/DICOM/*/* -o bids/ -f convertall -s GS001T1 -c none
    heudiconv -d {subject}/scans/DICOM/*/* -o {subject}/scans/ -f bids/code/heuristic_v1.py -s GS001T1 -c dcm2niix -b --minmeta --overwrite

    anat_t1w = create_key('anat/{subject}_T1w')
    func_mid1 = create_key('func/{subject}_task-MID_run-1_bold')
    func_mid2 = create_key('func/{subject}_task-MID_run-2_bold')
    fm_AP = create_key('fmap/{subject}_fieldmap_epi_AP')
    fm_PA = create_key('fmap/{subject}_fieldmap_epi_PA')

    info = {anat_t1w: [], func_mid1: [], func_mid2: [], fm_AP: [], fm_PA: []}

        if ('mprage' in s.protocol_name):
            info[anat_t1w].append(s.series_id)
        if ('MID' in s.protocol_name) and ('1' in s.protocol_name):
            info[func_mid1].append(s.series_id)
        if ('MID' in s.protocol_name) and ('2' in s.protocol_name):
            info[func_mid2].append(s.series_id)
        if ('FieldMap' in s.protocol_name) and ('AP' in s.protocol_name):
            info[fm_AP].append(s.series_id)
        if ('FieldMap' in s.protocol_name) and ('PA' in s.protocol_name):
            info[fm_PA].append(s.series_id)

        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
    """
