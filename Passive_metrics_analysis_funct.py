import numpy as np
import pandas as pd
import os as os
from mne import io
import scipy.io
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.ticker
import matplotlib.colors as colors
import matplotlib as mpl
import NMF
from scipy import signal
from scipy import stats
from fooof import FOOOFGroup
from Lepeu_Nat_Com_2023 import Info_Experiment
from statsmodels.tsa.stattools import acf as acf
from statsmodels.graphics import tsaplots

def LFP_DataFrame(animal,session,dir,name_channel,condition,no_rescale = True,save = True,highpass=0.1, lowpass=800):
    #############################################
    # Created: GL, August 2022
    # Goal: Create dataframe with LFP between SP and PP
    #############################################
    filename = animal + '_' + session
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)

    else:
        os.chdir(dir + animal + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()
    event_name = raw._annotations.description
    event_onset = np.round(raw._annotations.onset * Sampling_freq).astype(int)
    events = event_onset[event_name == '']

    if highpass != 0.1 or lowpass != 800:
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]


    # Load the type of each events according to file save during stimulation
    os.chdir(dir + '/Event_type')
    info_PP = scipy.io.loadmat(filename + "_PP_type.mat")['conditionnal_pulse_matrice']
    info_SP = scipy.io.loadmat(filename + "_voltage_SP.mat")['voltage_SP']

    # take only second pulse for PP
    event_PP = events[:2 * len(info_PP[0]):2]  # S08 => 20, S10 => 22

    # take event for SP
    onset_SP = events[2 * len(info_PP[0]):2 * len(info_PP[0]) + len(info_SP[0])]

    # Get LFP for each Pulse
    onset_pulse = np.concatenate((event_PP,onset_SP))

    list_EEG = []
    for event in onset_pulse:
        event_EEG = data[channel,int(event + 4 * Sampling_freq): (event + 8 * Sampling_freq)].flatten()
        list_EEG.append(event_EEG)

    # conditions
    condition_array = np.array([condition] * len(onset_pulse))

    # Creat dataframe with info for each PP
    info_LFP = {'Onset[datapoints]': onset_pulse, 'Condition': condition_array, 'LFP': list_EEG }
    LFP_df = pd.DataFrame(info_LFP)

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_LFP_" + name_channel)

    return LFP_df

def LFP_df_auto(animal,session,dir,name_channel,ref_channel,no_rescale=True,highpass=0.1, lowpass=800):
    filename = animal + '_' + session
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + animal + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()

    if highpass != 0.1 or lowpass != 800:
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        Ref_LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + ref_channel)
    else:
        Ref_LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + ref_channel)

    LFP_df = Ref_LFP_df.loc[:,['Onset[datapoints]', 'Condition','Artefact']]

    list_EEG = []
    for event in LFP_df['Onset[datapoints]']:
        event_EEG = data[channel,int(event + 4 * Sampling_freq): (event + 8 * Sampling_freq)].flatten()
        list_EEG.append(event_EEG)

    LFP_df['LFP'] = list_EEG

    try:
        LFP_df['Block'] = Ref_LFP_df['Block']
        LFP_df['Filename'] = Ref_LFP_df['Filename']
        LFP_df["Chemical Sz"] =  Ref_LFP_df["Chemical Sz"]
        LFP_df['Distance from Sz[s]'] =  Ref_LFP_df['Distance from Sz[s]']
    except:
        pass

    if no_rescale == True:
        LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
    else:
        LFP_df.to_pickle(dir +'/Data_Event_by_session/' + filename + "_Info_LFP_" + name_channel)
    return LFP_df

def LFP_DataFrame_chemical_sz(animal,session,dir,name_channel,condition,highpass=0.1, lowpass=800,no_rescale = True,save = True):
    #############################################
    # Created: GL, August 2022
    # Goal: Create dataframe with LFP between SP for chemical sz protocol
    #############################################
    filename = animal + '_' + session
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)

    else:
        os.chdir(dir + animal + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()
    event_name = raw._annotations.description
    event_onset = np.round(raw._annotations.onset * Sampling_freq).astype(int)
    event_duration = np.round(raw._annotations.duration * Sampling_freq).astype(int)
    events = event_onset[event_name == '']

    if highpass != 0.1 or lowpass != 800:
        raw = raw.filter(l_freq=highpass, h_freq=lowpass, picks=channel, phase="zero")
    data = raw[:, :][0]

    # Load the type of each events according to file save during stimulation
    os.chdir(dir + '/Event_type')
    info_before = scipy.io.loadmat(filename + "_voltage_SP_before.mat")['voltage_SP'].flatten()
    info_after = scipy.io.loadmat(filename + "_voltage_SP_after.mat")['voltage_SP'].flatten()

    onset_SP_before = events[:len(info_before)] # onset event before inj
    onset_SP_after = events[len(info_before):len(info_before)+len(info_after) ] # onset event after inj

    N_events = len(onset_SP_before) + len(onset_SP_after)

    list_EEG = []
    for event in events[:N_events]:
        event_EEG = data[channel,int(event + 4 * Sampling_freq): (event + 8 * Sampling_freq)].flatten()
        list_EEG.append(event_EEG)

    infos_LFP = {'Intensity[v]': [info_before[0]] * N_events,'Onset[datapoints]': events[:N_events],'Condition': ['No inj'] * len(onset_SP_before) + [condition] * len(onset_SP_after),
                 'Before / After Inj':["Before"]*len(onset_SP_before) + ["After"]*len(onset_SP_after), 'Before / After Sz': [np.nan] * N_events, 'Distance from Sz[s]': [np.nan] * N_events, 'LFP':list_EEG}

    LFP_df = pd.DataFrame(infos_LFP)


    if 'Sz' in event_name:
        Sz_onset = event_onset[event_name == 'Sz'][0]
        Sz_duration = event_duration[event_name == 'Sz'][0]
        Sz_end = Sz_onset + Sz_duration
        LFP_df['Distance from Sz[s]'] = LFP_df['Onset[datapoints]'] / Sampling_freq - Sz_onset / Sampling_freq  # Calculate distance from Sz start
        LFP_df.loc[LFP_df['Distance from Sz[s]'] > 0, ['Distance from Sz[s]']] = LFP_df['Onset[datapoints]'] / Sampling_freq - Sz_end / Sampling_freq  # Replace by distance form Sz end if after Sz
        LFP_df.loc[LFP_df['Distance from Sz[s]'] < 0, ['Before / After Sz']] = 'Before'
        LFP_df.loc[(LFP_df['Onset[datapoints]'] > Sz_onset) & (LFP_df['Onset[datapoints]'] < Sz_end), 'Before / After Sz'] = "During"
        LFP_df.loc[(LFP_df['Onset[datapoints]'] > Sz_onset) & (LFP_df['Onset[datapoints]'] < Sz_end), 'Distance from Sz[s]'] = np.nan  # Nan the one during Sz
        LFP_df.loc[LFP_df['Distance from Sz[s]'] > 0, ['Before / After Sz']] = 'After'
        #LFP_df.loc[LFP_df[ 'Before / After Inj'] == 'Before' , ['Distance from Sz[s]']] = np.nan

    else:
        print('No Sz found')

    if 'Injection' in event_name:
        Injection = event_onset[event_name == 'Injection'][0]
        LFP_df['Distance from Injection [s]'] = LFP_df['Onset[datapoints]'] / Sampling_freq - Injection / Sampling_freq  # Calculate distance from injection

    else:
        print('No Injection found')

    if condition == 'NaCl':
        last_pulse = onset_SP_after[-1]
        LFP_df['Distance from Sz[s]'] = LFP_df['Onset[datapoints]'] / Sampling_freq - last_pulse / Sampling_freq  # Calculate distance from Sz start
        a = 1

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_LFP_"+ name_channel)

    return LFP_df

def LFP_remove_artefact(animal, session, dir,name_channel,Detection_window,time_window=500,Sampling_freq=2000,no_rescale=True,save=True):
    #############################################
    # Created: GL, August 2022
    # Goal: Detect artefact in LFP bout
    #############################################
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
    else:
        LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + name_channel)

    LFP_df['Artefact'] = False;  LFP_df['Sum LL'] = np.nan; LFP_df['Max LL'] = np.nan

    for i in range(0, LFP_df.shape[0]):
        event_EEG = LFP_df.loc[i,'LFP']
        LFP_df.loc[i,'Sum LL'] = np.sum(gl.linelength_SP(event_EEG, window=100))
        LFP_df.loc[i,'Max LL'] = np.max(gl.linelength_SP(event_EEG, window=100))

    # Check Max value to check if artefact
    for metric in ['Sum LL','Max LL']:
        for x in LFP_df[metric].sort_values(ascending=False):
            i = np.where(LFP_df[metric] == x)[0]
            onset_SP = LFP_df['Onset[datapoints]'][i]
            event_EEG = np.array(LFP_df.loc[i,'LFP'])[0]
            Event_LL = np.array(gl.linelength_SP(event_EEG, window=100))
            title = filename + ' ' + name_channel + ' Pulse n°' + str(i) + ' ' +metric
            fig1 = plt.figure(title, figsize=(20, 5)).suptitle(title)
            gridspec.GridSpec(12, 12)
            ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
            ax2 = ax1.twinx()
            x = np.arange(0, len(event_EEG) / (Sampling_freq/1000), 1000 / Sampling_freq)
            ax1.plot(x, event_EEG, color='#403d3d')
            ax2.plot(x, Event_LL, color='r')
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
                LFP_df.loc[i,'Artefact'] = True
                print('event before n° ', i, " removed")
            elif response == "y":
                print('event before n° ', i, " kept")
                break

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_LFP_" + name_channel)
    return

def LFP_add_block_info(animals, name_channel,path):
    for i_animal, animal in enumerate(animals):
        sessions_animals= Info_Experiment.block_session_for_norm(animal)
        os.chdir(path + animal + '/Data_Event_by_session')
        for week,session_in_week in enumerate(sessions_animals):
            # Retrieve dataframe for each sessions
            for i_session, session in enumerate(session_in_week):
                filename = animal + '_' + session
                try:
                    LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
                    LFP_df["Filename"] = [filename] * len(LFP_df['Onset[datapoints]'])
                    LFP_df["Block"] = [week] * len(LFP_df['Onset[datapoints]'])
                    LFP_df["Animal"] = [animal] * len(LFP_df['Onset[datapoints]'])
                    LFP_df.to_pickle(filename + "_No_rescale_Info_LFP_" + name_channel)
                except:
                    print('No file for ' + session)

def LFP_varaince(animal, session, dir,name_channel,no_rescale=True,save=True):
    #############################################
    # Created: GL, August 2022
    # Goal: Calculate variance LFP bout
    #############################################
    dir = dir + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
    else:
        LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + name_channel)

    LFP_df['Variance'] = np.nan

    for i in range(0, LFP_df.shape[0]):
        if LFP_df.loc[i,'Artefact'] == False:
            event_EEG = LFP_df.loc[i, 'LFP']
            LFP_df.loc[i,'Variance'] = np.var(event_EEG)

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_" + name_channel)
    return

def LFP_autocorr(animal, session, dir,name_channel,no_rescale=True,save=True, show=False):
    #############################################
    # Created: GL, August 2022
    # Goal: Calculate autocorrealtion on a LFP bout
    #############################################
    dir = dir + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
    else:
        LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + name_channel)

    LFP_df['Autocorrelation'] = np.nan

    for i in range(0, LFP_df.shape[0]):
        if LFP_df.loc[i,'Artefact'] == False:
            event_EEG = LFP_df.loc[i, 'LFP']
            nlags = len(event_EEG)/2
            autocorr = acf(event_EEG, nlags=nlags)
            lag_half = np.min(np.argwhere(autocorr < 0.5))
            LFP_df.loc[i,'Autocorrelation'] = lag_half

            if show == True:
                # plot autocorrelation function
                title = filename + ' ' + name_channel + ' Pulse n°' + str(i)
                fig1 = plt.figure(title, figsize=(20, 5)).suptitle(title)
                gridspec.GridSpec(12, 12)
                ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=5, colspan=12)
                x = np.arange(0, len(event_EEG))
                ax1.plot(x, event_EEG, color='#403d3d')
                ax2 = plt.subplot2grid((12, 12), (6, 0), rowspan=5, colspan=12)
                tsaplots.plot_acf(event_EEG,ax=ax2, lags=nlags)
                ax2.scatter(lag_half,autocorr[lag_half],c='r',s=100)
                ax2.set(ylabel='Autocorr', xlabel='lag')
                ax2.text(lag_half, 0.8, 'lag half autocorr = ' + str(lag_half), size=10, color='purple')
                plt.subplots_adjust(hspace=0.98, bottom=0.03)
                plt.show()

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_" + name_channel)
    return

def LFP_skewness(animal, session, dir,name_channel,no_rescale=True,save=True,  show=False):
    #############################################
    # Created: GL, August 2022
    # Goal: Calculate skewness LFP bout
    #############################################
    dir = dir + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
    else:
        LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + name_channel)

    LFP_df['Skewness'] = np.nan

    for i in range(0, LFP_df.shape[0]):
        if LFP_df.loc[i,'Artefact'] == False:
            event_EEG = LFP_df.loc[i, 'LFP']
            skewness = stats.skew(event_EEG, bias=False)
            LFP_df.loc[i,'Skewness'] = np.abs(skewness)

            if show == True:
                # plot histogramm function
                title = filename + ' ' + name_channel + ' Pulse n°' + str(i)
                fig1 = plt.figure(title, figsize=(20, 5)).suptitle(title)
                gridspec.GridSpec(12, 12)
                ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=5, colspan=12)
                x = np.arange(0, len(event_EEG))
                ax1.plot(x, event_EEG, color='#403d3d')
                ax2 = plt.subplot2grid((12, 12), (6, 0), rowspan=5, colspan=12)
                ax2.hist(event_EEG,50)
                ax2.text(1, 50, 'skewness: ' + str(skewness), size=10, color='r')
                ax2.axvline(x=0, linestyle="dashed", linewidth=0.8, color='k')
                plt.subplots_adjust(hspace=0.98, bottom=0.03)
                plt.show()

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_" + name_channel)
    return

def LFP_SumLL(animal, session, dir,name_channel,no_rescale=True,save=True):
    #############################################
    # Created: GL, August 2022
    # Goal: Calculate SUM LL LFP bout
    #############################################
    dir = dir + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
    else:
        LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + name_channel)

    LFP_df['Sum LL'] = np.nan

    for i in range(0, LFP_df.shape[0]):
            event_EEG = LFP_df.loc[i, 'LFP']
            Sum_LL = np.sum(np.abs(np.diff(event_EEG)))
            LFP_df.loc[i,'Sum LL'] = np.abs(Sum_LL)

    LFP_df.loc[np.argwhere('Artefact' == True).flatten(), 'Sum LL'] = np.nan

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_" + name_channel)

    print(animal+" " + session +" Sum LL "+ name_channel)
    return

def Pearson_correlation_matrix(data):
    nb_channel = len(data)
    corr_matrix = np.zeros((nb_channel,nb_channel))
    p_val_matrix = np.zeros((nb_channel,nb_channel))
    for idx_1 in range(nb_channel):
        row_1 = data[idx_1]
        for idx_2 in range(nb_channel):
            row_2 = data[idx_2]
            corr, p_value = stats.pearsonr(row_1,row_2)
            corr_matrix[idx_1,idx_2] = np.abs(corr)
            p_val_matrix[idx_1,idx_2] = p_value

    return corr_matrix, p_val_matrix

def LFP_xcorrelation(animal, session, dir,ref_channel,no_rescale=True,save=True, show=False):
    #############################################
    # Created: GL, September 2022
    # Goal: For each channel, calculate spatial correlation with all other channels
    #############################################
    dir = dir + animal
    filename = animal + '_' + session
    list_df_by_channel = []
    # Load Ref_df dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        Ref_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + ref_channel)
    else:
        Ref_df = pd.read_pickle(filename + '_Info_LFP_' + ref_channel)

    Ref_df = Ref_df.loc[:, ['Onset[datapoints]','Artefact','Condition']]

    good_channels = Info_Experiment.get_list_good_channel(animal, type='LFP')
    for name_channel in good_channels:
        # Load LFP for each channels in ref df
        os.chdir(dir + '/Data_Event_by_session')
        if no_rescale == True:
            LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
        else:
            LFP_df = pd.read_pickle(filename + '_Info_LFP_' + name_channel)

        LFP_df['Channel'] = name_channel
        list_df_by_channel.append(LFP_df)

        Ref_df.loc[:, name_channel] = LFP_df['LFP']

    # Keep only LFP without artefact (based on Ref channel)
    data_df = Ref_df.loc[Ref_df['Artefact'] == False, :]

    #Creat coloumn to add mean xcorr for each channel
    mean_corr_per_channel = []
    for name_channel in good_channels:
        name = 'xcorr '+name_channel
        mean_corr_per_channel.append(name)
        data_df.loc[:,name] = np.nan

    for i_r,row in data_df.iterrows():
        data_LFP = np.array(row[good_channels].tolist())
        corr_matrix, p_val_matrix = Pearson_correlation_matrix(np.abs(data_LFP))
        corr_matrix[np.diag_indices(len(corr_matrix))] = np.nan  # Nan diagonal

        mean_corr_per_channel = np.nanmean(corr_matrix, axis=0)
        for i_c, channel in enumerate(mean_corr_per_channel):
            data_df.loc[i_r, channel] = mean_corr_per_channel[i_c]

        if show == True:
            divnorm = colors.TwoSlopeNorm(vmin=0, vcenter=0.5, vmax=1)
            title = filename + ' xcorr' + ' Pulse n°' + str(i_r)
            fig1 = plt.figure(title, figsize=(10, 5)).suptitle(title)
            gridspec.GridSpec(12, 12)
            ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=10, colspan=10)
            im = ax1.imshow(corr_matrix, norm=divnorm)
            ax1.set_xticks(np.arange(0, len(good_channels)))
            ax1.set_xticklabels(ax1.get_xticks(), rotation=90)
            # ax1.set_xticklabels(good_channels)
            ax1.set_yticks(np.arange(0, len(good_channels)))
            ax1.set_yticklabels(good_channels)

            ax2 = plt.subplot2grid((12, 12), (0, 10), rowspan=10, colspan=2)
            ax2.imshow(np.reshape(mean_corr_per_channel,(len(mean_corr_per_channel),1)), norm=divnorm)
            ax2.set_xticks([])

            ax3 = plt.subplot2grid((12, 12), (11, 1), rowspan=1, colspan=10)
            colorbar = mpl.colorbar.ColorbarBase(ax3, orientation='horizontal', cmap=matplotlib.cm.get_cmap('viridis'),norm=divnorm, label='Pearson correlation')
            plt.show()

    for i_ch,name_channel in enumerate(good_channels):
        LFP_df = list_df_by_channel[i_ch]
        LFP_df.loc[:,'Mean Spatial Correlation'] = data_df.loc[:,mean_corr_per_channel[i_ch]]
        if save == True:
            if no_rescale == True:
                LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
            else:
                LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_" + name_channel)

        print(animal+" " + session +" spatial correlation  "+ name_channel)
    return

def LFP_xcorrelation_all_channels(animal, session, dir,ref_channel,no_rescale=True,save=True, show=False):
    #############################################
    # Created: GL, September 2022
    # Goal: Calculate correlation across all channels
    #############################################
    dir = dir + animal
    filename = animal + '_' + session
    list_df_by_channel = []
    channel_order = Info_Experiment.get_channel_order(type='LFP')
    # Load Ref_df dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        Ref_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + ref_channel)
    else:
        Ref_df = pd.read_pickle(filename + '_Info_LFP_' + ref_channel)

    Ref_df = Ref_df.loc[:, ['Onset[datapoints]','Artefact','Condition','Block']]

    good_channels = Info_Experiment.get_list_good_channel(animal, type='LFP')
    for name_channel in channel_order:
        if np.isin(name_channel,good_channels):
            # Load LFP for each channels in ref df
            os.chdir(dir + '/Data_Event_by_session')
            if no_rescale == True:
                LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
            else:
                LFP_df = pd.read_pickle(filename + '_Info_LFP_' + name_channel)

            LFP_df['Channel'] = name_channel
            list_df_by_channel.append(LFP_df)

            Ref_df.loc[:, name_channel] = LFP_df['LFP']
        else:
            Ref_df.loc[:, name_channel] = np.nan

    # Keep only LFP without artefact (based on Ref channel)

    data_df = Ref_df.loc[Ref_df['Artefact'] == False, :]
    divnorm = colors.TwoSlopeNorm(vmin=0,vcenter=0.5,vmax=1)
    list_corr_matrix =[]
    for i_r,row in data_df.iterrows():
        data_LFP = np.array(row[channel_order].tolist())
        corr_matrix, p_val_matrix = Pearson_correlation_matrix_with_nan(np.abs(data_LFP))
        corr_matrix[np.diag_indices(len(corr_matrix))] = np.nan  # Nan diagonal
        list_corr_matrix.append(corr_matrix)

        mean_corr_per_channel = np.nanmean(corr_matrix)
        data_df.loc[i_r,'Mean Spatial Correlation'] = mean_corr_per_channel

        if show == True:
            title = filename + ' xcorr' + ' Pulse n°' + str(i_r)
            fig1 = plt.figure(title, figsize=(10, 5)).suptitle(title)
            gridspec.GridSpec(12, 12)
            ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=10, colspan=10)
            im = ax1.imshow(corr_matrix, norm=divnorm)
            ax1.set_xticks(np.arange(0, len(channel_order)))
            ax1.set_xticklabels(ax1.get_xticks(), rotation=90)
            # ax1.set_xticklabels(good_channels)
            ax1.set_yticks(np.arange(0, len(channel_order)))
            ax1.set_yticklabels(channel_order)

            ax3 = plt.subplot2grid((12, 12), (11, 1), rowspan=1, colspan=10)
            colorbar = mpl.colorbar.ColorbarBase(ax3, orientation='horizontal', cmap=matplotlib.cm.get_cmap('viridis'),norm=divnorm, label='Pearson correlation')
            plt.show()

    data_df.loc[:,'Correlation matrix'] = list_corr_matrix
    if save == True:
        if no_rescale == True:
            data_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_all_channel")
        else:
            data_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_all_channel" )

        print(animal+" " + session +" spatial correlation all channel ")
    return

def Norm_save_metric(animals, sessions_per_animal, metric, dir):
    # Normalize LFP metrics by week and animal, and save the dataframe
    for i_animal, animal in enumerate(animals):
        sessions = sessions_per_animal[animal]
        os.chdir(dir + '/' + animal + '/Data_Event_by_session')
        list_channel = Info_Experiment.get_list_good_channel(animal)
        for name_channel in list_channel:
            LFP_channel_df = []
            for session in sessions:
                filename = animal + '_' + session
                print(filename + ' ' +name_channel)
                LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
                LFP_df['Session'] = session
                LFP_channel_df.append(LFP_df)

            All_LFP_channel = pd.concat(LFP_channel_df, ignore_index=True)
            All_LFP_channel = Nomralization_LFP_metric_by_block(All_LFP_channel,metric)  # Normalized  pulse to Mean NaCl max int of the block

            for session in sessions:
                filename = animal + '_' + session
                LFP_session_df = All_LFP_channel[All_LFP_channel['Session']==session]
                LFP_session_df = LFP_session_df.reset_index(drop=True)
                LFP_session_df.to_pickle(dir + '/' + animal + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)

def Nomralization_LFP_metric_by_block(df, metric):
    all_block = np.sort(np.unique(df["Block"]))
    df['Normalized ' + metric] = np.nan
    for block in all_block:
        Mean_value_NaCl = np.mean(df[metric] [(df['Artefact'] ==  False) & (df['Condition'] == 'NaCl')& (df['Block'] == block)])
        df.loc[df['Block'] == block,'Normalized ' + metric] = df[metric][df['Block'] == block] / Mean_value_NaCl


    df['Normalized ' + metric] = df['Normalized ' + metric].astype(float)
    df[metric] = df[metric].astype(float)
    return (df)

def Nomralization_xcorr_matrice_by_block(df, metric):
    all_block = np.sort(np.unique(df["Block"]))
    df['Normalized ' + metric] = np.nan
    for block in all_block:
        List_matrix_NaCl = np.array(df[metric] [(df['Artefact'] ==  False) & (df['Condition'] == 'NaCl')& (df['Block'] == block)].tolist())
        mean_NaCl_matrix = np.nanmean(List_matrix_NaCl,axis=0)
        df.loc[df['Block'] == block,'Normalized ' + metric] = df[metric][df['Block'] == block].apply(lambda x: x / mean_NaCl_matrix)

    return (df)

def Diff_xcorr_matrice_by_block(df, metric):
    all_block = np.sort(np.unique(df["Block"]))
    df['Normalized ' + metric] = np.nan
    for block in all_block:
        List_matrix_NaCl = np.array(df[metric] [(df['Artefact'] ==  False) & (df['Condition'] == 'NaCl')& (df['Block'] == block)].tolist())
        mean_NaCl_matrix = np.nanmean(List_matrix_NaCl,axis=0)
        df.loc[df['Block'] == block,'Normalized ' + metric] = df[metric][df['Block'] == block].apply(lambda x: x - mean_NaCl_matrix)

    return (df)

def Inspect_outliers_autocorr(animal, session, dir,name_channel,no_rescale=True,save=True):
    #############################################
    # Created: GL, August 2022
    # Goal: Detect artefact in LFP bout
    #############################################
    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    dir = dir + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if no_rescale == True:
        LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
    else:
        LFP_df = pd.read_pickle(filename + '_Info_SP_LFP_' + name_channel)

    # Check Max value to check if artefact
    for metric in ['Autocorrelation']:
        for i, x  in LFP_df[metric].sort_values(ascending=False).iteritems():

            event_EEG = np.array(LFP_df.loc[i,'LFP'])
            autocorr = acf(event_EEG, nlags=len(event_EEG)/2)
            lag_half = np.min(np.argwhere(autocorr < 0.5))

            # plot autocorrelation function
            title = filename + ' ' + name_channel + ' Max Pulse n°' + str(i)
            fig1 = plt.figure(title, figsize=(20, 5)).suptitle(title)
            gridspec.GridSpec(12, 12)
            ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=5, colspan=12)
            x = np.arange(0, len(event_EEG))
            ax1.plot(x, event_EEG, color='#403d3d')
            ax2 = plt.subplot2grid((12, 12), (6, 0), rowspan=5, colspan=12)
            tsaplots.plot_acf(event_EEG, ax=ax2, lags=len(event_EEG)/2)
            ax2.scatter(lag_half, autocorr[lag_half], c='r', s=100)
            ax2.set(ylabel='Autocorr', xlabel='lag')
            ax2.text(lag_half, 0.8, 'lag half autocorr = ' + str(lag_half), size=10, color='purple')
            plt.subplots_adjust(hspace=0.98, bottom=0.03)
            plt.show()

            response = input('keep it?(y/n/c)')
            if response == "c":
                print('event before n° ', i, " kept but continue")
            elif response != "y":
                LFP_df.loc[i,'Artefact'] = True
                LFP_df.loc[i,'Autocorrelation'] = np.nan
                print('event before n° ', i, " removed")
            elif response == "y":
                print('event before n° ', i, " kept")
                break

        for metric in ['Autocorrelation']:
            for i, x in LFP_df[metric].sort_values(ascending=False, na_position='first')[::-1].iteritems():

                event_EEG = np.array(LFP_df.loc[i, 'LFP'])
                lag_half = LFP_df.loc[i, 'Autocorrelation']

                # plot autocorrelation function
                title = filename + ' ' + name_channel + ' Min Pulse n°' + str(i)
                fig1 = plt.figure(title, figsize=(20, 5)).suptitle(title)
                gridspec.GridSpec(12, 12)
                ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=5, colspan=12)
                x = np.arange(0, len(event_EEG))
                ax1.plot(x, event_EEG, color='#403d3d')
                ax2 = plt.subplot2grid((12, 12), (6, 0), rowspan=5, colspan=12)
                tsaplots.plot_acf(event_EEG, ax=ax2, lags=len(event_EEG) / 2)
                ax2.scatter(lag_half,0.5, c='r', s=100)
                ax2.set(ylabel='Autocorr', xlabel='lag')
                ax2.text(lag_half, 0.8, 'lag half autocorr = ' + str(lag_half), size=10, color='purple')
                plt.subplots_adjust(hspace=0.98, bottom=0.03)
                plt.show()

                response = input('keep it?(y/n/c)')
                if response == "c":
                    print('event before n° ', i, " kept but continue")
                elif response != "y":
                    LFP_df.loc[i, 'Artefact'] = True
                    LFP_df.loc[i, 'Autocorrelation'] = np.nan
                    print('event before n° ', i, " removed")
                elif response == "y":
                    print('event before n° ', i, " kept")
                    break

    if save == True:
        if no_rescale == True:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_No_rescale_Info_LFP_" + name_channel)
        else:
            LFP_df.to_pickle(dir + '/Data_Event_by_session/' + filename + "_Info_SP_LFP_" + name_channel)
    return

def Normalization_LFP_before_inj(df, metric):
    df['Normalized ' + metric] = np.nan
    Mean_SP_before = np.nanmean(df[metric] [(df[metric].notna()) & (df['Before / After Inj'] == 'Before')])
    df.loc[:,'Normalized ' + metric] = df[metric] / Mean_SP_before

    return (df)
def rolling_spike_count(animal, session, path,window_sec, no_rescale = True,show = False):
    ### Created November 2022 by GL
    # for animals with PYZ Sz without Pulse, calculate 1/f exponent on a rolling window before Sz
    # Need fif file with injection ('Injection') and seizure  ('Sz') annotated
    #####

    dir = path + animal
    filename = animal + '_' + session

    # Load LFP dataframe
    os.chdir(dir + '/Data_Event_by_session')

    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + animal + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    event_name = raw._annotations.description
    event_onset = np.round(raw._annotations.onset * Sampling_freq).astype(int)
    event_duration = np.round(raw._annotations.duration * Sampling_freq).astype(int)+1
    Sz_start = int(event_onset[event_name == 'Sz'][0])
    Inj = int(event_onset[event_name == 'Injection'] + event_duration[event_name == 'Injection'][0])
    Spike_start = event_onset[event_name == 'Spike']

    rolling_window = np.arange(Inj,Sz_start-(1* Sampling_freq),1* Sampling_freq)
    spike_count = np.zeros(len(rolling_window))
    for i, wind in np.ndenumerate(rolling_window):
        index_window = np.arange(wind,wind+1*Sampling_freq,1)
        sum_spike = sum(np.isin(Spike_start,index_window))
        spike_count[i] = sum_spike


    time_before_sz_sec = (Sz_start-Inj) / Sampling_freq
    x = np.arange(-time_before_sz_sec+1,0, 1)
    df_spike_count = pd.DataFrame({'Time before Sz [s]': x, 'Spike Count': spike_count})
    df_spike_count['Rolling Spike Count'] = df_spike_count['Spike Count'].rolling(window_sec).sum()#.shift(-10)

    if show == True:
        title = filename + ' spike count before Chemical Sz'
        fig1 = plt.figure(title, figsize=(16, 8)).suptitle(title)
        gridspec.GridSpec(12, 12)
        ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
        ax1.plot(x,spike_count)
        ax1.plot(x,df_spike_count['Rolling Spike Count'])
        ax1.set_xlabel('Time[s]')
        ax1.set_ylabel('Spike per '+str(window_sec)+'s')

        plt.show()


    if no_rescale == True:
        df_spike_count.to_pickle(dir + '/Data_Event_by_session/' + filename + "_spike_count_before_Sz")
    else:
        df_spike_count.to_pickle(dir + '/Data_Event_by_session/' + filename + "_spike_count_before_Sz_rescale")
