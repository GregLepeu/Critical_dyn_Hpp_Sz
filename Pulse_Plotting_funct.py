import numpy as np
import pandas as pd
import matplotlib.animation as animation
import os as os
from mne import io
import scipy.io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.gridspec as gridspec
import matplotlib.ticker
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.patches as patches
from PIL import Image
import seaborn as sns
from scipy import integrate
from scipy import stats
import dabest
import Info_Experiment
import Pulse_Analysis_funct


##############################
#Single Pulse in an example animal
##############################
def SP_mean_trace_and_LL_per_intensitiy_1session(animal,session,dir,name_channel,metric,protocol,time_window,no_rescale=True,highpass=None):
    # From one session, plot mean trace in function of pulse intensities.
    filename = animal + '_' + session
    dir = dir + animal

    # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
    if no_rescale == True:
        os.chdir(dir + '/Pre-processed_No_rescale_fif')
        raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
    else:
        os.chdir(dir + animal + '/Pre-processed_data_fif')
        raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

    Sampling_freq = int(raw.info['sfreq'])
    channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()
    time_window_datapoints = int(time_window * Sampling_freq / 1000)

    if highpass != None:
        # Filter signal at 3Hz before calculating P2P
        raw = raw.filter(l_freq=highpass, h_freq=800, picks=channel, phase="zero")
    data = raw[:, :][0]

    # Load SP dataframe
    os.chdir(dir + '/Data_Event_by_session')
    if protocol == 'SP':
        if no_rescale == True:
            SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
        else:
            SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + name_channel)

    all_diff_intensity = np.sort(np.unique(SP_df['Intensity[v]']))

    Mean_EEG_by_intensity = []
    SD_EEG_by_intensity = []
    for intensity in all_diff_intensity:
        index_intensity = np.where(np.logical_and(SP_df['Intensity[v]'] == intensity, SP_df[metric].notna()))[0]
        onset_SP = SP_df['Onset[datapoints]'] [index_intensity]
        EEG_by_intensity=[]
        for event in onset_SP:
            event_EEG = data[channel,int(event - time_window_datapoints/2):int(event + time_window_datapoints)].flatten()
            event_EEG = event_EEG - np.mean(event_EEG[:int(time_window_datapoints/2)])
            EEG_by_intensity.append(event_EEG)

        Mean_EEG_by_intensity.append(np.array(np.mean(EEG_by_intensity,axis=0)))
        SD_EEG_by_intensity.append(np.array(np.std(EEG_by_intensity,axis=0)))

    title = filename + " " + name_channel + " Mean SP response per intensity " + str(time_window)+ 'ms ' + protocol
    fig1 = plt.figure(title, figsize=(15, 8)).suptitle(title)
    divnorm = colors.TwoSlopeNorm(vmin=0.4,vcenter=1.0,vmax=1.6)
    color_code = plt.cm.hot(divnorm(all_diff_intensity))
    gridspec.GridSpec(12, 12)
    ax1= plt.subplot2grid((12, 12), (0, 0), rowspan=5, colspan=12)
    x = np.arange(-time_window/2, time_window, 1000 / Sampling_freq)
    for i in range(len(all_diff_intensity)):
        ax1.plot(x,Mean_EEG_by_intensity[i], color=color_code[i], label=str(all_diff_intensity[i])+' [V]')
    ax1.axvspan(0, 3, edgecolor='#1B2ACC', facecolor='#089FFF', linestyle="--", lw=1)
    ax1.set_xlabel('[ms]')
    ax1.set_ylabel('[uV]')

    ax2 = plt.subplot2grid((12, 12), (6, 0), rowspan=5, colspan=12)
    gridspec.GridSpec(12, 12)
    sns.lineplot(ax=ax2, data=SP_df, x="Intensity[v]", y=metric, marker='o',palette='grey')
    ax2.set_xlabel("Intensity[v]")
    ax2.set_ylabel(metric)

    ax3 = plt.subplot2grid((12, 12), (11, 0), rowspan=1, colspan=12)
    colorbar = mpl.colorbar.ColorbarBase(ax3, orientation='horizontal', cmap= matplotlib.cm.get_cmap('hot'), norm=divnorm)
    ax3.set_xlim(right=1.0)
    ax3.set_xlabel('Intensity [V]')

    title = filename + " " + name_channel + " LL per intensity"
    fig2 = plt.figure(title, figsize=(15, 8)).suptitle(title)
    divnorm = colors.TwoSlopeNorm(vmin=0.4, vcenter=1.0, vmax=1.6)
    color_code = plt.cm.hot(divnorm(all_diff_intensity))
    ax1 = plt.subplot2grid((12, 12), (6, 0), rowspan=5, colspan=12)
    gridspec.GridSpec(12, 12)
    for i in range(len(all_diff_intensity)):
        Mean_EEG = Mean_EEG_by_intensity[i]
        Sum_LL = np.sum(np.abs(np.diff(Mean_EEG[int(time_window_datapoints/2):int(time_window_datapoints)])))/time_window
        ax1.plot([0, Sum_LL], [-i, -i], color=color_code[i], label=str(all_diff_intensity[i]) + ' [V]')
    ax1.set_xlabel("LL [uV/ms]")
    ax1.set_ylabel("Intensity[v]")
def SP_mean_trace_across_conditions(animal,name_channel,sessions,dir,intensity,metric,hue_order,time_window,no_rescale=True,highpass=None):
    # Plot the mean trace of a single pulse response for each conditions
    my_color_palette = Info_Experiment.get_color_cnd()
    EEG_SP_by_session=[]
    condition_by_session=[]
    for session in sessions:
        filename = animal + '_' + session
        # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
        if no_rescale == True:
            os.chdir(dir + animal + '/Pre-processed_No_rescale_fif')
            raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
        else:
            os.chdir(dir + animal + '/Pre-processed_data_fif')
            raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

        Sampling_freq = int(raw.info['sfreq'])
        channel = np.argwhere(np.array(raw.ch_names) == name_channel).flatten()
        time_window_datapoints = int(time_window * Sampling_freq / 1000)

        if highpass != None:
            # Filter signal at 3Hz before calculating P2P
            raw = raw.filter(l_freq=highpass, h_freq=800, picks=channel, phase="zero")
        data = raw[channel, :][0].flatten()

        os.chdir(dir + '/' + animal + '/Data_Event_by_session')
        if no_rescale == True:
            try:
                ID_df = pd.read_pickle(filename + '_No_rescale_Info_ID50_' + name_channel)
                SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
                SP_df = pd.concat([SP_df, ID_df], ignore_index=True)
            except:
                SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
        else:
            try:
                ID_df = pd.read_pickle(filename + '_Info_ID50_' + name_channel)
                SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + name_channel)
                SP_df = pd.concat([SP_df, ID_df], ignore_index=True)
            except:
                SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + name_channel)

        all_diff_condition = np.unique(SP_df['Condition'])
        for condition_in_session in all_diff_condition:
            condition_by_session.append(condition_in_session)

        all_diff_intensity = np.sort(np.unique(SP_df['Intensity[v]']))
        index_intensity = np.where(np.logical_and(SP_df['Intensity[v]'] == intensity, SP_df[metric] != np.nan))[0]
        onset_SP = SP_df['Onset[datapoints]'][index_intensity]
        EEG_SP_session = []
        for event in onset_SP:
            event_EEG = data[int(event - time_window_datapoints / 2):int(event + time_window_datapoints)].flatten()
            EEG_SP_session.append(event_EEG)

        EEG_SP_by_session.append(np.array(EEG_SP_session))

    Mean_EEG_SP_by_cat =[]
    SD_EEG_SP_by_cat = []
    n_by_cat =[]

    all_condition = np.unique(condition_by_session)
    mask = np.isin(hue_order, all_condition)
    all_condition = np.array(hue_order)[mask]

    for cat in all_condition:
        index_session_cat = np.argwhere(np.array(condition_by_session)==cat).flatten()
        EEG_SP_by_cat =[]
        for s in index_session_cat:
            for EEG in EEG_SP_by_session[s]:
                EEG_SP_by_cat.append(EEG)
        Mean_EEG_SP_cat = np.mean(np.array(EEG_SP_by_cat), axis=0).flatten()
        n_by_cat.append(len(EEG_SP_by_cat))
        Mean_EEG_SP_by_cat.append(Mean_EEG_SP_cat)
        SD_EEG_SP_cat = np.std(np.array(EEG_SP_by_cat), axis=0).flatten()
        SD_EEG_SP_by_cat.append(SD_EEG_SP_cat)


    title = animal + " " + name_channel + " Mean " + str(intensity_found) +  "V SP response per category " + str(time_window) + 'ms'
    fig1 = plt.figure(title, figsize=(15, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    x = np.arange(-time_window / 2, time_window, 1000 / Sampling_freq)
    for i,cnd in enumerate(all_condition):
        color = my_color_palette[cnd]
        ax1.plot(x, Mean_EEG_SP_by_cat[i], label=cnd +' (n= '+str(n_by_cat[i])+' pulses)' ,color =color)
        ax1.fill_between(x, Mean_EEG_SP_by_cat[i] - SD_EEG_SP_by_cat[i],Mean_EEG_SP_by_cat[i] + SD_EEG_SP_by_cat[i], alpha=0.2, color = color)
    ax1.axvspan(0, 3, edgecolor='#1B2ACC', facecolor='#089FFF', linestyle="--",alpha=0.2, lw=1)
    ax1.set_xlabel('[ms]')
    ax1.set_ylabel('[uV]')
    ax1.legend()
    return
def SP_all_trace_across_conditions(animal,ref_channel,sessions,dir,hue_order, intensity,time_window,metric,no_rescale=True,highpass=None):
    my_color_palette = Info_Experiment.get_color_cnd()
    EEG_SP_by_session_by_channels=[]
    condition_by_session=[]
    list_channel = Info_Experiment.get_list_good_channel(animal, probe='no')
    for session in sessions:
        filename = animal + '_' + session
        # Retrieve data, Sampling Freq, channel number and timestamps pulse from FIF file
        if no_rescale == True:
            os.chdir(dir + animal+ '/Pre-processed_No_rescale_fif')
            raw = io.read_raw_fif(filename + '_filtered_No_rescale_raw.fif', preload=True)
        else:
            os.chdir(dir + animal+ '/Pre-processed_data_fif')
            raw = io.read_raw_fif(filename + '_filtered_raw.fif', preload=True)

        Sampling_freq = int(raw.info['sfreq'])
        channels =  np.where(np.isin(raw.ch_names, list_channel) == True)[0]
        time_window_datapoints = int(time_window * Sampling_freq / 1000)

        if highpass != None:
            # Filter signal at 3Hz before calculating P2P
            raw = raw.filter(l_freq=highpass, h_freq=800, picks=channels, phase="zero")
        data = raw[:, :][0]

        # Load SP dataframe
        os.chdir(dir + animal + '/Data_Event_by_session')
        if no_rescale == True:
            SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + ref_channel)
        else:
            SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + ref_channel)


        all_diff_condition = np.unique(SP_df['Condition'])
        for condition_in_session in all_diff_condition:
            condition_by_session.append(condition_in_session)

        all_diff_intensity = np.sort(np.unique(SP_df['Intensity[v]']))
        intensity_found = gl.find_nearest(all_diff_intensity, intensity)
        index_intensity = np.where(np.logical_and(SP_df['Intensity[v]'] == intensity_found, SP_df[metric] != np.nan))[0]
        onset_SP = SP_df['Onset[datapoints]'][index_intensity]

        EEG_by_channels = []
        for ch in channels:
            list_event_EEG = []
            for event in onset_SP:
                event_EEG = data[ch,int(event - time_window_datapoints / 2):int(event + time_window_datapoints)].flatten()
                list_event_EEG.append(event_EEG)
            EEG_by_channels.append(list_event_EEG)
        EEG_SP_by_session_by_channels.append(EEG_by_channels)

    Mean_EEG_by_cat_by_channel =[]
    SD_EEG_by_cat_by_channel = []
    n_by_cat =[]


    for cat in hue_order:
        index_session_cat = np.argwhere(np.array(condition_by_session)==cat).flatten()
        Mean_EEG_cat_by_channel = []
        SD_EEG_cat_by_channel = []
        for idx_ch,ch in enumerate(list_channel):
            EEG_channel_by_cat =[]
            for s in index_session_cat:
                    for EEG in EEG_SP_by_session_by_channels[s][idx_ch]:
                        EEG_channel_by_cat.append(EEG)
            Mean_EEG_channel_cat = np.mean(np.array(EEG_channel_by_cat), axis=0).flatten()
            Mean_EEG_cat_by_channel.append(Mean_EEG_channel_cat)
            SD_EEG_channel_cat = np.std(np.array(EEG_channel_by_cat), axis=0).flatten()
            SD_EEG_cat_by_channel.append(SD_EEG_channel_cat)
        n_by_cat.append(len(EEG_channel_by_cat))
        Mean_EEG_by_cat_by_channel.append(Mean_EEG_cat_by_channel)
        SD_EEG_by_cat_by_channel.append(SD_EEG_cat_by_channel)


    title = animal + " all channels" + " Mean " + str(intensity_found) +  "V SP response per category " + str(time_window) + 'ms'
    fig1 = plt.figure(title, figsize=(15, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    x = np.arange(-time_window / 2, time_window, 1000 / Sampling_freq)
    min_value = np.min(Mean_EEG_by_cat_by_channel); max_value = np.max(Mean_EEG_by_cat_by_channel)
    scaling_factor = (max_value-min_value)/1.5
    for i,cnd in enumerate(hue_order):
        color = my_color_palette[cnd]
        for idx_ch,data in enumerate(Mean_EEG_by_cat_by_channel[i]):
            ax1.plot(x, Mean_EEG_by_cat_by_channel[i][idx_ch] - idx_ch*scaling_factor, label=cnd +' (n= '+str(n_by_cat[i])+' pulses)',lw=0.5,color =color)
    ax1.axvspan(0, 3, edgecolor='#1B2ACC', facecolor='#089FFF', linestyle="--",alpha=0.2, lw=1)
    ax1.set_xlabel('[ms]')
    ax1.set_ylabel('[uV]')
    ax1.set_yticks(np.arange(-(len(list_channel)-1)*scaling_factor, 1, scaling_factor))
    ax1.set_yticklabels(np.flip(list_channel))
def SP_across_condition(animal, name_channel,sessions,path,metric):
    # For a given animal, plot mean input/ouput curve by condition
    my_color_palette = Info_Experiment.get_color_cnd()
    # Load SP dataframe
    SP_sessions = []
    condition_by_session = []
    os.chdir(path + animal + '/Data_Event_by_session')
    for session in sessions:
        filename = animal + '_' + session

        # Load SP dataframe
        SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
        SP_sessions.append(SP_df)

        all_diff_condition = np.unique(SP_df['Condition'])
        for condition_in_session in all_diff_condition:
            condition_by_session.append(condition_in_session)

    All_SP_df = pd.concat(SP_sessions, ignore_index=True)
    all_different_intensity = np.sort(np.unique(All_SP_df['Intensity[v]']))

    # For each condition and each intensity, the mean response is calculated with SD
    mean_resp_condition = []; std_resp_condition = [];all_intensity_per_session =[]
    all_diff_condition = np.unique(condition_by_session)
    for cat in all_diff_condition:
        mean_resp_int = []
        std_resp_int = []
        all_different_intensity = np.sort(np.unique(All_SP_df['Intensity[v]'][All_SP_df['Condition'] == cat]))
        all_intensity_per_session.append(all_different_intensity)
        for intensity in all_different_intensity:
            index_int = np.where(np.logical_and(np.logical_and(All_SP_df['Intensity[v]'] == intensity,All_SP_df['Condition'] == cat),All_SP_df[metric].notna()))[0]
            mean_resp = np.mean(All_SP_df[metric][index_int])
            mean_resp_int.append(mean_resp)
            std_resp = np.std(All_SP_df[metric][index_int])
            std_resp_int.append(std_resp)
        mean_resp_condition.append(np.array(mean_resp_int))
        std_resp_condition.append(np.array(std_resp_int))


    title = animal + ' SP across conditions ' + name_channel + ' ' + metric
    fig3 = plt.figure(title, figsize=(16, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    for i, cnd in enumerate(all_diff_condition):
        color = my_color_palette[cnd]
        n_condition = len(np.argwhere(np.array(condition_by_session) == cnd))
        ax1.errorbar(x=all_intensity_per_session[i], y=mean_resp_condition[i],
                     label=cnd+' (n= '+str(n_condition)+' sessions)', color=color)
        ax1.fill_between(all_intensity_per_session[i], mean_resp_condition[i] - std_resp_condition[i], mean_resp_condition[i] + std_resp_condition[i],
                         alpha=0.2, color=color)
    ax1.set_xticks(np.arange(np.min(all_different_intensity),np.max(all_different_intensity),0.05))
    ax1.set_xticklabels(np.round(np.arange(np.min(all_different_intensity),np.max(all_different_intensity),0.05),2))
    ax1.set_xlabel('TTL Intensity [V]')
    ax1.set_ylabel(metric)
    plt.legend()
    plt.subplots_adjust(left=0.05, right=0.95)


##############################
#Single Pulse across animals and sessions
##############################

def SP_mean_resp_across_conditions_bootstrap_norm_block(animals,channel,sessions_per_animals,dir,intensity, LL_window,hue_order,no_rescale=True):
    my_color_palette = Info_Experiment.get_color_cnd()
    metric = 'Sum LL ' + str(LL_window) + 'ms'
    SP_df_by_animal = []
    for i_animal, animal in enumerate(animals):
        good_channel = Info_Experiment.get_list_good_channel(animal)
        if np.isin(channel,good_channel) == True:
            os.chdir(dir+ animal + '/Data_Event_by_session')
            SP_sessions = []
            for session in sessions_per_animals[animal]:
                # Retrieve dataframe with paired pulses value for each sessions
                filename = animal + '_' + session
                if no_rescale == True:
                    SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + channel)
                else:
                    SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + channel)

                SP_sessions.append(SP_df)

            Animal_SP_df = pd.concat(SP_sessions, ignore_index=True)
            Animal_SP_df = Pulse_Analysis_funct.Nomralization_SP_by_block(Animal_SP_df, metric, intensity) #Normalized to Mean NaCl pulse of the block
            Animal_SP_df['Animal'] = animal
            SP_df_by_animal.append(Animal_SP_df)
        else:
            print('No '+channel+' in ' + animal)

    SP_df_all = pd.concat(SP_df_by_animal, ignore_index=True)

    SP_df_all = Pulse_Analysis_funct.Nan_after_sz_SP(SP_df_all,'Normalized ' + metric) #Remove all Pulse after a chemical Sz

    conditions = SP_df_all['Condition'].unique() #Remove conditions not present to avoid bug
    mask = np.isin(hue_order,conditions)
    hue_order = np.array(hue_order)[mask]
    SP_df_all['Animal x Block'] = SP_df_all['Animal'] + ' x ' + SP_df_all['Block'].astype(str)


    data_per_cat=[]
    for cnd in hue_order:
            points_cat = SP_df_all.loc[(SP_df_all['Condition']==cnd)& (SP_df_all['Intensity[v]']==intensity), :]
            Mean_Norm_resp = points_cat.groupby('Animal x Block')['Normalized '+metric].mean()
            Mean_resp = points_cat.groupby('Animal x Block')[metric].mean()
            Mean_data = pd.DataFrame({'Animal x Block':Mean_resp.index,'Normalized '+metric:Mean_Norm_resp.values,metric:Mean_resp.values, 'Condition':[cnd]*len(Mean_resp.values)})
            data_per_cat.append(Mean_data)

    df_int = pd.concat(data_per_cat,ignore_index=True)

    title = animals + '_'+ channel+ ' Mean Norm Response to SP '+ str(intensity) +'[v] by block Bootstrap ' + metric
    fig = plt.figure(title, figsize=(12, 10)).suptitle(title)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    ax1.axhline(y=1, color='k',  linewidth=0.5, alpha=0.8)
    multi_groups_unpaired = dabest.load(df_int,x="Condition", y='Normalized '+metric ,idx=hue_order)
    multi_groups_unpaired.mean_diff.plot(ax=ax1,raw_marker_size=4,swarm_ylim= [0,2],
                                     contrast_label="Mean difference 95%CI",contrast_ylim= [-0.5,0.5],custom_palette=my_color_palette)

    title = animals + '_'+ channel+ ' Mean Response to SP '+ str(intensity) +'[v] by block Bootstrap ' + metric
    fig = plt.figure(title, figsize=(12, 10)).suptitle(title)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    ax1.axhline(y=1, color='k',  linewidth=0.5, alpha=0.8)
    multi_groups_unpaired = dabest.load(df_int,x="Condition", y=metric ,idx=hue_order)
    multi_groups_unpaired.mean_diff.plot(ax=ax1,raw_marker_size=4,
                                     contrast_label="Mean difference 95%CI",custom_palette=my_color_palette)

def SP_AUC_across_condition_norm_block(animals, channel,sessions_per_animal,dir,hue_order,metric):
    # Metric can be metric
    my_color_palette = Info_Experiment.get_color_cnd()
    # Load SP dataframe
    All_SP_df = []
    for i_animal, animal in enumerate(animals):
        SP_animal_df = []
        sessions = sessions_per_animal[animal]
        os.chdir(dir + '/' + animal + '/Data_Event_by_session')
        name_channel = Pulse_Analysis_funct.correct_channel_name(channel, animal)
        good_channel = Info_Experiment.get_list_good_channel(animal)
        good_channel.append('all ch')
        if np.isin(name_channel, good_channel) == True:
            for session in sessions:
                filename = animal + '_' + session
                # Load SP dataframe
                SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
                SP_animal_df.append(SP_df)

            SP_animal_df = pd.concat(SP_animal_df, ignore_index=True)
            SP_animal_df = Pulse_Analysis_funct.Nomralization_Pulse_by_block(SP_animal_df, metric)  # Normalized pulse to Mean NaCl 1V of the block
            SP_animal_df['Animal'] = [animal] * len(SP_animal_df)
            All_SP_df.append(SP_animal_df)

    All_SP_df = pd.concat(All_SP_df, ignore_index=True)
    conditions = All_SP_df['Condition'].unique()  # Remove conditions not present to avoid bug
    mask = np.isin(hue_order, conditions)
    hue_order = np.array(hue_order)[mask]
    All_SP_df = All_SP_df[np.isin(All_SP_df['Condition'],hue_order)]

    animal_list = [] ;  AUC_list = []; Block_list = []; Cnd_list = []
    for animal in All_SP_df['Animal'].unique():
        for block in All_SP_df['Block'] [All_SP_df['Animal'] == animal].unique():
            for cnd in hue_order:
                df = All_SP_df [(All_SP_df['Animal'] == animal) & (All_SP_df['Block'] == block) &  (All_SP_df['Condition'] == cnd)]
                Intensities =  np.sort(df['Intensity[v]'].unique())
                Mean_value = df.groupby(['Intensity[v]'])['Normalized ' + metric].mean()
                AUC = integrate.trapz(Mean_value,Intensities)
                animal_list.append(animal);AUC_list.append(AUC); Block_list.append(block); Cnd_list.append(cnd)


    info_df = {'Animal':animal_list, 'AUC':AUC_list, 'Block':Block_list, 'Condition':Cnd_list}
    plot_df = pd.DataFrame(info_df)
    plot_df['AUC'] = plot_df['AUC'].replace(0,np.nan)
    plot_df['Animal x Block'] = plot_df['Animal'] + ' x ' + plot_df['Block'].astype(str)
    plot_df = Pulse_Analysis_funct.Nomralization_AUC_by_block(plot_df)

    title= animals +' '+ channel + ' AUC IO curve ' + metric
    fig1 = plt.figure(title, figsize=(8, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    mulit_groupe = dabest.load(plot_df, idx= hue_order,x="Condition", y='AUC')
    mulit_groupe.mean_diff.plot(ax=ax1,custom_palette=my_color_palette, swarm_label='AUC I/O curve')

    title= animals +' '+ channel + 'Norm AUC IO curve ' + metric
    fig1 = plt.figure(title, figsize=(8, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    mulit_groupe = dabest.load(plot_df, idx= hue_order,x="Condition", y='Normalized AUC')
    mulit_groupe.mean_diff.plot(ax=ax1,custom_palette=my_color_palette, swarm_label='Normalized AUC',swarm_ylim= [0,2],
                                     contrast_label="Mean difference 95%CI",contrast_ylim= [-0.5,0.5])
    ax1.axhline(y=1, color='k', linestyle='--', linewidth=0.5)

def SP_brain_map_across_conditions_norm_block(animals,sessions_per_animals,path,idx_intensity,LL_window,hue_order,no_rescale=True):
    # Plot SP response across channels in a brain map (Figure 6D)
    metric = 'Sum LL ' + str(LL_window) + 'ms'
    SP_df_by_animal = []
    for i_animal, animal in enumerate(animals):
        list_channels = Info_Experiment.get_list_good_channel(animal, type='LFP')
        os.chdir(path + animal + '/Data_Event_by_session')
        for name_channel in list_channels:
            SP_sessions = []
            for session in sessions_per_animals[animal]:
                # Retrieve dataframe with paired pulses value for each sessions
                filename = animal + '_' + session
                if no_rescale == True:
                    SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
                else:
                    SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + name_channel)

                SP_sessions.append(SP_df)

            Animal_SP_df = pd.concat(SP_sessions, ignore_index=True)
            Animal_SP_df = Pulse_Analysis_funct.Nomralization_Pulse_by_block(Animal_SP_df, LL_window,metric) #Normalized 1st and 2nd pulse to Mean NaCl Fisrt pulse of the block
            Animal_SP_df['Channel'] = [name_channel] * len(Animal_SP_df)

            SP_df_by_animal.append(Animal_SP_df)

    All_SP_df = pd.concat(SP_df_by_animal, ignore_index=True)

    channels_order = Info_Experiment.get_channel_order(type='LFP')
    intensity = ['Low Intensity', 'Medium Intensity', 'Max Intensity'][idx_intensity]
    All_SP_df = All_SP_df[(All_SP_df['Intensity [v]'] == intensity)]

    #### For Boostraping ####
    All_SP_df['Condition'] = pd.Categorical(All_SP_df.Condition.tolist(), categories=hue_order)
    All_SP_df['Channel'] = pd.Categorical(All_SP_df.Channel.tolist(), categories=channels_order)
    All_PP_df = All_SP_df[All_SP_df['Condition'].notna()]  # take out all pulse with cnd not in hue order
    All_PP_df.sort_values(by=['Channel', 'Condition'], inplace=True)
    All_PP_df['Channel x CND'] = All_PP_df['Channel'].astype(str) + ' ' + All_PP_df['Condition'].astype(str)
    all_condition = All_PP_df['Channel x CND'].unique()
    all_condition_nested = gl.nest_list(all_condition.tolist(), len(hue_order))
    multi_groupe = dabest.load(All_PP_df, idx=all_condition_nested, x='Channel x CND', y='Normalized Conditioning Pulse ' + metric, resamples=5000)
    result_Bootstrap = multi_groupe.mean_diff.statistical_tests

    conditions_mean_diff =  np.delete(hue_order, 0)
    df_by_cnd = []
    for i_cnd, cnd in enumerate(conditions_mean_diff):
        mean_diff = result_Bootstrap["difference"][i_cnd::len(conditions_mean_diff)]
        IC_95= result_Bootstrap["bca_high"][i_cnd::len(conditions_mean_diff)]
        IC_05 = result_Bootstrap["bca_low"][i_cnd::len(conditions_mean_diff)]
        p_value = result_Bootstrap["pvalue_permutation"][i_cnd::len(conditions_mean_diff)]
        value_df = {'Channel': channels_order,'Condition': [cnd] * len(mean_diff),'Mean Diff': mean_diff, 'IC 95': IC_95 , 'IC 05':IC_05, 'p_value perm': p_value}
        df_Cnd = pd.DataFrame(value_df,columns=['Channel','Condition', 'Mean Diff', 'IC 95', 'IC 05', 'p_value perm'])
        df_by_cnd.append(df_Cnd)
    df_all_cnd = pd.concat(df_by_cnd, ignore_index=True)

    title = animal + '_'+ ' Brain Map to Conditioning Pulse normalized by block ' + metric +' ' + intensity
    os.chdir(path+'Figures/')
    im = Image.open('Brain_axial.png') #laod brain image as tempalte
    fig2 = plt.figure(title, figsize=(15, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    col_cnd = int(12 / len(conditions_mean_diff))
    divnorm = colors.TwoSlopeNorm(vmin=-0.45, vcenter=0,vmax=0.45)
    cmap = matplotlib.cm.get_cmap('seismic')
    coor_per_ch = Info_Experiment.get_coor_per_ch()
    for i, cnd in enumerate(conditions_mean_diff):
        ax = plt.subplot2grid((12, 12), (0, i*col_cnd), rowspan=11, colspan=col_cnd)
        ax.set_title(cnd)
        ax.imshow(im)  # Display the brain image
        ax.set_xticks([])
        ax.set_yticks([])

        # Create a Circle patch for each brain region
        all_patches=[]
        for Channel in df_all_cnd['Channel']:
            Value = float(df_all_cnd['Mean Diff'][(df_all_cnd['Channel']==Channel) & (df_all_cnd['Condition']==cnd)])
            p_value = float(df_all_cnd['p_value perm'][(df_all_cnd['Channel']==Channel) & (df_all_cnd['Condition']==cnd)])
            if p_value > 0.005:
                Value = 0
            coor = coor_per_ch[Channel]
            color=cmap(divnorm(Value))
            cir =  patches.Circle(coor, radius=15, edgecolor='k', facecolor=color)
            all_patches.append(cir)

        for patch in all_patches:
            ax.add_patch(patch)

    ax1 =  plt.subplot2grid((12, 12), (11, 1), rowspan=1, colspan=10)
    colorbar = mpl.colorbar.ColorbarBase(ax1, orientation='horizontal',cmap=cmap,norm=divnorm, label='Normalized Mean Difference with NaCl')

def SP_NMF_AUC_norm_by_block_bootstrap(animals,sessions_per_animal,rank,dir,hue_order,metric,show=False,no_rescale=True):
    # Calculate NMF on normalized data by block AND channel, and calculate one AUC per block
    my_color_palette = Info_Experiment.get_color_cnd()
    AUC_df_per_block = []
    W_df_per_animal = []
    for i_animal, animal in enumerate(animals):
        os.chdir(dir + animal + '/Data_Event_by_session')
        list_channel = Info_Experiment.get_list_good_channel(animal, type='LFP')
        for name_channel in list_channel:
            SP_channel_all_session = []
            for session in sessions_per_animal[animal]:
                filename = animal + '_' + session
                if no_rescale == True:
                    SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_analogue_' + name_channel)
                else:
                    SP_df = pd.read_pickle(filename + '_Info_SP_analogue_' + name_channel)
                SP_df['Session'] = session
                SP_df['Channel'] = name_channel
                SP_channel_all_session.append(SP_df)

            SP_all_session = pd.concat(SP_channel_all_session,ignore_index=True)
            SP_all_session = Pulse_Analysis_funct.Nomralization_SP_by_block(SP_all_session, metric)


            if name_channel == list_channel[0]:
                SP_df_animal = SP_all_session.loc[:, ['Session', 'Intensity[v]', 'Onset[datapoints]', 'Condition', 'Block']]

            SP_df_animal[name_channel] = SP_all_session['Normalized '+metric]

        input_NMF = np.transpose(np.array(SP_df_animal.loc[:, list_channel]))
        W, H = Pulse_Analysis_funct.get_nnmf(input_NMF, rank)
        W_df = pd.DataFrame({'Animal' : [animal] * len(list_channel),'Channel':list_channel, 'Weight': W.flatten()})
        W_df_per_animal.append(W_df)

        H_matrix = SP_df_animal.loc[:,['Session','Intensity[v]', 'Onset[datapoints]', 'Condition', 'Block']]

        for i_H in range(H.shape[0]):
            H_matrix['H'+str(i_H+1)] = H[i_H]

        H_matrix = H_matrix.loc[H_matrix['H1'] > 0,:]
        all_block = H_matrix['Block'].unique()

        if show == True: # Plot basis functions and activation coefficient
            Pulse_Analysis_funct.plot_V_W_H(input_NMF, W, H, animal + ' SP norm NMF rank' + str(rank), list_channel )
            Pulse_Analysis_funct.plot_NMF_AUC_Ph(H_matrix,hue_order, my_color_palette,animal + ' SP norm NMF rank' + str(rank) + ' AUC per H')
            # plt.show()

        for block in all_block:
            H_matrix_block = H_matrix.loc[H_matrix['Block'] == block, :]
            AUC_df = Pulse_Analysis_funct.NMF_SP_get_AUC_per_block(H_matrix_block, hue_order, animal, block)
            AUC_df_per_block.append(AUC_df)

    all_AUC_df = pd.concat(AUC_df_per_block, ignore_index=True)

    all_AUC_df['Animal Block'] =   all_AUC_df['Animal'] +' '+  all_AUC_df['Block'].astype(str)
    all_block =  all_AUC_df['Animal Block'].unique()

    all_AUC_df['Normalized AUC'] = np.nan
    for a_block in all_block:
        all_AUC_df.loc[all_AUC_df['Animal Block']==a_block,'Normalized AUC'] = all_AUC_df.loc[all_AUC_df['Animal Block']==a_block, 'AUC'] - float(all_AUC_df.loc[(all_AUC_df['Condition'] == 'NaCl') & (all_AUC_df['Animal Block']==a_block), 'AUC'])

    # Plot mean difference of activation coefficient across conditions with 95%CI
    mulit_groupe = dabest.load(all_AUC_df, idx= hue_order, x="Condition", y='AUC')
    title = animals +" NMF norm SP AUC H1 block Bootstrapped"
    fig1 = plt.figure(title, figsize=(8, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    mulit_groupe.mean_diff.plot(ax=ax1,custom_palette=my_color_palette, raw_marker_size=4)

    # Plot mean difference of normalized activation coefficient across conditions with 95%CI
    mulit_groupe_norm = dabest.load(all_AUC_df, idx= hue_order, x="Condition", y='Normalized AUC')
    title = animals + " NMF norm SP AUC H1 block Bootstrapped Norm"
    fig2 = plt.figure(title, figsize=(10, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    ax.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    mulit_groupe_norm.mean_diff.plot(ax=ax,custom_palette=my_color_palette,raw_marker_size=4,swarm_label="I/O AUC normalized to NaCl",contrast_label="Mean difference 95%CI")

    mean_diff = mulit_groupe_norm.mean_diff.statistical_tests["difference"]
    bca_low = mulit_groupe_norm.mean_diff.statistical_tests["bca_low"]
    bca_high = mulit_groupe_norm.mean_diff.statistical_tests["bca_high"]
    p_value = mulit_groupe_norm.mean_diff.statistical_tests["pvalue_permutation"]
    os.chdir(dir + "/Values")
    info_df = {"Name": ['NMF_AUC_boostrapped_result']*len(mean_diff),'Condition':np.delete(hue_order,0), 'Mean Difference': mean_diff,'bca_low':bca_low,'bca_high':bca_high, 'p-value': p_value}
    NMF_AUC_boostrapped_result = pd.DataFrame(info_df)
    NMF_AUC_boostrapped_result.to_pickle('NMF_AUC_boostrapped_result')

    title = animals + ' NMF norm SP Brain Mean activation function'
    fig3 = plt.figure(title, figsize=(8, 8)).suptitle(title)
    im = Image.open(dir + 'Figures/Brain_axial.png')  # load brain image as tempalte

    All_W_df = pd.concat(W_df_per_animal, ignore_index=True)
    Mean_W_per_channel = All_W_df.groupby(['Channel'])['Weight'].mean()

    # Create color scale
    divnorm = colors.TwoSlopeNorm(vmin=np.min(Mean_W_per_channel),vcenter=np.median([np.min(Mean_W_per_channel),np.max(Mean_W_per_channel)]),vmax=np.max(Mean_W_per_channel))
    cmap = plt.get_cmap('jet')

    # For each channel, creat a cricle and color according to the normalized activation coefficient and plot them on brain image
    ax1 = plt.subplot2grid((12, 12), (0,0), rowspan=11, colspan=12)
    ax1.imshow(im)
    ax1.set_xticks([])
    ax1.set_yticks([])
    all_patches=[]
    coor_per_ch = Info_Experiment.get_coor_per_ch() #Coordinate on the brain image
    for Channel, Value in Mean_W_per_channel.iteritems():
        coor = coor_per_ch[Channel]
        color=cmap(divnorm(Value))
        cir =  patches.Circle(coor, radius=15, edgecolor='k', facecolor=color)
        all_patches.append(cir)

    for patch in all_patches:
        ax1.add_patch(patch)

    ax2 =  plt.subplot2grid((12, 12), (11, 1), rowspan=1, colspan=10)
    colorbar = mpl.colorbar.ColorbarBase(ax2, orientation='horizontal',cmap=cmap,norm=divnorm, label='Weights')
