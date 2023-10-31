import numpy as np
import pandas as pd
import os as os
from mne import io
import scipy.io
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import dabest
from Lepeu_Nat_Com_2023 import Info_Experiment
from sklearn.decomposition import NMF

# All functions used for pulse analysis, created by GL

def linelength_to_plot(data,window):
    # For plotting purpose, transform data (1D time series) in line-length
    D = np.concatenate((np.repeat(np.nan, window),np.absolute(np.ediff1d(data))))
    LL_nan = []

    for i, x in np.ndenumerate(D):
        sum = np.nansum(D[int(i[0]-window/2):int(i[0] + window/2)])
        LL_nan.append(float(sum))

    LL = LL_nan[int(window/2):-int(window/2 - 1)]

    return LL

def SP_DataFrame(animal,session,dir,name_channel,condition,save = True):
    #############################################
    # Created: GL, September 2020
    # Goal: From protocol of stimulation (_voltage_SP) and sitmulation timestamps, create a dataframe to store single pulse reponses
    #############################################
    filename = animal + '_' + session
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    os.chdir(dir + '/Pre-processed_No_rescale_fif')
    raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    event_name = raw._annotations.description
    event_onset = np.round(raw._annotations.onset * Sampling_freq).astype(int)
    event = event_onset[event_name == ''] # Event without name correspond to stim timestmaps

    # Load the type of each events according to file save during stimulation
    os.chdir(dir + '/Event_type')
    info_PP = scipy.io.loadmat(filename + "_PP_type.mat")['conditionnal_pulse_matrice']
    info_SP = scipy.io.loadmat(filename + "_voltage_SP.mat")['voltage_SP']

    # take only event for SP
    onset_SP = event[2 * len(info_PP[0]):2 * len(info_PP[0]) + len(info_SP[0])]

    # conditions
    condition_array = np.array([condition] * len(info_SP[0]))

    # Creat dataframe with info for each PP
    infos_SP = {'Intensity[v]': np.round(info_SP[0], 2), 'Onset[datapoints]': onset_SP, 'Condition': condition_array}
    SP_df = pd.DataFrame(infos_SP, columns=['Intensity[v]', 'Onset[datapoints]', 'Condition'])

    if save == True:
        SP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_SP_analogue_" + name_channel)

    return SP_df

def SP_df_auto(animal,session,dir,name_channel,ref_channel):
    # Based on the one created for the reference channel, create DF for each channel
    filename = animal + '_' + session
    dir = dir + animal

    # Load SP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    Ref_SP_df =  pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_'+ ref_channel)

    SP_df = Ref_SP_df.loc[:,['Intensity[v]', 'Onset[datapoints]', 'Condition']]

    try:
        SP_df['Block'] = Ref_SP_df['Block']
        SP_df['Filename'] = Ref_SP_df['Filename']
        SP_df['Intensity Conditioning Pulse'] = Ref_SP_df['Intensity Conditioning Pulse']
        SP_df["Chemical Sz"] =  Ref_SP_df["Chemical Sz"]
        SP_df['Distance from Sz[s]'] =  Ref_SP_df['Distance from Sz[s]']
    except:
        pass

    SP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_SP_analogue_" + name_channel)
    return SP_df

def Train_DataFrame(animal,session,dir,name_channel,condition,no_rescale = True,save = True):
    Duration_stim = Info_Experiment.get_stim_protocol(animal, session)
    Int_train =  Info_Experiment.get_intensity_Sz_protocol(animal)
    filename = animal + '_' + session
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    if no_rescale == True:
        os.chdir(dir +'/'+ animal + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)

    else:
        os.chdir(dir +'/'+ animal + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    event_name = raw._annotations.description
    event_onset = np.round(raw._annotations.onset * Sampling_freq).astype(int)
    event_duration = np.round(raw._annotations.duration * Sampling_freq).astype(int)
    event = event_onset[event_name == '']
    try:
        start_sz = event_onset[event_name == 'Ind_Sz']
        end_sz = start_sz + event_duration[event_name == 'Ind_Sz']
    except:
        print(session + ' No induce seizure found')
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()

    # Load the type of each events according to file save during stimulation
    os.chdir(dir + '/' + animal + '/Event_type')
    info_PP = scipy.io.loadmat(filename + "_PP_type.mat")['conditionnal_pulse_matrice']
    info_SP = scipy.io.loadmat(filename + "_voltage_SP.mat")['voltage_SP']
    try:    # Check if there an ID_50 file (round 2 only)
        info_ID50 = scipy.io.loadmat(filename + "_voltage_ID50.mat")['voltage_ID50']
        nb_event = len(info_PP[0])*2 + len(info_SP[0]) + len(info_ID50[0])
    except:
        nb_event = len(info_PP[0])*2 + len(info_SP[0])

    event_pulse = event[nb_event:]

    # Find star of the different trains of stim
    event_diff = np.diff(event_pulse)
    indice_start_train = np.argwhere(event_diff > 30 * Sampling_freq).flatten()

    event_train_by_stim = []
    for i in indice_start_train:
        if i == indice_start_train[0]:
            event_train = event_pulse[0:i+1]
        else:
            event_train = event_pulse[j:i+1]
        j=i+1
        a = np.diff(event_train)
        duration = (event_train[-1] - event_train[0]) / Sampling_freq
        event_train_by_stim.append(event_train)
        if i == indice_start_train[-1]:
            event_train = event_pulse[j:]
            event_train_by_stim.append(event_train)

    for i,train in enumerate(event_train_by_stim):
        Sz_per_pulse = []
        Induced_Sz = 'Yes' if start_sz < train[-1] < end_sz else 'No'
        for event in train:
            Pulse_Sz = 'Yes' if start_sz < event < end_sz else 'No'
            Sz_per_pulse.append(Pulse_Sz)
        condition_array = np.array([condition] * len(train))
        intensity_array =  np.array([Int_train] * len(train))
        session_array = np.array([session]*len(train))
        animal_array = np.array([animal]*len(train))
        info_df = {'Animal':animal_array, 'Session':session_array, 'Condition': condition_array ,'Pulse Index': np.arange(0,len(train)),
                    'Onset[datapoints]': train,'Intensity[v]': intensity_array, 'Duration Train[s]': np.array([Duration_stim[i]] * len(train)),
                   'Train with Sz' : np.array([Induced_Sz] * len(train)) ,'Pulse in Sz': np.array(Sz_per_pulse)}
        train_df = pd.DataFrame(info_df)
        if i ==0:
            all_trains_df = train_df
        else:
            all_trains_df = pd.concat([all_trains_df,train_df], ignore_index=True)

    if save == True:
        if no_rescale == True:
            all_trains_df.to_pickle(dir + '/' + animal + '/Data_Event_by_session/' + filename + "_No_rescale_Info_TrainStim_" + name_channel)
        else:
            all_trains_df.to_pickle(dir + '/' + animal + '/Data_Event_by_session/' + filename + "_TrainStim_" + name_channel)

def Train_DataFrame_auto(animal,session,dir,name_channel,ref_channel,no_rescale = True):
    filename = animal + '_' + session
    dir = dir + '/' + animal
    # Load PP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        Ref_all_trains_df =  pd.read_pickle(filename + "_No_rescale_Info_TrainStim_" + ref_channel)
    else:
        Ref_all_trains_df = pd.read_pickle(filename +  "_TrainStim_" + ref_channel)

    all_trains_df = Ref_all_trains_df.loc[:, ['Animal','Session','Condition','Pulse Index', 'Onset[datapoints]','Intensity[v]', 'Duration Train[s]', 'Train with Sz','Pulse in Sz' ]]

    if no_rescale == True:
        all_trains_df.to_pickle(filename + "_No_rescale_Info_TrainStim_" + name_channel)
    else:
        all_trains_df.to_pickle( filename + "_TrainStim_" + name_channel)

def SP_Sum_LL(animal, session, dir,name_channel,Detection_window,time_window=500,no_rescale=True,save=True,highpass=0.1, lowpass=800):
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    filename = animal + '_' + session
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()

    if highpass != 0.1 or lowpass != 800:
        # Filter signal at 3Hz before calculating P2P
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]

    print('Channel n°: ', channel, ' selected')

    # Load SP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
    else:
        SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + name_channel)

    onset_SP = SP_df['Onset[datapoints]']
    Detection_datapoints = int(Detection_window * Sampling_freq / 1000)
    time_window_datapoints = int(time_window * Sampling_freq / 1000)

    list_sum_LL = []

    for i in range(0, SP_df.shape[0]):
        event_EEG = data[channel,int(onset_SP[i] - time_window_datapoints):int(onset_SP[i] + time_window_datapoints)].flatten()
        Sum_LL = np.sum(np.abs(np.diff(data[channel,onset_SP[i]:onset_SP[i] + Detection_datapoints])))/Detection_window

        list_sum_LL.append(Sum_LL)

    metric = 'Sum LL ' + str(Detection_window) + 'ms'
    SP_df[metric] = list_sum_LL

    # Check Max value to check if artefact
    all_diff_intensity = np.sort(np.unique(SP_df['Intensity[v]']))
    for intensity in all_diff_intensity:
        index_intensity = np.where(SP_df['Intensity[v]'] == intensity)[0]
        SP_int = SP_df.loc[index_intensity, :]
        for x in SP_int[metric].sort_values(ascending=False):
            i = np.where(SP_df[metric] == x)[0]
            onset_SP = SP_df['Onset[datapoints]'][i]
            event_EEG = data[channel,
                            int(onset_SP[i] - time_window_datapoints):int(
                                onset_SP[i] + time_window_datapoints)].flatten()
            Event_LL = np.array(linelength_to_plot(event_EEG, window=Detection_datapoints))

            title = filename + ' ' + name_channel + ' Pulse n°' + str(i) + ', intensitiy ' + str(intensity) + ' V'
            fig1 = plt.figure(title, figsize=(8, 5)).suptitle(title)
            gridspec.GridSpec(12, 12)
            ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
            ax2 = ax1.twinx()
            x = np.arange(-time_window, time_window, 1000 / Sampling_freq)
            ax1.plot(x, event_EEG, color='#403d3d')
            ax2.plot(x, Event_LL, color='r')
            ax1.axvspan(0, 3, edgecolor='#1B2ACC', facecolor='#089FFF', linestyle="--", lw=1)
            ax1.axvline(x=Detection_window, ymin=-800, ymax=800, linestyle="dashed", linewidth=0.8, color='r')
            ax1.set_xlabel('[ms]')
            ax1.set_ylabel('[uV]')
            ax1.set_ylabel('[uV]')
            ax2.set_ylabel('LL[uV/ms]')
            ax1.set_ylim(bottom=-800, top=800)
            plt.show()
            response = input('keep it?(y/n/c)')
            if response == "c":
                print('event before n° ', i, " kept but continue")
            elif response != "y":
                SP_df[metric][i] = np.nan
                print('event before n° ', i, " removed")
            elif response == "y":
                print('event before n° ', i, " kept")
                break

    if save == True:
        SP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_SP_analogue_" + name_channel)
    return

def SP_Sum_LL_auto(animal, session, dir,name_channel,ref_channel,Detection_window,no_rescale=True,highpass=0.1, lowpass=800):
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    filename = animal + '_' + session
    dir = dir + animal
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()

    if highpass != 0.1 or lowpass != 800:
        # Filter signal at 3Hz before calculating P2P
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]

    print('Channel n°: ', channel, ' selected')

    # Load PP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_'+ name_channel)
        Ref_SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_'+ ref_channel)
    else:
        SP_df = pd.read_pickle(filename + '_Info_SP_analogue_'+ name_channel)
        Ref_SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + ref_channel)

    onset_SP = SP_df['Onset[datapoints]']
    Detection_datapoints = int(Detection_window * Sampling_freq / 1000)

    list_sum_LL = []

    for i in range(0, SP_df.shape[0]):
        event_EEG = data[channel, onset_SP[i]:int(onset_SP[i] + Detection_datapoints)].flatten()
        Sum_LL = np.sum(np.abs(np.diff(event_EEG))) / Detection_window
        list_sum_LL.append(Sum_LL)


    metric = 'Sum LL ' + str(Detection_window) + 'ms'
    SP_df[metric] = list_sum_LL

    # Nan where artefact in ref file
    SP_df.loc[Ref_SP_df[metric].isna(),metric] = np.nan
    SP_df.loc[Ref_SP_df[metric].isna(),metric] = np.nan

    if no_rescale == True:
        SP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_SP_analogue_" + name_channel)
    else:
        SP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_analogue_" + name_channel)

def Train_Sum_LL(animal, session,dir,name_channel,time_window,highpass=0.1, lowpass=800,no_rescale=True,save=True):
    # Modified by GL February 2022 => Sum_LL calculated automatically on inter-pulse window based on Freq stim
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    filename = animal + '_' + session
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()

    if highpass != 0.1 or lowpass != 800:
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]

    print('Channel n°: ', channel, ' selected')

    # Load Train stim dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        all_trains_df = pd.read_pickle(filename + "_No_rescale_Info_TrainStim_" + name_channel)
    else:
        all_trains_df = pd.read_pickle(filename + "_TrainStim_" + name_channel)

    onset_pulse = all_trains_df['Onset[datapoints]']
    Detection_window = time_window
    Detection_datapoints = int(Detection_window * Sampling_freq / 1000)

    list_sum_LL = []
    for i in range(0, len(onset_pulse)):
        Sum_LL = np.sum(np.abs(np.diff(data[channel,onset_pulse[i]:onset_pulse[i] + Detection_datapoints])))/Detection_window
        list_sum_LL.append(Sum_LL)

    metric = 'Sum LL ' + str(int(Detection_window)) + 'ms'
    all_trains_df[metric] = list_sum_LL

    for pulse in all_trains_df[metric].sort_values(ascending=False):
        i = np.where(all_trains_df[metric] == pulse)[0]
        event_EEG = data[channel,int(all_trains_df['Onset[datapoints]'][i] - Detection_datapoints):int(all_trains_df['Onset[datapoints]'][i] + Detection_datapoints)].flatten()
        Event_LL = np.array(linelength_to_plot(event_EEG, window=Detection_datapoints))
        title = (filename + ' ' + name_channel + ' Train ' + str(int(all_trains_df['Duration Train[s]'][i])) + 's, pulse index '+ str(int(all_trains_df['Pulse Index'][i])) + ', in Sz: ' + all_trains_df.loc[i, 'Pulse in Sz'].to_string())
        fig1 = plt.figure(title, figsize=(8, 5)).suptitle(title)
        gridspec.GridSpec(12, 12)
        ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
        ax2 = ax1.twinx()
        x = np.arange(-time_window, time_window, 1000 / Sampling_freq)
        ax1.plot(x, event_EEG, color='#403d3d')
        ax2.plot(x, Event_LL, color='r')
        ax1.axvspan(0, 3, edgecolor='#1B2ACC', facecolor='#089FFF', linestyle="--", lw=1)
        ax1.axvline(x=Detection_window, ymin=-800, ymax=800, linestyle="dashed", linewidth=0.8, color='r')
        ax1.set_xlabel('[ms]')
        ax1.set_ylabel('[uV]')
        ax1.set_ylabel('[uV]')
        ax2.set_ylabel('LL[uV/ms]')
        ax1.set_ylim(bottom=-800, top=800)
        plt.show()
        response = input('keep it?(y/c/n)')
        if response == "c":
            print('event before n° ', i, " kept but continue")
        elif response == "y":
            print('event before n° ', i, " kept")
            break
        elif response != "y":
            all_trains_df.loc[i,metric] = np.nan
            print('event before n° ', i, " removed")

    if save == True:
        if no_rescale == True:
            all_trains_df.to_pickle(filename + "_No_rescale_Info_TrainStim_" + name_channel)
        else:
            all_trains_df.to_pickle(filename + "_TrainStim_" + name_channel)

def Train_Sum_LL_auto(animal, session, dir,name_channel,ref_channel ,time_window,highpass=0.1, lowpass=800,no_rescale=True):
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    filename = animal + '_' + session
    dir = dir + animal

    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()

    if highpass != 0.1 or lowpass != 800:
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]

    print('Channel n°: ', channel, ' selected')

    # Load Train stim dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        all_trains_df = pd.read_pickle(filename + '_No_rescale_Info_TrainStim_'+ name_channel)
        Ref_all_trains_df = pd.read_pickle(filename + '_No_rescale_Info_TrainStim_'+ ref_channel)
    else:
        all_trains_df = pd.read_pickle(filename + '_TrainStim_'+ name_channel)
        Ref_all_trains_df = pd.read_pickle(filename + '_TrainStim_' + ref_channel)

    onset_SP = all_trains_df['Onset[datapoints]']
    Detection_window = time_window
    Detection_datapoints = int(Detection_window * Sampling_freq / 1000)

    list_sum_LL = []

    for i in range(0, all_trains_df.shape[0]):
        event_EEG = data[channel, onset_SP[i]:int(onset_SP[i] + Detection_datapoints)].flatten()
        Sum_LL = np.sum(np.abs(np.diff(event_EEG))) / Detection_window
        list_sum_LL.append(Sum_LL)


    metric = 'Sum LL ' + str(int(Detection_window)) + 'ms'
    all_trains_df[metric] = list_sum_LL

    # Nan where artefact in ref file
    all_trains_df.loc[Ref_all_trains_df[metric].isna(),metric] = np.nan
    all_trains_df.loc[Ref_all_trains_df[metric].isna(),metric] = np.nan

    if no_rescale == True:
        all_trains_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_TrainStim_" + name_channel)
    else:
        all_trains_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_TrainStim_" + name_channel)

def Train_add_frequencies(animal, session,dir,name_channel,no_rescale=True):
    Stim_freq = Info_Experiment.Freq_Stim_session(animal, [session])[0]
    filename = animal + '_' + session
    dir = dir + animal
    # Load PP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        all_trains_df = pd.read_pickle(filename + '_No_rescale_Info_TrainStim_'+ name_channel)
    else:
        all_trains_df = pd.read_pickle(filename + '_TrainStim_'+ name_channel)

    all_trains_df.loc[:,'Stim Frequency'] = Stim_freq


    if no_rescale == True:
        all_trains_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_TrainStim_" + name_channel)
    else:
        all_trains_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_TrainStim_" + name_channel)

def Add_block_session_info(animals,name_channel,path,no_rescale=True):
    for i_animal, animal in enumerate(animals):
        sessions_animals= Info_Experiment.block_session_for_norm(animal)
        os.chdir(path + animal + '/Data_Event_by_session')
        for week,session_in_week in enumerate(sessions_animals):
            # Retrieve dataframe with paired pulses value for each sessions
            for i_session, session in enumerate(session_in_week):
                filename = animal + '_' + session

                SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
                SP_df["Block"] = [week] * len(SP_df['Onset[datapoints]'])
                SP_df["Filename"] = [filename] * len(SP_df['Onset[datapoints]'])
                SP_df.to_pickle(filename + "_No_rescale_Info_SP_analogue_" + name_channel)

                Train_df = pd.read_pickle(filename + "_No_rescale_Info_TrainStim_" + name_channel)
                Train_df["Block"] = [week] * len(Train_df['Onset[datapoints]'])
                Train_df["Filename"] = [filename] * len(Train_df['Onset[datapoints]'])
                Train_df.to_pickle(filename + "_No_rescale_Info_TrainStim_" + name_channel)

def Nomralization_SP_by_block(df, metric, intensity=1):
    # Normalize response by subtracting minimum and then dividing by mean NaCl
    all_block = np.sort(np.unique(df["Block"]))
    df['Normalized ' + metric] = np.nan
    for block in all_block:
        Mean_SP_NaCl = np.nanmean(df[metric] [(df['Block'] == block)&(df['Intensity[v]'] == intensity) & (df[metric].notna()) & (df['Condition'] == 'NaCl')])
        df.loc[(df['Block'] == block),'Normalized ' + metric] = df[metric][df['Block'] == block] / Mean_SP_NaCl
    return (df)

def Nomralization_Pulse_by_block(df, metric):
    all_block = np.sort(np.unique(df["Block"]))
    df['Normalized ' + metric] = np.nan
    for block in all_block:
        Mean_First_Pulse_NaCl = np.mean(df[metric] [(df[metric].notna()) & (df['Condition'] == 'NaCl') & (df['Block'] == block)])
        df.loc[df['Block'] == block,'Normalized ' + metric] = df[metric][df['Block'] == block] / Mean_First_Pulse_NaCl

    return (df)

def Normalization_SP_before_inj(df, metric):
    intensity = np.unique(df['Intensity[v]'])
    df['Normalized ' + metric] = np.nan
    for int in intensity:
        Mean_SP_before = np.nanmean(df[metric] [(df['Intensity[v]'] == int) & (df[metric].notna()) & (df['Before / After Inj'] == 'Before')])
        df.loc[(df['Intensity[v]'] == int),'Normalized ' + metric] = df[metric] / Mean_SP_before
    return (df)

##### Function for NMF #####

def get_nnmf(X, rank, it=2000):
    # remove rows that are completly equal zero
    W = np.zeros((X.shape[0], rank))
    X[np.isnan(X)] = 0 #transfrom nan in 0
    X0 = np.delete(X, np.where(X == np.nan)[0], 0) #Remove column with only zeros

    # NMF transform
    model = NMF(n_components=rank, init='random', max_iter=it)
    W0 = model.fit_transform(X0)
    H = model.components_
    W[np.where(np.mean(X, 1) > 0)[0], :] = W0

    return W, H
def plot_V_W_H(M_input ,W, H, title, ylabels):
    # Plot basis functions and activation coefficients
    fig2 = plt.figure(title, figsize=(16, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)

    ax1 = plt.subplot2grid((12, 12), (0, 4), rowspan=7, colspan=8)
    ax1.set_title('Input Matrix')
    aspect_M = M_input.shape[1] / 20 * 8 / M_input.shape[0]
    ax1.imshow(M_input, aspect=aspect_M)#, aspect=aspect, vmin=np.percentile(M_input, 20), vmax=np.percentile(M_input, 95))  # , vmin=0, vmax=15
    if ylabels:
        ax1.set_yticks(np.arange(len(ylabels)))
        ax1.set_yticklabels(ylabels)
    ax1.set_xlabel('trials')

    aspect_W = W.shape[1] / 5 * 8 / W.shape[0]
    ax2 = plt.subplot2grid((12, 12), (0, 0), rowspan=11, colspan=3)
    ax2.set_title('Basic Functions')
    ax2.imshow(W, aspect=aspect_W, vmin=np.percentile(W, 20), vmax=np.percentile(W, 95), cmap='hot')  # , vmin=0, vmax=15
    ax2.set_ylabel('Channels')
    ax2.set_xlabel('Ranks')
    H_col = []
    for i in range(W.shape[1]):
        H_col.append('W' + str(i + 1))
    ax2.set_xticks(np.arange(W.shape[1]))
    ax2.set_xticklabels(H_col, fontsize=12)
    if ylabels:
        ax2.set_yticks(np.arange(len(W)))
        ax2.set_yticklabels(ylabels)


    # plot activation functions
    aspect_H = H.shape[1] /20 * 5 / H.shape[0]
    ax3 = plt.subplot2grid((12, 12), (8, 4), rowspan=4, colspan=8, sharex=ax1)
    ax3.set_title('Activation Function')
    ax3.imshow(H, aspect=aspect_H, vmin=np.percentile(H, 20), vmax=np.percentile(H, 95), cmap='hot')  # , vmin=0, vmax=15
    ax3.set_ylabel('Activation Function (H)', fontsize=12)
    ax3.set_xlabel('Trials', fontsize=12)
    W_col = []
    for i in range(H.shape[0]):
        W_col.append('H' + str(i + 1))
    ax3.set_yticks(np.arange(len(H)))
    ax3.set_yticklabels( W_col, fontsize=12)

    plt.subplots_adjust(hspace=0.9, wspace=0.9)

def plot_NMF_AUC_Ph(data, hue_order,my_color_palette, title):
    # For each coefficient, plot the I/O cruve for activation coefficient
    all_condition = np.unique(data['Condition'])
    H_all = [i for i in data.columns if i.startswith('H')]

    fig = plt.figure(title, figsize=(16, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)

    AUC_dict = {}
    a = np.isin(hue_order, all_condition)
    conditions = np.array(hue_order)[a].tolist()

    for i_h, Hs in enumerate(H_all):
        axx = plt.subplot2grid((12, 12), (0, int(i_h * (12 / len(H_all)))), rowspan=12, colspan=int(12 / len(H_all)))
        val_min = np.min(data.groupby(['Condition', 'Intensity[v]'])[Hs].mean())
        val_max = np.max(data.groupby(['Condition', 'Intensity[v]'])[Hs].mean())
        for idx_cnd,cnd in enumerate(conditions):
            dat_c = data[(data.Condition == cnd)]
            Int_all = np.unique(dat_c['Intensity[v]'])
            AUC1 = np.trapz(np.repeat(val_max, len(Int_all)) - val_min, Int_all)
            H_mean = dat_c.groupby('Intensity[v]')[Hs].mean().values
            AUC = np.trapz(H_mean - val_min, np.unique(dat_c['Intensity[v]'])) / AUC1
            AUC_dict[Hs+'_'+cnd] = AUC
            axx.plot(Int_all, H_mean, color=my_color_palette[cnd], label=cnd + ' AUC: ' + str(np.round(AUC, 2)))
            axx.fill_between(Int_all, val_min, H_mean, color=my_color_palette[cnd], alpha=0.1)
        axx.set_title(Hs)
        axx.axhline(val_min)
        axx.axhline(val_max)
        axx.plot([np.min(Int_all), np.max(Int_all)], [val_min, val_max], '--', c=[0, 0, 0], alpha=0.5)
        axx.set_ylim([0, 1.1 * val_max])
        axx.legend()
        axx.set_xlabel('Intensity [v]')
        if i_h == 0:
            axx.set_ylabel('H coefficient')

    plt.subplots_adjust(wspace=0.9)

    return AUC_dict

def NMF_SP_get_AUC_per_block(data, hue_order,animal, block):
    # For each block, calculate area under the I/O cruve
    Int_all = np.unique(data['Intensity[v]'])
    all_condition = np.unique(data['Condition'])
    H_all = [i for i in data.columns if i.startswith('H')]
    conditions = np.array(hue_order)[np.isin(hue_order, all_condition)].tolist() # Remove condition not in the block from conditions

    list_AUC=[] ; list_Hs = [] ; list_cnd = []; list_session = []
    for i_h, Hs in enumerate(H_all):
        val_min = np.min(data.groupby(['Condition', 'Intensity[v]'])[Hs].mean())
        val_max = np.max(data.groupby(['Condition', 'Intensity[v]'])[Hs].mean())
        AUC1 = np.trapz(np.repeat(val_max, len(Int_all)) - val_min, Int_all)
        for idx_cnd,cnd in enumerate(conditions):
            dat_c = data[(data.Condition == cnd)]
            session = np.unique(data['Session'][(data.Condition == cnd)])[0]
            H_mean = dat_c.groupby('Intensity[v]')[Hs].mean().values
            AUC = np.trapz(H_mean - val_min, np.unique(dat_c['Intensity[v]'])) / AUC1
            list_AUC.append(AUC)
            list_Hs.append(Hs), list_cnd.append(cnd);list_session.append(session)

    info_df = {'Animal': [animal] * len(conditions), 'Session':list_session,'Block': [block] * len(conditions),'Condition':list_cnd,'H':list_Hs, 'AUC':list_AUC}
    AUC_df = pd.DataFrame(info_df)

    return AUC_df