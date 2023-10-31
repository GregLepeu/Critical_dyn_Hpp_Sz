
import matplotlib.pyplot as plt
from Lepeu_Nat_Com_2023 import Pulse_Analysis_funct
import GL_Pulse_Plot
from Lepeu_Nat_Com_2023 import Info_Experiment

# Created by GL, script to process responses to opotgentic pulse, and save them in pandas datafram

animal = 'Ent_CamK2_09'
dir =  '/Volumes/LaCie/Acute_Pharmaco_Mod/'
list_sessions =  ['S01', 'S02', 'S03']
list_condition = Info_Experiment.condition_by_session(animal, list_sessions) #Load the pharamlogical conditions for each session
list_channel = Info_Experiment.get_list_good_channel(animal, type='LFP') #Get the list of good chanel (no artefact) for a given animal


ref_channel = 'CA1 R' # Channel used to discard pulses with artefacts
list_channel.remove(ref_channel)

LL_window = 250 #Window in ms used to calcualte the line-length of single-pulse responses
LL_window_train = 53 #Window in ms used to calcualte the cumulatinve line-length in train stim (for 20Hz=> 50ms + 3ms pulse length)

metric = 'Sum LL ' + str(LL_window) + 'ms'
metric_train =  'Sum LL ' + str(LL_window_train) + 'ms'

for i in range(len(list_sessions)):
    session = list_sessions[i]
    condition = list_condition[i]

    ## Create DF for the different Stim protocol #####
    Pulse_Analysis_funct.SP_DataFrame(animal,session, dir, ref_channel, condition)
    Pulse_Analysis_funct.Train_DataFrame(animal, session, dir, ref_channel, condition)

    ###### Calculate metric in resposne to Stim and reject artefacts #######
    Pulse_Analysis_funct.SP_Sum_LL(animal, session, dir, ref_channel, Detection_window=LL_window,time_window=LL_window, lowpass=100, highpass=0.5,save=False)
    Pulse_Analysis_funct.Train_Sum_LL(animal, session,dir,ref_channel,time_window=LL_window_train,highpass=0.5, lowpass=100)

    #### Plot stim response #########
    GL_Pulse_Plot.SP_mean_trace_and_LL_per_intensitiy_1session(animal,session, dir, ref_channel,metric=metric,protocol="SP",time_window=LL_window)
    plt.show()


######## For all the oters channels, automaticaly create DF and calculate metric based on artefact rejection made for ref_channel
for session in list_sessions:
    for channel in list_channel:
        Pulse_Analysis_funct.SP_df_auto(animal, session, dir, channel, ref_channel)

        Pulse_Analysis_funct.SP_Sum_LL_auto(animal, session, dir, channel,ref_channel, Detection_window=LL_window, lowpass=100, highpass=0.5)
        Pulse_Analysis_funct.Train_Sum_LL_auto(animal, session, dir, channel, ref_channel,time_window=LL_window_train, highpass=0.5, lowpass=100)

