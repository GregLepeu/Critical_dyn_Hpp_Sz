import Info_Experiment
import Pulse_Analysis_funct
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors
import matplotlib.patches as patches
import os
import dabest
from PIL import Image

#### Scirpt made by GL, corresponding to figure 7.
# Look at dynamic of single pulse responses (LL) as well as passive metrics before PTZ induced seizures.


dir = '/Volumes/LaCie/Acute_Pharmaco_Mod/'

animals=["Ent_CamK2_24","Ent_CamK2_34","Ent_CamK2_38","Ent_CamK2_59","Ent_CamK2_60","Ent_CamK2_61","Ent_CamK2_62","Ent_CamK2_63","Ent_CamK2_64"]#,"Ent_CamK2_11","Ent_CamK2_16"] #Ent_CamK2_38 and 60 removed because no Ind Stim at 20Hz


name_channel ="CA1 R"

sessions_per_animals  = {"Ent_CamK2_24": ['S28','S29','S30'],"Ent_CamK2_34": ['S23'],"Ent_CamK2_38": ['S24','S25'],
                         "Ent_CamK2_59": ['S01','S02','S03','S04','S05','S06'],"Ent_CamK2_60": ['S03','S04'],
                         "Ent_CamK2_61": ['S01','S02','S03','S05','S07'],"Ent_CamK2_62": ['S01','S02','S03','S04','S05','S06'],
                         "Ent_CamK2_63": ['S01','S02','S03','S04','S05','S06'],"Ent_CamK2_64": ['S01','S02','S03','S04']}

LL_window = 250

conditions_GABA = ["NaCl", 'PTZ 20mg/kg']
condition_Conv_PTZ = ['No inj','Convulsive PTZ'] #'PTZ error', 'Convulsive PTZ'

def SP_Mean_dynamic_Chemical_Sz_by_session(animals, sessions_per_animals,name_channel,path,LL_window,decimal,no_rescale = True):
    my_color_palette = Info_Experiment.get_color_cnd()
    metric = 'Sum LL ' + str(LL_window) + 'ms'
    List_all_mean_df = []
    for idx_animal, animal in enumerate(animals):
        good_channel = Info_Experiment.get_list_good_channel(animal)
        if np.isin(name_channel, good_channel) == True:
            os.chdir(path + animal + '/Data_Event_by_session')
            for session in sessions_per_animals[animal]:
                # Retrieve dataframe with paired pulses value for each sessions
                filename = animal + '_' + session
                if no_rescale == True:
                    SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_' + name_channel)
                else:
                    SP_df = pd.read_pickle(filename + '_Info_SP_' + name_channel)
                SP_df = Pulse_Analysis_funct.Normalization_SP_before_inj(SP_df, metric)
                SP_df['Filename'] = filename
                SP_df['Distance from Injection [min]'] = np.round(SP_df['Distance from Injection [s]'] / 60, decimals=decimal)
                SP_df['Distance from Sz [min]'] = np.round(SP_df['Distance from Sz[s]'] / 60, decimals=decimal)
                SP_df.loc[SP_df['Distance from Sz[s]'] > 0, 'Distance from Sz [min]'] = SP_df['Distance from Sz [min]'] + 1
                SP_df = SP_df.loc[SP_df['Distance from Sz[s]'].notna()]
                SP_df.loc[(SP_df['Condition'] == 'PTZ 40mg/kg') | (SP_df['Condition'] == 'PTZ 30mg/kg') | (SP_df['Condition'] == 'PTZ 25mg/kg'), 'Condition'] = 'Convulsive PTZ'
                SP_df.loc[SP_df['Before / After Sz'] == 'After', ['Condition']] = 'Post-Ictal'
                mean_SP_df = SP_df.groupby(['Distance from Sz [min]']).agg(
                    {'Filename': ['first'], 'Normalized ' + metric: ['mean', 'std'],
                     'Distance from Sz [min]': ['first'], 'Distance from Injection [min]': ['first'],
                     'Condition': ['first']})
                mean_SP_df.columns = ['Filename', 'Mean Normalized ' + metric, 'SD Normalized ' + metric,
                                          'Distance from Sz [min]', 'Distance from Injection [min]', 'Condition']
                mean_SP_df = mean_SP_df.reindex()
                List_all_mean_df.append(mean_SP_df)
        else:
            print('No ' + name_channel + ' in ' + animal)

    All_SP_df = pd.concat(List_all_mean_df, ignore_index=True)
    Inj_time = np.min(All_SP_df.loc[All_SP_df['Condition'] == 'Convulsive PTZ', 'Distance from Sz [min]']) - 1
    All_SP_df.loc[All_SP_df['Condition'] == 'No inj', ['Distance from Sz [min]']] = All_SP_df['Distance from Injection [min]'] - abs(Inj_time) #Realgin all baseline

    title = gl.list_to_string(animals) + '_' + name_channel + ' Mean SP by animal distance from Sz '+ metric
    fig1 = plt.figure(title, figsize=(16, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    sns.lineplot(ax=ax1, data=All_SP_df, x='Distance from Sz [min]', y='Mean Normalized ' + metric,  ci=None, zorder=0, hue="Condition", palette=my_color_palette)
    for df in List_all_mean_df:
        df.loc[df['Condition'] == 'No inj', ['Distance from Sz [min]']] = df['Distance from Injection [min]'] - abs(Inj_time) #Realgin all baseline
        sns.lineplot(ax=ax1, data=df, x='Distance from Sz [min]', y='Mean Normalized ' + metric, ci=None,zorder=0, lw=0.5, alpha=0.5,hue="Condition", palette=my_color_palette)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
    ax1.axhline(y=1, color='k', linestyle='--', linewidth=0.5)
    ax1.axvspan(0, 1, edgecolor='w', facecolor='w', linestyle="--", alpha=1, lw=0.1, zorder=1)
    ax1.text(10, -0.05, ' n=' + str(len(List_all_mean_df)),horizontalalignment='center')
    ax1.set_xlim(left=-32)
    ax1.legend([])

def SP_Mean_dynamic_Chemical_Sz_NMF_by_session(animals, sessions_per_animals,path,decimal,no_rescale = True):
    my_color_palette = Info_Experiment.get_color_cnd()
    rank = 'H1'
    List_all_mean_df = []
    for idx_animal, animal in enumerate(animals):
            os.chdir(path + animal + '/Data_Event_by_session')
            for session in sessions_per_animals[animal]:
                # Retrieve dataframe with paired pulses value for each sessions
                filename = animal + '_' + session
                if no_rescale == True:
                    SP_df = pd.read_pickle(filename +'_No_rescale_Info_SP_NMF_rank1')
                else:
                    SP_df = pd.read_pickle(filename + '_Info_SP_NMF_rank1')
                SP_df = Pulse_Analysis_funct.Normalization_SP_before_inj(SP_df, rank)
                SP_df['Filename'] = filename
                SP_df['Distance from Injection [s]'] = SP_df['Distance from Sz[s]'] - np.min(
                    SP_df.loc[SP_df['Before / After Inj'] == 'After', 'Distance from Sz[s]'])
                SP_df['Distance from Injection [min]'] = np.round(SP_df['Distance from Injection [s]'] / 60, decimals=decimal)
                SP_df['Distance from Sz [min]'] = np.round(SP_df['Distance from Sz[s]'] / 60, decimals=decimal)
                SP_df.loc[SP_df['Distance from Sz[s]'] > 0, 'Distance from Sz [min]'] = SP_df['Distance from Sz [min]'] + 1
                SP_df = SP_df.loc[SP_df['Distance from Sz[s]'].notna()]
                SP_df.loc[SP_df['Before / After Inj'] == 'Before', ['Condition']] = 'Control'
                SP_df.loc[(SP_df['Condition'] == 'PTZ 40mg/kg') | (SP_df['Condition'] == 'PTZ 30mg/kg') | ( SP_df['Condition'] == 'PTZ 25mg/kg'), 'Condition'] = 'Convulsive PTZ'
                SP_df.loc[SP_df['Before / After Sz'] == 'After', ['Condition']] = 'Post-Ictal'
                mean_SP_df = SP_df.groupby(['Distance from Sz [min]']).agg(
                    {'Filename': ['first'], 'Normalized ' + rank: ['mean', 'std'],
                     'Distance from Sz [min]': ['first'], 'Distance from Injection [min]': ['first'],
                     'Condition': ['first']})
                mean_SP_df.columns = ['Filename', 'Mean Normalized ' + rank, 'SD Normalized ' + rank,'Distance from Sz [min]', 'Distance from Injection [min]', 'Condition']
                mean_SP_df = mean_SP_df.reindex()
                List_all_mean_df.append(mean_SP_df)


    All_SP_df = pd.concat(List_all_mean_df, ignore_index=True)

    Inj_time = np.min(All_SP_df.loc[All_SP_df['Condition'] == 'Convulsive PTZ', 'Distance from Sz [min]']) - 1
    All_SP_df.loc[All_SP_df['Condition'] == 'Control', ['Distance from Sz [min]']] = All_SP_df['Distance from Injection [min]'] - abs(Inj_time) #Realgin all baseline to injection time

    title = gl.list_to_string(animals) + '_'  + 'mean SP NMF by animal distance from Sz ' + rank
    fig1 = plt.figure(title, figsize=(16, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    sns.lineplot(ax=ax1, data=All_SP_df, x='Distance from Sz [min]', y='Mean Normalized ' + rank,  ci=None, zorder=0, hue="Condition", palette=my_color_palette)
    for df in List_all_mean_df:
        df.loc[df['Condition'] == 'Control', ['Distance from Sz [min]']] = df['Distance from Injection [min]'] - abs(Inj_time)
        sns.lineplot(ax=ax1, data=df, x='Distance from Sz [min]', y='Mean Normalized ' + rank, ci=None,zorder=0, lw=0.5, alpha=0.5,hue="Condition", palette=my_color_palette)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
    ax1.axhline(y=1, color='k', linestyle='--', linewidth=0.5)
    ax1.axvspan(0, 1, edgecolor='w', facecolor='w', linestyle="--", alpha=1, lw=0.1, zorder=1)
    ax1.text(10, -0.05, ' n=' + str(len(List_all_mean_df)),horizontalalignment='center')
    ax1.set_xlim(left=-32)
    ax1.legend([], [], frameon=False)

def SP_brain_map_chemical_sz(animals,sessions_per_animals,path,LL_window,min_dist_Sz,max_dist_Sz,no_rescale=True):
    metric = 'Sum LL ' + str(LL_window) + 'ms'
    channels_order = Info_Experiment.get_channel_order(type='LFP')
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
                    SP_df = pd.read_pickle(filename + "_No_rescale_Info_SP_" + name_channel)
                else:
                    SP_df = pd.read_pickle(filename + "_Info_SP_" + name_channel)

                SP_df["Filename"] = [filename] * len(SP_df)
                SP_df["Channel"] = [name_channel] * len(SP_df)
                SP_df = Pulse_Analysis_funct.Normalization_SP_before_inj(SP_df, metric)
                SP_sessions.append(SP_df)

            Animal_SP_df = pd.concat(SP_sessions, ignore_index=True)
            SP_df_by_animal.append(Animal_SP_df)

    All_SP_df = pd.concat(SP_df_by_animal, ignore_index=True)
    All_SP_df['Distance from Sz [min]'] = (All_SP_df['Distance from Sz[s]'] / 60).round(0)

    list_channels =  All_SP_df['Channel'].unique()

    # Calculate diff between ctrl and before SZ
    Pulse_before = np.logical_or(np.logical_and(All_SP_df['Distance from Sz [min]'] >= min_dist_Sz , (All_SP_df['Distance from Sz [min]'] < max_dist_Sz)), All_SP_df['Before / After Inj'] == 'Before')
    All_SP_df_befroe = All_SP_df[Pulse_before] # Keep only pulse before inj (Ctrl) and after x min

    #### For Boostraping ####
    All_SP_df_befroe.loc[:,'Channel'] = pd.Categorical(All_SP_df_befroe.Channel.tolist(), categories=channels_order)
    All_SP_df_befroe.loc[:,'Before / After Inj'] = pd.Categorical(All_SP_df_befroe['Before / After Inj'].tolist(), categories=['Before', 'After'])
    All_SP_df_befroe.sort_values(by=['Channel', 'Before / After Inj'], inplace=True)
    All_SP_df_befroe.loc[:,'Channel x Before / After Inj'] = All_SP_df_befroe['Channel'].astype(str) + ' ' + All_SP_df_befroe['Before / After Inj'].astype(str)
    all_condition = All_SP_df_befroe['Channel x Before / After Inj'].unique()
    all_condition_nested = gl.nest_list(all_condition.tolist(), 2)
    multi_groupe_before = dabest.load(All_SP_df_befroe, idx=all_condition_nested, x='Channel x Before / After Inj', y='Normalized ' + metric, resamples=5000)
    result_Bootstrap_after = multi_groupe_before.mean_diff.statistical_tests

    mean_diff = result_Bootstrap_after["difference"]
    IC_95= result_Bootstrap_after["bca_high"]
    IC_05 = result_Bootstrap_after["bca_low"]
    p_value = result_Bootstrap_after["pvalue_permutation"]
    value_df_before = {'Channel': list_channels,'Mean Diff': mean_diff, 'IC 95': IC_95 , 'IC 05':IC_05, 'p_value perm': p_value}
    plot_df_before = pd.DataFrame(value_df_before,columns=['Channel', 'Mean Diff', 'IC 95', 'IC 05', 'p_value perm'])


    title = gl.list_to_string(animals) + '_'+ 'Brain Map SP Chemical Sz '+str(min_dist_Sz)+' to ' + str(max_dist_Sz) +'min to Sz' + metric
    os.chdir(path+'/Figures/')
    im = Image.open('Brain_axial.png') #laod brain image as tempalte
    fig2 = plt.figure(title, figsize=(10, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    divnorm = colors.TwoSlopeNorm(vmin=-0.45, vcenter=0,vmax=0.45)
    cmap = mpl.cm.get_cmap('seismic')
    coor_per_ch = Info_Experiment.get_coor_per_ch()

    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=11, colspan=6)
    ax1.imshow(im)  # Display the brain image
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Create a Circle patch for each brain region
    all_patches = []
    for Channel in plot_df_before['Channel']:
        Value = float(plot_df_before['Mean Diff'][(plot_df_before['Channel'] == Channel)])
        p_value = float(plot_df_before['p_value perm'][(plot_df_before['Channel'] == Channel)])
        if p_value > 0.005:
            Value = 0
        coor = coor_per_ch[Channel]
        color = cmap(divnorm(Value))
        cir = patches.Circle(coor, radius=15, edgecolor='k', facecolor=color)
        all_patches.append(cir)

    for patch in all_patches:
        ax1.add_patch(patch)

def SP_NMF_across_conditions_bootstrap_mean_by_session(animals, sessions_per_animal, path,min_dist_Sz,max_dist_Sz,hue_order):
    my_color_palette = Info_Experiment.get_color_cnd()
    rank = 'H1'
    list_df_metric = []
    for animal in animals:
        for session in sessions_per_animal[animal]:
            filename = animal+'_'+session
            os.chdir(path + animal+ '/Data_Event_by_session/')
            SP_df = pd.read_pickle(filename + '_No_rescale_Info_SP_NMF_rank1')

            SP_df = Pulse_Analysis_funct.Normalization_SP_before_inj(SP_df, rank)

            SP_df['Filename'] = filename
            SP_df['Distance from Sz [min]'] = (SP_df['Distance from Sz[s]'] / 60).round(0)
            SP_df.loc[SP_df['Distance from Sz[s]'] > 0, 'Distance from Sz [min]'] = SP_df['Distance from Sz [min]'] + 1
            SP_df = SP_df.loc[np.logical_or(SP_df['Before / After Inj'] == 'Before',np.logical_and(SP_df['Distance from Sz [min]'] > min_dist_Sz, SP_df['Distance from Sz [min]'] <= max_dist_Sz))]
            SP_df.loc[SP_df['Before / After Inj'] == 'Before', ['Condition']] = 'No inj'
            SP_df.loc[(SP_df['Condition'] == 'PTZ 40mg/kg') | (SP_df['Condition'] == 'PTZ 30mg/kg') | (SP_df['Condition'] == 'PTZ 25mg/kg'), 'Condition'] = 'Convulsive PTZ'
            SP_df.loc[SP_df['Before / After Sz'] == 'After', ['Condition']] = 'Post-Ictal'
            mean_SP_df = SP_df.groupby(['Condition']).agg({ 'Filename':['first'],'Normalized ' + rank: ['mean', 'std'], 'Condition':['first']})
            mean_SP_df.columns = ['Filename','Mean Normalized ' + rank, 'SD Normalized ' + rank, 'Condition']
            mean_SP_df =mean_SP_df.reindex()
            list_df_metric.append(mean_SP_df)


    all_df_metric = pd.concat(list_df_metric,ignore_index=True)


    title= gl.list_to_string(animals) +' NMF '+ str(min_dist_Sz)+' to '+str(max_dist_Sz)+ ' '+rank
    fig1 = plt.figure(title, figsize=(8, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)

    paired_group = dabest.load(all_df_metric, x="Condition",y='Mean Normalized ' + rank, idx=hue_order,paired=False, id_col='Filename')
    paired_group.mean_diff.plot(ax=ax1,custom_palette=my_color_palette)
    ax1.axhline(y=1, color='k', linestyle='--', linewidth=0.5)

def metric_Mean_dynamic_Chemical_Sz(animals, sessions_per_animals,name_channel,path,metric,no_rescale = True):
    # Plot passive metrics as warning signs (Supp. Figure 10)
    my_color_palette = Info_Experiment.get_color_cnd()

    List_all_mean_df = []
    for idx_animal, animal in enumerate(animals):
        good_channel = Info_Experiment.get_list_good_channel(animal)
        if np.isin(name_channel, good_channel) == True:
            os.chdir(path + animal + '/Data_Event_by_session')
            for session in sessions_per_animals[animal]:
                # Retrieve dataframe with paired pulses value for each sessions
                filename = animal + '_' + session
                print(filename)
                if no_rescale == True:
                    os.chdir(path + animal + '/Data_Event_by_session')
                    LFP_df = pd.read_pickle(filename + '_No_rescale_Info_LFP_' + name_channel)
                else:
                    os.chdir(path + animal + '/Data_Event_by_session')
                    LFP_df = pd.read_pickle(filename + '_Info_LFP_' + name_channel)
                LFP_df = Pulse_Analysis_funct.Normalization_LFP_before_inj(LFP_df, metric)

                mean_LFP_df = LFP_df.groupby(['Distance from Sz [min]']).agg(
                    {'Filename': ['first'], 'Normalized ' + metric: ['mean', 'std'],
                     'Distance from Sz [min]': ['first'], 'Distance from Injection [min]': ['first'],
                     'Condition': ['first']})
                mean_LFP_df.columns = ['Filename', 'Mean Normalized ' + metric, 'SD Normalized ' + metric,'Distance from Sz [min]', 'Distance from Injection [min]', 'Condition']
                List_all_mean_df.append(mean_LFP_df)
        else:
            print('No ' + name_channel + ' in ' + animal)

    All_LFP_df = pd.concat(List_all_mean_df, ignore_index=True)
    Inj_time = np.min(All_LFP_df.loc[(All_LFP_df['Condition'] == 'Convulsive PTZ')| (All_LFP_df['Condition'] == 'NaCl'), 'Distance from Sz [min]']) - 1
    All_LFP_df.loc[All_LFP_df['Condition'] == 'No inj', ['Distance from Sz [min]']] = All_LFP_df['Distance from Injection [min]'] - abs(Inj_time) #Realgin all baseline


    title = gl.list_to_string(animals) + '_' + name_channel + ' Mean ' + metric + ' distance from Sz'
    fig1 = plt.figure(title, figsize=(16, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    sns.lineplot(ax=ax1, data=All_LFP_df, x='Distance from Sz [min]', y='Mean Normalized ' + metric, ci=None, zorder=0,hue="Condition", palette=my_color_palette)
    for df in List_all_mean_df:
        df.loc[df['Condition'] == 'No inj', ['Distance from Sz [min]']] = df['Distance from Injection [min]'] - abs(Inj_time)  # Realgin all baseline
        sns.lineplot(ax=ax1, data=df, x='Distance from Sz [min]', y='Mean Normalized ' + metric, ci=None, zorder=0,lw=0.5, alpha=0.5, hue="Condition", palette=my_color_palette)
    ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
    ax1.axhline(y=1, color='k', linestyle='--', linewidth=0.5)
    ax1.axvspan(0, 1, edgecolor='w', facecolor='w', linestyle="--", alpha=1, lw=0.1, zorder=1)
    ax1.text(10, -0.05, ' n=' + str(len(List_all_mean_df)), horizontalalignment='center')
    ax1.set_xlim(left=-32)
    ax1.legend([])




SP_Mean_dynamic_Chemical_Sz_by_session(animals, sessions_per_animals,name_channel,dir,LL_window,0)

SP_brain_map_chemical_sz(animals,sessions_per_animals,dir,LL_window,min_dist_Sz=-5,max_dist_Sz=-2,no_rescale=True)

SP_NMF_across_conditions_bootstrap_mean_by_session(animals, sessions_per_animals, dir,min_dist_Sz=-8,max_dist_Sz=-7,hue_order=condition_Conv_PTZ)

SP_Mean_dynamic_Chemical_Sz_NMF_by_session(animals, sessions_per_animals,dir,0)


metric_Mean_dynamic_Chemical_Sz(animals, sessions_per_animals,name_channel,dir,'Autocorrelation')
metric_Mean_dynamic_Chemical_Sz(animals, sessions_per_animals,name_channel,dir,'Variance')
metric_Mean_dynamic_Chemical_Sz(animals, sessions_per_animals,name_channel,dir,'Skewness')
metric_Mean_dynamic_Chemical_Sz(animals, sessions_per_animals,name_channel,dir,'Mean Spatial Correlation')
metric_Mean_dynamic_Chemical_Sz(animals, sessions_per_animals,name_channel,dir,'Sum LL')


plt.show()