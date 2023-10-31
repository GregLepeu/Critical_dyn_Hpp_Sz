import Passive_metrics_analysis_funct
import Info_Experiment
import matplotlib.pyplot as plt

# Created by GL, script to process passive metrics in between single pulse, and save them in pandas datafram


dir = 'X://4 e-Lab/Greg/Acute_Pharmaco_Mod/'
animal = 'Ent_CamK2_61'
list_sessions = ['S01','S02','S03','S04','S05','S07']
list_condition = Info_Experiment.condition_by_session(animal, list_sessions)
list_channel = Info_Experiment.get_list_good_channel(animal, type='LFP')


ref_channel = 'CA1 R'
channel_no_ref = list_channel.copy()
channel_no_ref.remove(ref_channel)

for i in range(len(list_sessions)):
    session = list_sessions[i]
    condition = list_condition[i]

    ## Create DF passive EEG metrics #####
    Passive_metrics_analysis_funct.LFP_DataFrame(animal,session,dir,ref_channel,condition, lowpass=100, highpass=0.5)
    ## Remove artefact based on LL
    Passive_metrics_analysis_funct.LFP_remove_artefact(animal, session, dir,ref_channel,Detection_window=250)

    ## Calculate the diffrent passive metrics on each LFP bout
    Passive_metrics_analysis_funct.LFP_autocorr(animal, session, dir,ref_channel, show=False)
    Passive_metrics_analysis_funct.Inspect_outliers_autocorr(animal, session, dir,ref_channel,no_rescale=True,save=True)
    Passive_metrics_analysis_funct.LFP_varaince(animal, session, dir,ref_channel)
    Passive_metrics_analysis_funct.LFP_skewness(animal, session, dir, ref_channel, show=False)
    Passive_metrics_analysis_funct.LFP_SumLL(animal, session, dir, ref_channel)
    Passive_metrics_analysis_funct.LFP_xcorrelation(animal, session, dir, ref_channel, no_rescale=True, save=True, show=False)
    Passive_metrics_analysis_funct.LFP_xcorrelation_all_channels(animal, session, dir, ref_channel, no_rescale=True, save=True,show=False)

######## For all the oters channels, automaticaly create DF and calculate metrics based on artefact rejection made for ref_channel
for session in list_sessions:
    for channel in channel_no_ref:
        Passive_metrics_analysis_funct.LFP_df_auto(animal,session,dir,channel,ref_channel, lowpass=100, highpass=0.5)
        Passive_metrics_analysis_funct.LFP_varaince(animal, session, dir,channel)
        Passive_metrics_analysis_funct.LFP_autocorr(animal, session, dir,channel, show=False)
        Passive_metrics_analysis_funct.LFP_skewness(animal, session, dir, channel, show=False)
        Passive_metrics_analysis_funct.LFP_SumLL(animal, session, dir, channel)
        Passive_metrics_analysis_funct.LFP_xcorrelation(animal, session, dir, channel, no_rescale=True, save=True, show=False)



plt.show()
