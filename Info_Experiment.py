import numpy as np
import pandas as pd

def condition_by_session(animal, list_sessions='all'):

    if animal == 'Ent_CamK2_03':
        condition_by_session = {'S01': 'PTZ error', 'S02': 'Dz 5mg/kg', 'S03': 'NaCl',
                                'S04':  'NaCl','S05':  'Dz 5mg/kg', 'S06': 'PTZ error',
                                'S07': 'PTZ error', 'S08': 'NaCl','S09': 'Dz 5mg/kg',
                                'S10': 'NaCl', 'S11':'PTZ error', 'S12': 'Dz 5mg/kg',
                                'S13': 'NaCl', 'S14': 'Dz 5mg/kg', 'S15': 'Bic 1mg/kg',
                                'S16': 'NaCl', 'S17':  'Bic 0.5mg/kg'}

    elif animal == 'Ent_CamK2_04':
        condition_by_session = {'S01': 'NaCl', 'S02': 'Dz 5mg/kg', 'S03': 'PTZ error', 'S04': 'PTZ error',
                                'S05': 'Dz 5mg/kg', 'S06': 'NaCl', 'S07': 'PTZ error', 'S08':'Dz 5mg/kg',
                                'S09': 'NaCl', 'S10': 'PTZ error', 'S11': 'Dz 5mg/kg', 'S12': 'NaCl',
                                'S13': 'Dz 5mg/kg', 'S14': 'NaCl', 'S15': 'Bic 1mg/kg',
                                'S16': 'NaCl', 'S17': 'Bic 0.5mg/kg',
                                'S18': 'NaCl', 'S19': 'Bic 0.5mg/kg'}

    elif animal == 'Ent_CamK2_06':
        condition_by_session = {'S01': 'Dz 5mg/kg', 'S02': 'PTZ error', 'S03': 'NaCl',
                                'S04': 'NaCl', 'S05': 'PTZ error', 'S06': 'Dz 5mg/kg',
                                'S07': 'NaCl', 'S08': 'Dz 5mg/kg','S09': 'PTZ error',
                                'S10':  'Dz 5mg/kg', 'S11': 'PTZ error', 'S12': 'NaCl',
                                'S13': 'Bic 2mg/kg', 'S14': 'NaCl', 'S15':  'Dz 5mg/kg', 'S16': 'Bic 0.5mg/kg',
                                }

    elif animal == 'Ent_CamK2_07':
        condition_by_session = {'S01': 'NaCl', 'S02': 'Dz 5mg/kg', 'S03': 'PTZ error', 'S04':  'Dz 5mg/kg',
                                'S05': 'NaCl', 'S06': 'PTZ error', 'S07': 'Dz 5mg/kg', 'S08': 'NaCl',
                                'S09': 'PTZ error', 'S10': 'Dz 5mg/kg', 'S11': 'NaCl', 'S12': 'PTZ error', "S13": 'Bic 2mg/kg'}


    elif animal == 'Ent_CamK2_09':
        condition_by_session={'S01': 'PTZ 20mg/kg', 'S02': 'PTX 0.75mg/kg', 'S03' : 'NaCl','S04': 'Dz 5mg/kg',
                              'S05': 'PTZ 20mg/kg','S06':  'NaCl', 'S07': 'Dz 5mg/kg', 'S08': 'PTX 0.75mg/kg',
                              'S09': 'PTZ 20mg/kg','S10':  'NaCl', 'S11': 'Dz 5mg/kg', 'S12': 'PTX 0.75mg/kg',
                              'S13': 'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_10':
        condition_by_session={'S01': 'PTX 0.75mg/kg', 'S02': 'NaCl', 'S03': 'Dz 5mg/kg', 'S04': 'PTZ 20mg/kg',
                              'S05': 'Dz 5mg/kg', 'S06': 'PTZ 20mg/kg', 'S07': 'PTX 0.75mg/kg', 'S08': 'NaCl',
                              'S09': 'Dz 5mg/kg', 'S10': 'PTZ 20mg/kg', 'S11': 'PTX 0.75mg/kg', 'S12': 'NaCl',
                              'S13': 'Dz 5mg/kg', 'S14': 'PTZ 20mg/kg', 'S15': 'PTX 0.75mg/kg', 'S16': 'NaCl',
                              'S17': 'Dz 3mg/kg', 'S18': 'NaCl', 'S19': 'Dz 1mg/kg', 'S20': 'Dz 7mg/kg',
                              'S21': 'NaCl', 'S22': 'PTZ 20mg/kg', 'S23': 'Dz 5mg/kg', 'S24': 'PTX 0.75mg/kg'
                              }

    elif animal == 'Ent_CamK2_11':
        condition_by_session={'S01': 'PTX 0.75mg/kg', 'S02': 'PTZ 20mg/kg', 'S03': 'NaCl', 'S04': 'Dz 5mg/kg',
                              'S05': 'PTZ 20mg/kg', 'S06': 'NaCl', 'S07': 'Dz 5mg/kg', 'S08': 'PTX 0.75mg/kg',
                              'S09': 'PTZ 20mg/kg', 'S10': 'NaCl', 'S11': 'Dz 5mg/kg', 'S12': 'PTX 0.75mg/kg',
                              'S13': 'PTX 0.75mg/kg', 'S14': 'Dz 5mg/kg', 'S15': 'PTZ 20mg/kg', 'S16': 'NaCl',
                              'S17': 'Dz 1mg/kg', 'S18': 'Dz 7mg/kg', 'S19': 'Dz 3mg/kg', 'S20': 'NaCl',
                              'S21': 'Dz 5mg/kg', 'S22': 'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_12':
        condition_by_session={'S01': 'Dz 5mg/kg', 'S02': 'PTX 0.75mg/kg', 'S03' : 'NaCl', 'S04': 'PTZ 20mg/kg',
                              'S05' : 'PTX 0.75mg/kg','S06' : 'Dz 5mg/kg', 'S07': 'PTZ 20mg/kg', 'S08' : 'NaCl',
                              'S09' : 'PTX 0.75mg/kg', 'S10': 'Dz 5mg/kg', 'S11': 'PTZ 20mg/kg', 'S12': 'NaCl',
                              'S13': 'NaCl', 'S14':  'PTZ 20mg/kg', 'S15':  'Dz 5mg/kg', 'S16': 'PTX 0.75mg/kg',
                              'S17': 'Dz 3mg/kg', 'S18': 'NaCl', 'S19': 'Dz 1mg/kg', 'S20': 'Dz 7mg/kg',
                              'S21': 'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_13':
        condition_by_session={'SP_ID50' : None}

    elif animal == 'Ent_CamK2_14':
        condition_by_session={'SP_ID50' : None}

    elif animal == 'Ent_CamK2_15':
        condition_by_session={'S01': 'PTZ 20mg/kg', 'S02':'Dz 5mg/kg','S03' : 'NaCl', 'S04' :'PTX 0.75mg/kg',
                              'S05' : 'NaCl', 'S06' : 'Dz 5mg/kg', 'S07': 'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_16':
        condition_by_session = {'S01': 'PTX 0.75mg/kg', 'S02': 'PTZ 20mg/kg', 'S03' : 'Dz 5mg/kg','S04':  'NaCl',
                                'S05' : 'Dz 5mg/kg', 'S06':  'NaCl','S07':  'PTZ 20mg/kg','S08': 'PTX 0.75mg/kg',
                                'S09' : 'Dz 5mg/kg', 'S10': 'PTZ 20mg/kg', 'S11': 'NaCl', 'S12': 'PTX 0.75mg/kg',
                                'S13': 'Dz 5mg/kg', 'S14': 'NaCl', 'S15': 'PTZ 20mg/kg', 'S16': 'PTX 0.75mg/kg',
                                'S17': 'Dz 7mg/kg', 'S18': 'Dz 1mg/kg', 'S19': 'Dz 3mg/kg', 'S20': 'NaCl',
                                'S21': 'PTX 0.75mg/kg', 'S22': 'Dz 5mg/kg', 'S23': 'PTZ 20mg/kg', 'S24': 'NaCl'}

    elif animal == 'Ent_CamK2_17':
        condition_by_session = {'S01': 'PTX 0.75mg/kg', 'S02': 'PTZ 20mg/kg', 'S03' : 'Dz 5mg/kg', 'S04' : 'NaCl',
                                'S05': 'PTZ 20mg/kg', 'S06' : 'NaCl', 'S07' : 'Dz 5mg/kg', 'S08': 'PTX 0.75mg/kg',
                                'S09': 'NaCl', 'S10': 'Dz 5mg/kg', 'S11': 'PTZ 20mg/kg', 'S12': 'PTX 0.75mg/kg',
                                'S13': 'PTZ 20mg/kg', 'S14': 'NaCl', 'S15': 'Dz 5mg/kg', 'S16': 'PTX 0.75mg/kg',
                                'S17': 'NaCl', 'S18': 'Dz 3mg/kg', 'S19': 'Dz 1mg/kg', 'S20': 'Dz 7mg/kg',
                                'S21': 'PTZ 20mg/kg', 'S22': 'NaCl', 'S23': 'Dz 5mg/kg', 'S24': 'PTX 0.75mg/kg'
                                }

    elif animal == 'Ent_CamK2_18':
        condition_by_session = {'S01': 'PTX 0.75mg/kg', 'S02': 'PTZ 20mg/kg', 'S03' : 'Dz 5mg/kg', 'S04' : 'NaCl',
                                'S05': 'Dz 5mg/kg', 'S06' : 'PTZ 20mg/kg', 'S07' : 'PTX 0.75mg/kg', 'S08': 'NaCl',
                                'S09': 'Dz 5mg/kg', 'S10': 'PTX 0.75mg/kg', 'S11': 'NaCl', 'S12': 'PTZ 20mg/kg',
                                'S13': 'Dz 5mg/kg', 'S14': 'PTZ 20mg/kg', 'S15': 'PTX 0.75mg/kg', 'S16': 'NaCl',
                                'S17': 'Dz 1mg/kg', 'S18': 'NaCl', 'S19': 'Dz 3mg/kg', 'S20': 'Dz 7mg/kg',
                                'S21': 'Dz 5mg/kg', 'S22': 'NaCl', 'S23': 'PTZ 20mg/kg', 'S24': 'PTX 0.75mg/kg'}

    elif animal == 'Ent_CamK2_22':
        condition_by_session = {'S01': None, 'S02': None, 'S03': None, 'S04': None,'S05': None,
                                'S06': 'PTZ 20mg/kg','S07': 'NaCl', 'S08' : 'Dz 5mg/kg',
                                'S09' :'Dz 5mg/kg','S10': 'NaCl' , 'S11': 'PTZ 20mg/kg',
                                'S12': 'PTZ 20mg/kg', 'S13': 'NaCl','S14':'Dz 5mg/kg',
                                'S15':'PTZ 20mg/kg','S16': 'NaCl','S17':'Dz 5mg/kg',
                                'S18':'Dz 5mg/kg','S19':'PTZ 20mg/kg','S20': 'NaCl',
                                'S21': 'PTZ 20mg/kg' , 'S22': 'NaCl','S23':'Dz 5mg/kg'}

    elif animal == 'Ent_CamK2_24':
        condition_by_session = {'S01': None, 'S02': None, 'S03': None, 'S04': None,'S05': None,
                                'S06': 'PTZ 20mg/kg', 'S07' : 'Dz 5mg/kg','S08': 'NaCl',
                                'S09' :'Dz 5mg/kg','S10': 'NaCl','S11': 'PTZ 20mg/kg',
                                'S12': 'PTZ 20mg/kg', 'S13': 'Dz 5mg/kg', 'S14': 'NaCl',
                                'S15': 'Dz 5mg/kg','S16': 'PTZ 20mg/kg','S17': 'NaCl',
                                'S18': 'NaCl','S19': 'Dz 5mg/kg','S20': 'PTZ 20mg/kg',
                                'S21': 'NaCl', 'S22': 'Dz 5mg/kg', 'S23': 'PTZ 20mg/kg',
                                'S24': 'PTZ 20mg/kg', 'S25': 'NaCl','S26': 'Dz 5mg/kg',
                                'S27': 'PTZ 30mg/kg', 'S28': 'PTZ 30mg/kg', 'S29': 'PTZ 30mg/kg', 'S30': 'PTZ 30mg/kg'}

    elif animal == 'Ent_CamK2_26':
        condition_by_session = {'S01': None,'S02': None, 'S03': None, 'S04': None,'S05': None }

    elif animal == 'Ent_CamK2_28':
        condition_by_session = {'S01': None,'S02': None, 'S03': None, 'S04': None,'S05': None,
                                'S06': 'NaCl', 'S07' : 'Dz 5mg/kg', 'S08': 'PTZ 20mg/kg',
                                'S09': 'PTZ 20mg/kg', 'S10': 'Dz 5mg/kg','S11': 'NaCl',
                                'S12': 'NaCl', 'S13': 'PTZ 20mg/kg', 'S14':'Dz 5mg/kg',
                                'S15': 'NaCl', 'S16': 'Dz 5mg/kg', 'S17': 'PTZ 20mg/kg',
                                'S18': 'NaCl', 'S19': 'PTZ 20mg/kg', 'S20': 'Dz 5mg/kg'}

    elif animal == 'Ent_CamK2_30':
        condition_by_session = {'S01': 'Dz 5mg/kg', 'S02': 'PTZ 20mg/kg', 'S03': 'NaCl',
                                'S04':'Dz 5mg/kg', 'S05': 'PTZ 20mg/kg', 'S06': 'NaCl',
                                'S07': 'Dz 5mg/kg','S08': 'NaCl','S09' : 'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_34':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj',
                                'S09': 'PTZ 20mg/kg', 'S10': 'Dz 5mg/kg', 'S11': 'NaCl',
                                'S12': 'PTZ 20mg/kg', 'S13': 'NaCl', 'S14': 'Dz 5mg/kg',
                                'S15': 'PTZ 20mg/kg', 'S16': 'NaCl', 'S17': 'Dz 5mg/kg', 'S18':'PTZ 20mg/kg',
                                'S19': 'NaCl', 'S20':  'Dz 5mg/kg', 'S21': 'NaCl','S22':'PTZ 20mg/kg',
                                'S23':'PTZ 30mg/kg'}

    elif animal == 'Ent_CamK2_35':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj'}

    elif animal == 'Ent_CamK2_38':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj',
                                'S09':'Dz 5mg/kg', 'S10':'NaCl', 'S11' : 'PTZ 20mg/kg',
                                'S12': 'NaCl', 'S13': 'Dz 5mg/kg', 'S14': 'PTZ 20mg/kg',
                                'S15': 'PTZ 20mg/kg', 'S16': 'Dz 5mg/kg', 'S17': 'NaCl', 'S18': 'PTZ 20mg/kg',
                                'S19': 'PTZ 20mg/kg', 'S20': 'NaCl', 'S21':  'Dz 5mg/kg',
                                'S23':'PTZ 30mg/kg','S24':'PTZ 30mg/kg','S25':'PTZ 30mg/kg'}

    elif animal == 'Ent_CamK2_39':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj',
                                'S09': 'PTZ 20mg/kg', 'S10':  'Dz 5mg/kg', 'S11': 'NaCl',
                                'S12': 'PTZ 20mg/kg', 'S13': 'Dz 5mg/kg', 'S14': 'NaCl',
                                'S15': 'NaCl', 'S16': 'Dz 5mg/kg', 'S17': 'PTZ 20mg/kg', 'S18': 'NaCl',
                                'S19': 'NaCl', 'S20': 'Dz 5mg/kg', 'S21': 'PTZ 20mg/kg', 'S22':'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_40':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj',
                                'S09': 'NaCl', 'S10': 'PTZ 20mg/kg', 'S11':'Dz 5mg/kg',
                                'S12': 'Dz 5mg/kg', 'S13': 'NaCl', 'S14':'PTZ 20mg/kg',
                                'S15': 'Dz 5mg/kg','S16': 'NaCl', 'S17':'PTZ 20mg/kg'}


    elif animal == 'Ent_CamK2_42':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj',
                                'S09': 'NaCl', 'S10': 'PTZ 20mg/kg', 'S11': 'Dz 5mg/kg',
                                'S12': 'Dz 5mg/kg', 'S13': 'PTZ 20mg/kg', 'S14': 'NaCl',
                                'S15': 'Dz 5mg/kg', 'S16': 'PTZ 20mg/kg', 'S17': 'NaCl', 'S18': 'Dz 5mg/kg',
                                'S19': 'NaCl','S20': 'PTZ 20mg/kg'}

    elif animal == 'Ent_CamK2_43':
        condition_by_session = {'S01': 'No inj','S02': 'No inj', 'S03': 'No inj','S04': 'No inj','S05': 'No inj', 'S06': 'No inj','S07': 'No inj','S08': 'No inj',
                                'S09':'Dz 5mg/kg', 'S10':'NaCl'}

    elif animal == 'Ent_CamK2_54':
        condition_by_session = {'S10':'Dz 3mg/kg','S11': 'Dz 7mg/kg', 'S12': 'Dz 5mg/kg','S13': 'Dz 1mg/kg', 'S14': 'NaCl'}

    elif animal == 'Ent_CamK2_55':
        condition_by_session = {'S10': 'NaCl', 'S11': 'Dz 1mg/kg', 'S12': 'Dz 7mg/kg', 'S13': 'Dz 5mg/kg', 'S14': 'Dz 3mg/kg'}

    elif animal == 'Ent_CamK2_56':
        condition_by_session = {'S10': 'Dz 7mg/kg', 'S11': 'Dz 5mg/kg', 'S12': 'Dz 3mg/kg', 'S13': 'NaCl', 'S14': 'Dz 1mg/kg'}

    elif animal == 'Ent_CamK2_57':
        condition_by_session = {'S10': 'Dz 3mg/kg', 'S11': 'Dz 5mg/kg', 'S12': 'Dz 1mg/kg', 'S13': 'NaCl', 'S14': 'Dz 7mg/kg'}

    elif animal == 'Ent_CamK2_58':
        condition_by_session = {'S10': 'Dz 7mg/kg', 'S11': 'Dz 3mg/kg', 'S12': 'NaCl', 'S13': 'Dz 1mg/kg', 'S14': 'Dz 5mg/kg'}

    elif animal == 'Ent_CamK2_59':
        condition_by_session = {'S01': 'NaCl', 'S02': 'PTZ 25mg/kg', 'S03': 'NaCl', 'S04': 'PTZ 25mg/kg', 'S05': 'NaCl', 'S06': 'PTZ 25mg/kg'}

    elif animal == 'Ent_CamK2_60':
        condition_by_session = {'S01': 'NaCl', 'S02': 'PTZ 25mg/kg', 'S03': 'NaCl', 'S04': 'PTZ 25mg/kg'}

    elif animal == 'Ent_CamK2_61':
        condition_by_session = {'S01': 'NaCl', 'S02': 'PTZ 25mg/kg', 'S03': 'NaCl', 'S04': 'PTZ 25mg/kg','S05': 'NaCl', 'S06': 'PTZ 25mg/kg',  'S07': 'PTZ 30mg/kg'}

    elif animal == 'Ent_CamK2_62':
        condition_by_session = {'S01': 'NaCl', 'S02': 'PTZ 25mg/kg', 'S03': 'NaCl', 'S04': 'PTZ 25mg/kg','S05': 'NaCl', 'S06': 'PTZ 25mg/kg', 'S07':'No inj'}

    elif animal == 'Ent_CamK2_63':
        condition_by_session = {'S01': 'NaCl', 'S02': 'PTZ 25mg/kg', 'S03': 'NaCl', 'S04': 'PTZ 25mg/kg','S05': 'NaCl', 'S06': 'PTZ 25mg/kg'}

    elif animal == 'Ent_CamK2_64':
        condition_by_session = {'S01': 'NaCl', 'S02': 'PTZ 25mg/kg', 'S03': 'NaCl', 'S04': 'PTZ 25mg/kg'}

    if list_sessions == 'all':
        list_sessions = list(condition_by_session.keys())

    list_conditions = [condition_by_session[x] for x in list_sessions]

    return list_conditions
def TTSZ_by_session(animal, list_sessions='all'):
        if animal == 'Ent_CamK2_03':
            TTSZ_by_session = {'S01': 5, 'S02': 8, 'S03': 5, 'S04': 5, 'S05': 10, 'S06': 5,
                               'S07': 5, 'S08': 5, 'S09': 6, 'S10': 5, 'S11': 5, 'S12': 7,
                               'S13': 4, 'S14': 7, 'S15': 4, 'S16': 5}

        elif animal == 'Ent_CamK2_04':
            TTSZ_by_session = {'S01': 6, 'S02': 20, 'S03': 8, 'S04': 7, 'S05': 15, 'S06': 7,
                               'S07': 7, 'S08': 10, 'S09': 7, 'S10': 6, 'S11': 10, 'S12': 6,
                               'S13': 8, 'S14': 6, 'S15': 6, 'S16': 6, 'S17': 5, 'S18': 5,
                               'S19': 4}

        elif animal == 'Ent_CamK2_06':
            TTSZ_by_session = {'S01': 6, 'S02': 5, 'S03': 5, 'S04': 5, 'S05': 4, 'S06': 6,
                               'S07': 5, 'S08': 5, 'S09': 4, 'S10': 4, 'S11': 3, 'S12': 3,
                               'S13': 2, 'S14': 4, 'S15': 5}

        elif animal == 'Ent_CamK2_07':
            TTSZ_by_session = {'S01': 10, 'S02': 30, 'S03': 10, 'S04': 20, 'S05': 10, 'S06': 10,
                               'S07': 12, 'S08': 8, 'S09': 6, 'S10': 12, 'S11': 7, 'S12': 4}

        elif animal == 'Ent_CamK2_09':
            TTSZ_by_session = {'S01': 5, 'S02': 6, 'S03': 6, 'S04': 7,
                               'S05': 5, 'S06': 5, 'S07': 6, 'S08': 4,
                               'S09': 3, 'S10': 3.5, 'S11': 6, 'S12': 2.5, 'S13':np.nan}

        elif animal == 'Ent_CamK2_10':
            TTSZ_by_session = {'S01': 4, 'S02': 4, 'S03': 7, 'S04': 4,
                               'S05': 6, 'S06': 3.5, 'S07': 3, 'S08': 3.5,
                               'S09': 6, 'S10': 3.5, 'S11': 3, 'S12': 4,
                               'S13': 6, 'S14': 3, 'S15': 3, 'S16': 3,
                               'S17': 3.5, 'S18': 3.5, 'S19': 3.5, 'S20': 5,
                               'S21': 3.5, 'S22': 3, 'S23': 7, 'S24': 3}

        elif animal == 'Ent_CamK2_11':
            TTSZ_by_session = {'S01': 7, 'S02': 5, 'S03': 4, 'S04': 10,
                               'S05': 0.5, 'S06': 3, 'S07': 10, 'S08': 2.5,
                               'S09': 2.5, 'S10': 3, 'S11': 10, 'S12': 3.5,
                               'S13': 2.5, 'S14': 15, 'S15': 2, 'S16': 5,
                               'S17': 10, 'S18': 20, 'S19': 10, 'S20': 3,
                               'S21': 20, 'S22': 2}

        elif animal == 'Ent_CamK2_12':
            TTSZ_by_session = {'S01': 25, 'S02': 4, 'S03': 5, 'S04': 5,
                               'S05': 3.5, 'S06': 10, 'S07': 2.5, 'S08': 6,
                               'S09': 3.5, 'S10': 6, 'S11': 2, 'S12': 4,
                               'S13': 4, 'S14': 2.5, 'S15': 10, 'S16': 3.5,
                               'S17': 5, 'S18': 3.5, 'S19': 5, 'S20': 12,
                               'S21': 1.5}


        elif animal == 'Ent_CamK2_15':
            TTSZ_by_session = {'S01': 3, 'S02': 5, 'S03': 5, 'S04': 3.5,
                               'S05': 3.5, 'S06': 5, 'S07': 2.5}

        elif animal == 'Ent_CamK2_16':
            TTSZ_by_session = {'S01': 2, 'S02': 3, 'S03': 4, 'S04': 3,
                               'S05': 3, 'S06': 2.5, 'S07': 2.5, 'S08': 2.5,
                               'S09': 3, 'S10': 2.5, 'S11': 3, 'S12': 2.5,
                               'S13': 3, 'S14': 3, 'S15': 2.5, 'S16': 2.5,
                               'S17': 3.5, 'S18': 3, 'S19': 3, 'S20': 3.5,
                               'S21': 3, 'S22': np.nan, 'S23': 2.5, 'S24': 3.5}

        elif animal == 'Ent_CamK2_22':
            TTSZ_by_session = {'S06': 1.5, 'S07': 3.5, 'S08': 10,'S09': 10, 'S10': 4, 'S11': 2.5,
                               'S12': 2, 'S13': 2.5, 'S14': 5,
                                'S15':2, 'S16':1.5, 'S17':3.5,
                                'S18':8, 'S19':2 ,'S20':2,
                                'S21':1,'S22':15, 'S23':35}

        elif animal == 'Ent_CamK2_24':
            TTSZ_by_session = {'S06': 2, 'S07': 5, 'S08': 2.5,'S09': 6, 'S10': 3, 'S11': 3.5,
                               'S12': 3, 'S13': 5, 'S14': 3,
                               'S15': 4, 'S16': 2, 'S17': 3,
                               'S18': 3.5, 'S19': 20, 'S20': 3,
                               'S21': 2, 'S22': 10, 'S23':3,
                               'S24': 2.5, 'S25': 3, 'S26': 7}

        elif animal == 'Ent_CamK2_28':
            TTSZ_by_session = {'S06': 4, 'S07': 10, 'S08': 5 ,'S09': 3, 'S10': 12, 'S11': 5,
                               'S12': 3, 'S13': 3, 'S14': 7,
                               'S15':5, 'S16':15, 'S17':1.5,
                                'S18':2.5, 'S19':2.5 ,'S20':6,
                                'S21':1,'S22':15}

        elif animal == 'Ent_CamK2_30':
            TTSZ_by_session = {'S01': 35, 'S02': 7, 'S03': 7, 'S04': 35, 'S05': 10, 'S06': 10,
                               'S07': 35, 'S08': 20, 'S09': 30}

        elif animal == 'Ent_CamK2_34':
            TTSZ_by_session = {'S03': 25, 'S05': 35, 'S06': 35,'S07': 35,'S08':35,
                               'S09': 10, "S10": 35, 'S11': 35,
                               'S12': 5, 'S13': 5, 'S14': 10,
                               'S15': 35, 'S16': 35, 'S17': 35, 'S18': 35,
                               'S19': 4, 'S20': 7, 'S21': 3.5, 'S22': 2}

        elif animal == 'Ent_CamK2_35':
            TTSZ_by_session = {'S03': 35, 'S04': 10, 'S05': 35, 'S06': 6,'S07': 6, 'S08':3.5}

        elif animal == 'Ent_CamK2_38':
            TTSZ_by_session = {'S03': 35, 'S04': 35, 'S05': 35, 'S06': 35,'S07': 35,
                               'S09': 35, "S10": 35, 'S11': 20,
                               'S12': 35, 'S13': 35, 'S14': 35,
                               'S15': 35, 'S16': 35, 'S17':35, 'S18': 35,
                               'S19': 12, 'S20': 35, 'S21': 35}

        elif animal == 'Ent_CamK2_39':  #'S12': 5s removed because spont
            TTSZ_by_session = {'S03': 12, 'S04': 20, 'S06': 35,'S07': 35,'S08':6,
                               'S09': 35, "S10": 35, 'S11': 35,
                                'S12': np.nan, 'S13': 12, 'S14': 3.5,
                               'S15': 3, 'S16': 15, 'S17': 6, 'S18': 5,
                               'S19': 12, 'S20': 35, 'S21': 10,
                               'S22': 35}

        elif animal == 'Ent_CamK2_40':
            TTSZ_by_session = {'S03': 35, 'S04': 7, 'S05': 12, 'S06': 4,'S07': 3.5,'S08':3,
                               'S09': 35, "S10": 5, 'S11': 35,
                               'S12': 8, 'S13': 3, 'S14': 2.5,
                               'S15': 6, 'S16': 3.5 }

        elif animal == 'Ent_CamK2_42':
            TTSZ_by_session = {'S04': 20, 'S05': 10, 'S06': 6,'S07': 35, 'S08':35,
                               'S09': 35, "S10": 35, 'S11': 35,
                               'S12': 35, 'S13': 35, 'S14': 35,
                               'S15': 20, 'S16':  5, 'S17': 4, 'S18': 7,
                               'S19': 7}

        elif animal == 'Ent_CamK2_43':
            TTSZ_by_session = {'S03': 20, 'S04': 5, 'S05': 8, 'S06': 4,'S07': 3.5,'S08': 3,
                               'S09': 35, 'S10': 7}


        elif animal == 'Ent_CamK2_54':
            TTSZ_by_session = {'S01': 3.5, 'S02': 4, 'S03': 3.5, 'S04': 5, 'S05': 5,
                               'S06': 4,'S07': 3, 'S08': 2.5,
                               'S10': 4, 'S11': 6, 'S12': 5, 'S13': 3.5, 'S14': 3}

        elif animal == 'Ent_CamK2_55':
            TTSZ_by_session = {'S01': 3, 'S02': 4, 'S03': 5, 'S04': 5,
                               'S06': 5, 'S07': 3.5, 'S08': 3.5, 'S09': 2,
                               'S10': 2.5, 'S11': 4, 'S12': 7, 'S13': 5, 'S14': 4}

        elif animal == 'Ent_CamK2_56':
            TTSZ_by_session = {'S01': 1.5, 'S02': 2.5, 'S03': 3.5, 'S04': 2.5, 'S05': 2.5,
                               'S06': 2.5, 'S07': 3, 'S08': 3.5, 'S09': 2.5,
                               'S10': 3, 'S11': 3, 'S12': 3, 'S13': 2.5, 'S14': 3
                               }

        elif animal == 'Ent_CamK2_57':
            TTSZ_by_session = {'S01': 3.5, 'S02': 3, 'S03': 4, 'S04': 4, 'S05': 1,
                               'S06': 4, 'S07': 4, 'S08': 4, 'S09': 4,
                               'S10': 5, 'S11': 5, 'S12': 3.5, 'S13': 1.5, 'S14': 5}

        elif animal == 'Ent_CamK2_58':
            TTSZ_by_session = {'S01': 5, 'S02': 6, 'S03': 7, 'S04': 5, 'S05': 4,
                               'S06': 3.5, 'S07': 3.5, 'S08': 2.5, 'S09': 1.5,
                               'S10': 7, 'S11': 3.5, 'S12': 2, 'S13': 3, 'S14': 5}

        elif animal == 'Ent_CamK2_59':
            TTSZ_by_session = {'S01': 12, 'S03': 10,'S05': 7}

        elif animal == 'Ent_CamK2_60':
            TTSZ_by_session = {'S01': np.nan, 'S03': 25}

        elif animal == 'Ent_CamK2_61':
            TTSZ_by_session = {'S01': 8, 'S03': 6,'S05': 10}

        elif animal == 'Ent_CamK2_62':
            TTSZ_by_session = {'S01': 4, 'S03': 4,'S05': 3.5}

        elif animal == 'Ent_CamK2_63':
            TTSZ_by_session = {'S01': 8, 'S03': 6,'S05': 3.5}

        elif animal == 'Ent_CamK2_64':
            TTSZ_by_session = {'S01': 25, 'S03': 12}

        if list_sessions == 'all':
            list_sessions = list(TTSZ_by_session.keys())


        list_TTSZ = [TTSZ_by_session[x] for x in list_sessions]

        return list_TTSZ

def Racine_by_session(animal, list_sessions='all'):

    if animal == 'Ent_CamK2_03' or animal == 'Ent_CamK2_04' or animal == 'Ent_CamK2_06': #Animals without video recordings
        Racine_by_session = {}
        for session in list_sessions:
            Racine_by_session.update({session: np.nan})


    elif animal == 'Ent_CamK2_09':
        Racine_by_session = {'S01': 0, 'S02': 1, 'S03': 0, 'S04': 0,
                            'S05': 3, 'S06': 1, 'S07': 1, 'S08': 4,
                            'S09': 3, 'S10': 0, 'S11': 1, 'S12': 2}

    elif animal == 'Ent_CamK2_10':
        Racine_by_session = {'S01': 1, 'S02': 0, 'S03': 0, 'S04': 1,
                            'S05': 0, 'S06': 2, 'S07': 1, 'S08':0,
                            'S09': 0, 'S10': 2, 'S11': 1, 'S12': 1,
                            'S13': 0, 'S14': 1, 'S15': 2, 'S16': 0,
                            'S17': 1, 'S18': 2, 'S19' : 0, 'S20': 0,
                            'S21': 1, 'S22': 3, 'S23': 1, 'S24': 5}

    elif animal == 'Ent_CamK2_11':
        Racine_by_session = {'S01': 2, 'S02': 3, 'S03': 3, 'S04': 1,
                             'S05': 5, 'S06': 3, 'S07': 1, 'S08': 5,
                             'S09': 5, 'S10': 4, 'S11': 3, 'S12': 5,
                             'S13': 5, 'S14': 3, 'S15': 5, 'S16': 5,
                             'S17': 3, 'S18': 1, 'S19': 3, 'S20': 5,
                             'S21': 1, 'S22': 6}

    elif animal == 'Ent_CamK2_15':
        Racine_by_session = {'S01': 0, 'S02': 1, 'S03': 2, 'S04': 3,
                            'S05': 3, 'S06': 1, 'S07': 6}

    elif animal == 'Ent_CamK2_16':
        Racine_by_session = {'S01': 0, 'S02': 0, 'S03': 1, 'S04': 1,
                             'S05': 1, 'S06': 1, 'S07': 2, 'S08': 1,
                             'S09': 1, 'S10': 2, 'S11': 1, 'S12': 2,
                             'S13': 1, 'S14': 1, 'S15': 5, 'S16': 1,
                             'S17': 0, 'S18': 1, 'S19': 1, 'S20': 2,
                             'S21': 1, 'S23': 5, 'S24': 5}

    elif animal == 'Ent_CamK2_34':
        Racine_by_session = {'S12': 0,'S13': 0,'S14': 0,
                            'S19': 2, 'S20': 1,'S21': 2, 'S22': 3}

    elif animal == 'Ent_CamK2_38':
        Racine_by_session = {'S19': 0}

    elif animal == 'Ent_CamK2_39':
        Racine_by_session = {'S12': 3,'S13': 1,'S14': 3,
                             'S15': 1, 'S16': 2, 'S17': 5, 'S18': 5,
                            'S19': 3, 'S21': 5}

    elif animal == 'Ent_CamK2_40':
        Racine_by_session = {'S10': 5,
                             'S12': 1,'S13': 5,'S14': 5,
                             'S15': 1}

    elif animal == 'Ent_CamK2_42':
        Racine_by_session = {'S15': 2,'S16': 4,'S17': 4,'S18': 1,
                             'S19': 3}

    elif animal == 'Ent_CamK2_43':
        Racine_by_session = {'S10': 5}

    elif animal == 'Ent_CamK2_54':
        Racine_by_session = {'S10': 0, 'S11': 1,'S12': 1, 'S13': 1, 'S14': 2}

    elif animal == 'Ent_CamK2_55':
        Racine_by_session = {'S10': 5, 'S11': 1,'S12': 0, 'S13': 1, 'S14': 1}

    elif animal == 'Ent_CamK2_56':
        Racine_by_session = {'S10': 1, 'S11': 0,'S12': 1, 'S13': 5, 'S14': 1}

    elif animal == 'Ent_CamK2_57':
        Racine_by_session = {'S10': 0, 'S11': 0,'S12': 1, 'S13': 4, 'S14': 1}

    elif animal == 'Ent_CamK2_58':
        Racine_by_session = {'S10': 1, 'S11': 1,'S12': 5, 'S13': 5, 'S14': 1}

    list_Racine = [Racine_by_session[x] for x in list_sessions]

    return list_Racine

def get_Sz_df(animals, sessions_per_animals,path):
    cat_order = get_cat_order()
    Sz_df_by_animals = []
    for animal in animals:
        Sz_df = pd.DataFrame(columns=['Animal', 'Session', 'Time to Sz [s]', 'Condition'])
        sessions = sessions_per_animals[animal]
        Sz_df['Session'] = sessions
        Sz_df['Animal'] = [animal] * len(sessions)
        Sz_df['Condition'] = condition_by_session(animal, sessions)
        Sz_df['Time to Sz [s]'] = TTSZ_by_session(animal, sessions)
        Sz_df['Filename'] = Sz_df['Animal'] + '_' + Sz_df['Session']
        Sz_df = GL_Plot.Add_block_session_TTSZ(animal,Sz_df)
        Sz_df = GL_Plot.Add_norm_TTSZ_by_block(animal,Sz_df)
        # Sz_df = GL_Plot.Add_duration_Sz(animal, Sz_df, path)
        # Sz_df = GL_Plot.Add_norm_duration_sz_by_block(animal, Sz_df)
        #Sz_df = GL_Plot.Add_norm_Sum_LL_by_block(animal, Sz_df, path)
        # Sz_df = GL_Plot.Correct_CA1_Sum_LL(animal,Sz_df)
        Sz_df_by_animals.append(Sz_df)

    All_Sz_df = pd.concat(Sz_df_by_animals, ignore_index=True)
    return All_Sz_df
def Freq_Stim_session(animal,list_sessions = 'all'):
    if animal == 'Ent_CamK2_03' or animal == 'Ent_CamK2_04' or animal == 'Ent_CamK2_06' \
            or animal == 'Ent_CamK2_09' or animal == 'Ent_CamK2_10' or animal == 'Ent_CamK2_11' \
            or animal == 'Ent_CamK2_12' or  animal == 'Ent_CamK2_15' or animal == 'Ent_CamK2_16':
        Freq_by_session = {}
        for session in list_sessions:
            Freq_by_session.update({session: 20})

    elif animal == 'Ent_CamK2_22':
        Freq_by_session = {'S06': 20, 'S07': 20, 'S08': 20, 'S09': 20, 'S10': 20, 'S11': 20,
                       'S12': 20, 'S13': 20, 'S14': 20,
                       'S15': 40, 'S16': 40, 'S17': 40,
                       'S18': 10, 'S19': 10, 'S20': 10,
                       'S21': 4, 'S22': 4, 'S23': 4}

    elif animal == 'Ent_CamK2_24':
        Freq_by_session = {'S06': 20, 'S07': 20, 'S08': 20, 'S09': 20, 'S10': 20, 'S11': 20,
                       'S12': 20, 'S13': 20, 'S14': 20,
                       'S15': 40, 'S16': 40, 'S17': 40,
                       'S18': 4, 'S19': 4, 'S20': 4,
                       'S21': 7, 'S22': 7, 'S23': 7,
                        'S24': 10, 'S25': 10, 'S26': 10}

    elif animal == 'Ent_CamK2_28':
       Freq_by_session = {'S06': 20, 'S07': 20, 'S08': 20, 'S09': 20, 'S10': 20, 'S11': 20,
                       'S12': 20, 'S13': 20, 'S14': 20,
                       'S15': 7, 'S16': 7, 'S17': 7,
                       'S18': 40, 'S19': 40, 'S20': 40}

    elif animal == 'Ent_CamK2_30':
        Freq_by_session = {'S01': 20, 'S02': 20, 'S03': 20,
                           'S04': 20, 'S05': 20, 'S06': 20,
                            'S07': 7, 'S08': 7, 'S09': 7,'S10': 4}

    elif animal == 'Ent_CamK2_34':
        Freq_by_session = {'S03': 20, 'S05': 10, 'S06': 4,'S07': 7, 'S08':40,
                           'S09':10, "S10":10, 'S11':10,
                            'S12':40,'S13':40,'S14':40,
                            'S15':4, 'S16':4, 'S17':4,'S18':4,
                            'S19':20,'S20':20,'S21':20 , 'S22':20}

    elif animal == 'Ent_CamK2_35':
        Freq_by_session = {'S03': 7,'S04': 40, 'S05': 4, 'S06': 20,'S07': 10, 'S08': 20}

    elif animal == 'Ent_CamK2_38':
        Freq_by_session = {'S03': 20,'S04': 40, 'S05': 4, 'S06': 7,'S07': 10,
                           'S09': 10, "S10": 10, 'S11': 10,
                           'S12': 40, 'S13': 40, 'S14': 40,
                           'S15': 4, 'S16': 4, 'S17': 4, 'S18': 4,
                           'S19': 20, 'S20': 20, 'S21': 20}

    elif animal == 'Ent_CamK2_39':
        Freq_by_session = {'S03': 10, 'S04': 40, 'S06': 7,'S07': 4, 'S08': 20,
                           'S09': 4, "S10": 4, 'S11': 4,
                           'S12': 20, 'S13': 20, 'S14': 20,
                           'S15': 40, 'S16': 40, 'S17': 40, 'S18': 40,
                           'S19': 10, 'S20': 10, 'S21': 10, 'S22':7}

    elif animal == 'Ent_CamK2_40':
        Freq_by_session = {'S03': 4, 'S04': 20, 'S05': 7, 'S06': 10,'S07': 40, 'S08':20,
                           'S09': 4, "S10": 4, 'S11': 4,
                           'S12': 20, 'S13': 20, 'S14': 20,
                           'S15': 40, 'S16': 40}

    elif animal == 'Ent_CamK2_42':
        Freq_by_session = {'S04': 10, 'S05': 20, 'S06': 40,'S07': 7, 'S08': 4,
                           'S09': 4, "S10": 4, 'S11': 4,
                           'S12': 7, 'S13': 7, 'S14': 7,
                           'S15': 20, 'S16': 20, 'S17': 20, 'S18': 20,
                           'S19': 10}

    elif animal == 'Ent_CamK2_43':
        Freq_by_session = {'S03': 4, 'S04': 20, 'S05': 7, 'S06': 10,'S07': 40, 'S08':20,
                           'S09': 4, "S10": 4}

    elif animal == 'Ent_CamK2_54':
        Freq_by_session = {'S01': 20,'S02': 20, 'S03': 20, 'S04': 20, 'S05': 20,
                           'S06': '20p/s','S07': 20, 'S08':20}

    elif animal == 'Ent_CamK2_55':
        Freq_by_session = {'S01': 20, 'S02': 20, 'S03': 20, 'S04': 20,
                           'S06': '20p/s', 'S07': 20, 'S08': 20, 'S09': '20p/s'}

    elif animal == 'Ent_CamK2_56':
        Freq_by_session = {'S01': 20, 'S02': 20, 'S03': 20, 'S04': 20,'S05': 20,
                           'S06': 20, 'S07': '20p/s', 'S08':'20p/s', 'S09': 20}

    elif animal == 'Ent_CamK2_57':
        Freq_by_session = {'S01': 20, 'S02': 20, 'S03': 20, 'S04': 20,'S05': 20,
                           'S06': 20, 'S07': '20p/s', 'S08': 20, 'S09': '20p/s'}

    elif animal == 'Ent_CamK2_58':
        Freq_by_session = {'S01': 20, 'S02': 20, 'S03': 20, 'S04': 20,'S05': 20,
                           'S06':  '20p/s', 'S07': 20, 'S08': 20, 'S09': '20p/s'}


    if list_sessions == 'all':
        list_sessions = list(TTSZ_by_session.keys())

    list_Freq = [Freq_by_session[x] for x in list_sessions]

    return list_Freq
def get_color_cnd():
    my_color_palette =  {'Dz 1mg/kg':'#663399','Dz 3mg/kg':'#4AB2D6','Dz 5mg/kg':'#8FB996','Dz 7mg/kg':'#006594'
        ,'NaCl':'#594157', 'PTZ 20mg/kg':'#c7991a', 'PTX 0.75mg/kg': '#db3021', 'PTZ error':'#c7991a', 'No inj':"#3f3673", 'Convulsive PTZ':'#db3021','Control':'#594157','Post-Ictal':'#3287d1'} # 'PTZ 20mg/kg':'#F1BF98'

    return  my_color_palette
def get_cat_order():
    cat_order = ['NaCl','Dz 1mg/kg', 'Dz 3mg/kg', 'Dz 5mg/kg','Dz 7mg/kg',
                                                    'PTX 0.75mg/kg', 'PTZ 20mg/kg']
    return cat_order
def get_list_good_channel(animal,type='LFP'):

    if animal == 'Ent_CamK2_03':
        if type =='LFP':
            list_channel = ["ENT R",  "DG R", "CA3 R", "CA3 L", "ENT L"]

        elif type == 'all':
            list_channel = ["EEG R", 'EEG L', "ENT R", "DG R", "CA3 R", "CA3 L", "ENT L"]

    elif animal == 'Ent_CamK2_04':
        if type =='LFP':
            list_channel = ["ENT R", "CA1 R", "DG R", "CA1 L"]

        elif type == 'all':
            list_channel = ["EEG R", 'EEG L', "ENT R", "CA1 R", "DG R", "CA1 L"]

    elif animal == 'Ent_CamK2_06':
        if type == 'LFP':
            list_channel = ["CA1 R", "DG R", "CA1 L", "DG L"]

        elif type == 'all':
            list_channel = ["EEG R", 'EEG L', "CA1 R", "DG R", "CA1 L", "DG L"]

    elif animal == 'Ent_CamK2_09':
        if type == 'LFP':
            list_channel = [ "ENT R ventral", "ENT R dorsal","CA3 R", "CA3 L","CA1 L",  "DG L",  "Sub L",
                    "ENT L ventral", "ENT L dorsal"]

        elif type == 'all':
            list_channel = ["EEG R", 'EEG L', "ENT R ventral", "ENT R dorsal", "CA3 R", "CA3 L", "CA1 L", "DG L", "Sub L",
                            "ENT L ventral", "ENT L dorsal"]

        elif type == 'probe':
            list_channel = ["Probe 00", "Probe 01", "Probe 02", "Probe 03", "Probe 04", "Probe 05", "Probe 06", "Probe 07",
                         "Probe 08","Probe 09", "Probe 10", "Probe 11", "Probe 12", "Probe 13", "Probe 14", "Probe 15"]

        elif type == 'all + probe':
            list_channel = ["EEG R", 'EEG L',"ENT R ventral", "ENT R dorsal","CA3 R", "CA3 L","CA1 L",  "DG L",  "Sub L",
                    "ENT L ventral", "ENT L dorsal","Probe 00", "Probe 01", "Probe 02", "Probe 03", "Probe 04", "Probe 05", "Probe 06", "Probe 07",
                        "Probe 08", "Probe 09", "Probe 10", "Probe 11", "Probe 12", "Probe 13", "Probe 14", "Probe 15"]

    elif animal == 'Ent_CamK2_10':
        if type == 'LFP':
            list_channel = ["ENT R ventral","ENT R dorsal","CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", "CA1 L","DG L",  "Sub L", "ENT L ventral", "ENT L dorsal"]

        elif type == 'all':
            list_channel = ["EEG R", "EEG L", "ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", "CA1 L","DG L", "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_11' :
        if type =='LFP':
            list_channel = ["ENT R ventral", "ENT R dorsal", "CA3 R", "Sub R","CA3 L", "CA1 L", "DG L","Sub L",
                    "ENT L ventral", "ENT L dorsal"]

        if type == 'ALL':
            list_channel = ["EEG R", "EEG L", "ENT R ventral", "ENT R dorsal", "CA3 R", "Sub R", "CA3 L", "CA1 L", "DG L", "Sub L",
                            "ENT L ventral", "ENT L dorsal"]

        elif type == 'probe':
            list_channel = ["Probe 00", "Probe 01", "Probe 02", "Probe 03", "Probe 04", "Probe 05", "Probe 06", "Probe 07",
                         "Probe 08","Probe 09", "Probe 10", "Probe 11", "Probe 12", "Probe 13", "Probe 14", "Probe 15"]

        elif type == 'all + probe':
            list_channel = [ "ENT R ventral", "ENT R dorsal","CA3 R", "CA3 L","CA1 L",  "DG L",  "Sub L",
                    "ENT L ventral", "ENT L dorsal","Probe 00", "Probe 01", "Probe 02", "Probe 03", "Probe 04", "Probe 05", "Probe 06", "Probe 07",
                        "Probe 08", "Probe 09", "Probe 10", "Probe 11", "Probe 12", "Probe 13", "Probe 14", "Probe 15"]


    elif animal == 'Ent_CamK2_12':
        list_channel = ["Probe 00", "Probe 01", "Probe 02", "Probe 03", "Probe 04", "Probe 05", "Probe 06", "Probe 07",
                         "Probe 08","Probe 09", "Probe 10", "Probe 11", "Probe 12", "Probe 13", "Probe 14", "Probe 15"]

    elif animal == 'Ent_CamK2_15':
        if type == 'LFP':
            list_channel = ["ENT R ventral", "ENT R dorsal","CA1 R","CA3 R", "DG R", "Sub R","CA3 L", 'CA1 L', "DG L", "Sub L",
                         "ENT L ventral", "ENT L dorsal"]
        elif type == 'all':
            list_channel = ["EEG R", "EEG L", "ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", "CA1 L","DG L", "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_16':
        if type == 'LFP':
            list_channel =["ENT R ventral", "ENT R dorsal","CA1 R","CA3 R", "DG R", "Sub R","CA3 L", 'CA1 L', "DG L", "Sub L",
                         "ENT L ventral", "ENT L dorsal"]
        elif type == 'all':
            list_channel = ["EEG R", "EEG L", "ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L", "Sub L","ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_17':
        if type == 'all':
            list_channel =["EEG R", "EEG L", "ENT R ventral", "ENT R dorsal","CA1 R","CA3 R", "DG R", "Sub R","CA3 L", 'CA1 L', "DG L", "Sub L",
                             "ENT L ventral", "ENT L dorsal"]
        elif type == 'LFP':
            list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L","Sub L",
                    "ENT L ventral", "ENT L dorsal"]


    elif animal == 'Ent_CamK2_18':
        if type == 'all':
            list_channel =["EEG R", "EEG L", "ENT R ventral", "ENT R dorsal","CA1 R","CA3 R", "DG R", "Sub R","CA3 L", 'CA1 L', "DG L", "Sub L",
                             "ENT L ventral", "ENT L dorsal"]
        elif type == 'LFP':
            list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L","Sub L",
                    "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_22':
        list_channel = ["ENT R ventral", "ENT R dorsal","CA1 R","CA3 R", "DG R", "Sub R","CA3 L", 'CA1 L', "DG L", "Sub L",
                         "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_24':
        list_channel = ["ENT R ventral", "ENT R dorsal","CA1 R","CA3 R", "DG R", "Sub R","CA3 L", 'CA1 L', "DG L", "Sub L",
                         "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_26':
        list_channel = [ "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L",
                        "ENT L ventral", "ENT L dorsal"] #"ENT R ventral",

    elif animal == 'Ent_CamK2_28':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_30':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_34':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L",  "ENT L dorsal"]

    elif animal == 'Ent_CamK2_35':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_38':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_39': #EEG L and R bad
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_40':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                         "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_42':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_41':
        list_channel = ["Probe 01", "Probe 02", "Probe 03", "Probe 04",  "Probe 06", "Probe 07", "Probe 08","Probe 09", "Probe 10", "Probe 11"]

    elif animal == 'Ent_CamK2_43':
        list_channel = ["Probe 00", "Probe 01", "Probe 02", "Probe 03", "Probe 04", "Probe 05", "Probe 06", "Probe 07",
                         "Probe 08","Probe 09", "Probe 10", "Probe 11", "Probe 12", "Probe 13", "Probe 14", "Probe 15"]

    elif animal == 'Ent_CamK2_54':#"Sub R",
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R",  "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_55':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_56':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_57':  #EEG R bad
        list_channel = ["ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_58':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_59':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L"]

    elif animal == 'Ent_CamK2_60':
        list_channel = ["ENT R ventral", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral"]

    elif animal == 'Ent_CamK2_61':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L ventral"]

    elif animal == 'Ent_CamK2_62':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_63':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    elif animal == 'Ent_CamK2_64':
        list_channel = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R", "Sub R", "CA3 L", 'CA1 L', "DG L",
                        "Sub L", "ENT L ventral", "ENT L dorsal"]

    return(list_channel)

def get_color_channel():
    channel_color_palette = {"CA1 R":'#3182bd', "DG R":'#6baed6',"CA3 R":"#9ecae1","Sub R":"#c6dbef", "ENT R ventral":"#756bb1","ENT R dorsal":'#9e9ac8',
                             "CA1 L": '#e6550d', "DG L": '#fd8d3c', "CA3 L": "#fdae6b", "Sub L": "#fdd0a2","ENT L ventral": "#31a354", "ENT L dorsal": '#74c476' }
    return channel_color_palette
def get_coor_per_ch():
    Coor_per_channel = { "ENT R ventral" :(212,265),"ENT R dorsal" :(240,260),'CA1 R': (197, 190) , 'DG R':(170, 190) ,'CA3 R':(235, 190), "Sub R":(215, 220),"CA3 L": (65, 190), "CA1 L":(103, 190), "DG L":(130, 190),"Sub L":(85, 220),
                    "ENT L ventral":(87,265), "ENT L dorsal":(60,260)}
    return Coor_per_channel
def get_channel_order(type):
    if type == 'LFP':
        channel_order = ["ENT R ventral", "ENT R dorsal", "CA1 R", "CA3 R", "DG R","Sub R", "CA3 L","CA1 L", "DG L",
                     "Sub L", "ENT L dorsal", "ENT L ventral"]
    return channel_order

def Chemical_Sz_by_Session(animal):
    if animal == 'Ent_CamK2_03':
        Chemical_Sz_by_Session = {'S01': [None], 'S02': [None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                              'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                              'S13': [None], 'S14': [None],'S15': ['Bsl'],'S16': [None],'S17': ['PP'] }

    elif animal == 'Ent_CamK2_04':
        Chemical_Sz_by_Session = {'S01': [None], 'S02': [None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                              'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                              'S13': [None], 'S14': [None],'S15': [None],'S16': [None],
                                'S17': [None], 'S18': [None], 'S19': [None] }

    elif animal == 'Ent_CamK2_06':
        Chemical_Sz_by_Session = {'S01': [None], 'S02': [None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                              'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                              'S13': ['PP'], 'S14': [None],'S15': [None],'S16': ['Bsl'] }

    elif animal == 'Ent_CamK2_09':
        Chemical_Sz_by_Session={'S01': [None], 'S02':[None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                              'S09': ['Bsl'], 'S10':[None], 'S11': [None], 'S12':[None],
                              'S13': ['Sz_Ind']}

    elif animal == 'Ent_CamK2_10':
        Chemical_Sz_by_Session={'S01': ['After_Ind'], 'S02':[None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                              'S09': [None], 'S10':[None], 'S11': [None], 'S12':[None],
                              'S13': [None], 'S14': [None], 'S15': [None], 'S16':[None],
                              'S17': [None], 'S18': [None], 'S19': [None], 'S20':[None],
                              'S21': [None], 'S22': [None], 'S23': [None], 'S24': [None]
                              }

    elif animal == 'Ent_CamK2_11':
        Chemical_Sz_by_Session={'S01': ['PP'], 'S02':[None], 'S03': [None], 'S04': [None],
                              'S05': ['PP'], 'S06': [None], 'S07': [None], 'S08': ['PP'],
                              'S09': ['Bsl'], 'S10':[None], 'S11': [None], 'S12':['SP'],
                              'S13': ['After_Ind'], 'S14': [None], 'S15': ['SP'], 'S16':[None],
                              'S17': [None], 'S18': [None], 'S19': [None], 'S20':[None],
                              'S21': [None],'S22': [None]}


    elif animal == 'Ent_CamK2_12':
        Chemical_Sz_by_Session={'S01': [None], 'S02':[None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                              'S09': ['PP'], 'S10':[None], 'S11': [None], 'S12':[None],
                              'S13': [None], 'S14': ['PP'], 'S15': [None], 'S16':[None],
                              'S17': [None], 'S18': [None], 'S19': [None], 'S20':[None],
                              'S21': [None]}

    elif animal == 'Ent_CamK2_15':
        Chemical_Sz_by_Session={'S01': [None], 'S02':[None], 'S03': [None], 'S04': [None],
                              'S05': [None], 'S06': [None], 'S07': ['Sz_Ind']}

    elif animal == 'Ent_CamK2_16':
        Chemical_Sz_by_Session = {'S01': ['PP'], 'S02': [None], 'S03': [None], 'S04': [None],
                                  'S05': [None], 'S06': [None], 'S07': [None], 'S08': [None],
                                  'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                                  'S13': [None], 'S14': [None], 'S15': [None], 'S16': [None],
                                  'S17': [None], 'S18': [None], 'S19': [None], 'S20': [None],
                                  'S21': ['After_Ind'], 'S22': [None], 'S23': ['PP'], 'S24': [None]
                                  }

    elif animal == 'Ent_CamK2_34':
        Chemical_Sz_by_Session = {'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                                  'S13': [None], 'S14': [None], 'S15': [None], 'S16': [None],
                                  'S17': [None], 'S18': [None], 'S19': [None], 'S20': [None],  'S21': [None], 'S22': [None]}

    elif animal == 'Ent_CamK2_38':
        Chemical_Sz_by_Session = {'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                                  'S13': [None], 'S14': [None], 'S15': [None], 'S16': [None],
                                  'S17': [None], 'S18': [None], 'S19': [None], 'S20': [None], 'S21': [None]}


    elif animal == 'Ent_CamK2_39':
        Chemical_Sz_by_Session = {'S09': [None], 'S10': [None], 'S11': [None], 'S12': ['PP'],
                                  'S13': [None], 'S14': [None], 'S15': [None], 'S16': [None],
                                  'S17': ['PP','SP'], 'S18': [None], 'S19': [None], 'S20': [None], 'S21': [None]}


    elif animal == 'Ent_CamK2_40':
        Chemical_Sz_by_Session = {'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                                  'S13': [None], 'S14': [None], 'S15': [None]}

    elif animal == 'Ent_CamK2_42':
        Chemical_Sz_by_Session = {'S09': [None], 'S10': [None], 'S11': [None], 'S12': [None],
                                  'S13': [None], 'S14': [None], 'S15': [None], 'S16': [None],
                                  'S17': [None], 'S18': [None], 'S19': [None], 'S20': ['SP']}

    elif animal == 'Ent_CamK2_43':
        Chemical_Sz_by_Session = { 'S08': [None],'S09': [None], 'S10': [None]}

    elif animal == 'Ent_CamK2_54':
        Chemical_Sz_by_Session = {'S10': [None], 'S11': [None], 'S12': [None], 'S13': [None], 'S14': [None]}

    elif animal == 'Ent_CamK2_55':
        Chemical_Sz_by_Session = {'S10': [None], 'S11': [None], 'S12': [None], 'S13': [None], 'S14': [None]}

    elif animal == 'Ent_CamK2_56':
        Chemical_Sz_by_Session = {'S10': [None], 'S11': [None], 'S12': [None], 'S13': [None], 'S14': [None]}

    elif animal == 'Ent_CamK2_57':
        Chemical_Sz_by_Session = {'S10': [None], 'S11': [None], 'S12': [None], 'S13': [None], 'S14': [None]}

    elif animal == 'Ent_CamK2_58':
        Chemical_Sz_by_Session = {'S10': [None], 'S11': [None], 'S12': [None], 'S13': [None], 'S14': [None]}

    return Chemical_Sz_by_Session
def block_session_for_norm(animal):
    if animal == 'Ent_CamK2_03':
        blocks = [['S01','S02','S03'],['S04','S05','S06'],['S07','S08','S09'],['S10','S11','S12'],['S13','S14','S15'], ['S16','S17']]

    elif animal == 'Ent_CamK2_04':
        blocks = [['S01','S02','S03'],['S04','S05','S06'],['S07','S08','S09'],['S10','S11','S12'],['S13','S14','S15'], ['S16','S17','S18','S19']]

    elif animal == 'Ent_CamK2_06':
        blocks = [['S01','S02','S03'],['S04','S05','S06'],['S07','S08','S09'],['S10','S11','S12'],['S13','S14','S15','S16']]

    elif animal == 'Ent_CamK2_07':
        blocks = [['S01','S02','S03'],['S04','S05','S06'],['S07','S08','S09'],['S10','S11','S12','S13']]

    elif animal == 'Ent_CamK2_09':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12','S13']]#

    elif animal == 'Ent_CamK2_10':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12'],['S13','S14','S15','S16'],['S17','S18','S19','S20'],['S21','S22','S23','S24']]

    elif animal == 'Ent_CamK2_11':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12'],['S13','S14','S15','S16'],['S17','S18','S19','S20','S21','S22']]

    elif animal == 'Ent_CamK2_12':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12'],['S13','S14','S15','S16'],['S17','S18','S19','S20','S21']]

    elif animal == 'Ent_CamK2_15':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07']]

    elif animal == 'Ent_CamK2_16':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12'],['S13','S14','S15','S16'],['S17','S18','S19','S20'],['S21','S22','S23','S24']]

    elif animal == 'Ent_CamK2_17':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12'],['S13','S14','S15','S16'],['S17','S18','S19','S20'],['S21','S22','S23','S24']]

    elif animal == 'Ent_CamK2_18':
        blocks = [['S01','S02','S03','S04'],['S05','S06','S07','S08'],['S09','S10','S11','S12'],['S13','S14','S15','S16'],['S17','S18','S19','S20'],['S21','S22','S23','S24']]

    elif animal == 'Ent_CamK2_22':
        blocks = [['S06','S07','S08'], ['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17'], ['S18','S19','S20'], ['S21','S22','S23']]

    elif animal == 'Ent_CamK2_24':
        blocks = [['S06','S07','S08'], ['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17'], ['S18','S19','S20'], ['S21','S22','S23'], ['S24','S25','S26'],['S28','S29','S30']]

    elif animal == 'Ent_CamK2_28':
        blocks = [['S06','S07','S08'], ['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17'], ['S18','S19','S20']]

    elif animal == 'Ent_CamK2_30':
        blocks = [['S01', 'S02', 'S03'], ['S04','S05','S06'], ['S07', 'S08', 'S09']]

    elif animal == 'Ent_CamK2_34':
        blocks =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17','S18'],['S19','S20','S21','S22'],['S23']]

    elif animal == 'Ent_CamK2_35':
        blocks =  [['S03','S04','S05','S06','S07', 'S08']]

    elif animal == 'Ent_CamK2_38':
        blocks =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17','S18'],['S19','S20','S21'],['S24','S25']]

    elif animal == 'Ent_CamK2_39':
        blocks =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17','S18'],['S19','S20','S21','S22']]

    elif animal == 'Ent_CamK2_40':
        blocks =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17']]

    elif animal == 'Ent_CamK2_42':
        blocks =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11'], ['S12','S13','S14'], ['S15','S16','S17','S18'],['S19','S20']]

    elif animal == 'Ent_CamK2_43':
        blocks =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11']]

    elif animal == 'Ent_CamK2_54':
        blocks = [['S01', 'S02'], ['S03', 'S04', 'S05'],[ 'S06','S07'], ['S08'], ['S10','S11','S12','S13','S14']]

    elif animal == 'Ent_CamK2_55':
        blocks = [['S01', 'S02'], ['S03', 'S04'], ['S06', 'S07'], ['S08','S09'], ['S10','S11','S12','S13','S14']]

    elif animal == 'Ent_CamK2_56':
        blocks = [['S01', 'S02'], ['S03', 'S04', 'S05'], ['S06', 'S07'], ['S08','S09'], ['S10','S11','S12','S13','S14']]

    elif animal == 'Ent_CamK2_57':
        blocks = [['S01', 'S02'], ['S03', 'S04', 'S05'], ['S06', 'S07'], ['S08','S09'], ['S10','S11','S12','S13','S14']]

    elif animal == 'Ent_CamK2_58':
        blocks = [['S01', 'S02'], ['S03', 'S04', 'S05'], ['S06', 'S07'], ['S08','S09'], ['S10','S11','S12','S13','S14']]

    elif animal == 'Ent_CamK2_59':
        blocks = [['S01', 'S02'], ['S03', 'S04'], ['S05', 'S06']]

    elif animal == 'Ent_CamK2_60':
        blocks = [['S01', 'S02'], ['S03', 'S04']]

    elif animal == 'Ent_CamK2_61':
        blocks = [['S01', 'S02'], ['S03', 'S04'], ['S05', 'S06', 'S07']]

    elif animal == 'Ent_CamK2_62':
        blocks = [['S01', 'S02'], ['S03', 'S04'], ['S05', 'S06'],['S07']]

    elif animal == 'Ent_CamK2_63':
        blocks = [['S01', 'S02'], ['S03', 'S04'], ['S05', 'S06']]

    elif animal == 'Ent_CamK2_64':
        blocks = [['S01', 'S02'], ['S03', 'S04']]

    return blocks

def block_session_for_norm_freq(animal):
    if animal == 'Ent_CamK2_22':
        blocks_freq = [['S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22','S23']]

    elif animal == 'Ent_CamK2_24':
        blocks_freq = [['S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22','S23','S24','S25','S26']]

    elif animal == 'Ent_CamK2_34':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22']]

    elif animal == 'Ent_CamK2_35':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08']]

    elif animal == 'Ent_CamK2_38':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20','S21']]

    elif animal == 'Ent_CamK2_39':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22']]

    elif animal == 'Ent_CamK2_40':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11','S12','S13','S14','S15','S16','S17']]

    elif animal == 'Ent_CamK2_42':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20']]

    elif animal == 'Ent_CamK2_43':
        blocks_freq =  [['S03','S04','S05','S06','S07', 'S08'],['S09','S10','S11']]

    return blocks_freq
def get_stim_protocol(animal, session):
    if animal == 'Ent_CamK2_03' or animal == 'Ent_CamK2_04' or animal == 'Ent_CamK2_06':
        Duration_stim = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]

    elif animal == 'Ent_CamK2_09' or animal == 'Ent_CamK2_10' or animal == 'Ent_CamK2_11' or animal == 'Ent_CamK2_12' or animal == 'Ent_CamK2_16':
        if session == 'S01' or session == 'S02' or session == 'S03' or session == 'S04':
            Duration_stim = [1,2,3,4,5,6,7,8,10,12,15,20,25,30]
        else:
            Duration_stim = [0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]

    elif animal == 'Ent_CamK2_15':
        if session == 'S01' or session == 'S02' or session == 'S03':
            Duration_stim = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]
        else:
            Duration_stim = [0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]

    else :
        Duration_stim = [0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]

    return Duration_stim


