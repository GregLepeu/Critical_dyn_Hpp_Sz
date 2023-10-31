import Pulse_Plotting_funct
import matplotlib.pyplot as plt

dir = '/Volumes/LaCie/Acute_Pharmaco_Mod/'
animal = "Ent_CamK2_09"
name_channel = "CA1 R"
animals = ["Ent_CamK2_03","Ent_CamK2_04","Ent_CamK2_06","Ent_CamK2_09","Ent_CamK2_10","Ent_CamK2_11","Ent_CamK2_15","Ent_CamK2_16","Ent_CamK2_34","Ent_CamK2_39","Ent_CamK2_40","Ent_CamK2_42","Ent_CamK2_54","Ent_CamK2_55","Ent_CamK2_56","Ent_CamK2_57", "Ent_CamK2_58"]

sessions_per_animals  = { "Ent_CamK2_03" :['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12'],
                        "Ent_CamK2_04": ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11','S12'],
                        "Ent_CamK2_06": ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11','S12'],
                        "Ent_CamK2_09" :['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12'],#'S13'
                        "Ent_CamK2_10" : ['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S13','S14','S15','S16','S21','S22','S23'],#,'S16','S17','S18','S19','S20'
                        "Ent_CamK2_11" : ['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S13','S14','S15','S16','S20','S21','S22'],#,'S16','S17','S18','S19','S20'
                        "Ent_CamK2_12": ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10','S11', 'S12','S13', 'S14', 'S15', 'S16','S21'],
                        "Ent_CamK2_15" : ['S01','S02','S03','S04','S05','S06','S07'],
                        "Ent_CamK2_16" : ['S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S13','S14','S15','S16','S21','S22','S23','S24'],#,'S16','S17','S18','S19','S20'
                        "Ent_CamK2_34": [ 'S20', 'S21', 'S22'],
                        "Ent_CamK2_39": [ 'S13', 'S14'],
                        "Ent_CamK2_40": ['S12', 'S13', 'S14'],
                        "Ent_CamK2_42": [ 'S16', 'S17','S18'],
                        "Ent_CamK2_54": ['S10', 'S11', 'S12', 'S13', 'S14'],
                        "Ent_CamK2_55": ['S10', 'S11', 'S12', 'S13', 'S14'],
                        "Ent_CamK2_56": ['S10', 'S11', 'S12', 'S13', 'S14'],
                        "Ent_CamK2_57": ['S10', 'S11', 'S12', 'S13', 'S14'],
                        "Ent_CamK2_58": ['S10', 'S11', 'S12', 'S13', 'S14'],
                          }

conditions_GABA = ['NaCl','Dz 5mg/kg','PTZ 20mg/kg']
LL_window = 250
metric = 'Sum LL ' + str(LL_window) + 'ms'
intensity = 1

### For an example animal ###
sessions = sessions_per_animals[animal]

# Plot the mean trace of a single pulse response for each conditions
Pulse_Plotting_funct.SP_mean_trace_across_conditions(animal,name_channel,sessions,dir,intensity,metric,conditions_GABA,time_window=500)
Pulse_Plotting_funct.SP_all_trace_across_conditions(animal,name_channel,sessions,dir,conditions_GABA, intensity,time_window=500,metric=metric)

#  Across intensities, plot input/out curve
Pulse_Plotting_funct.SP_across_condition(animal, name_channel,sessions,dir,metric)


### Across animals ###

# For a given intensity, calculate and plot the mean response with bootstrapped 95%CI
Pulse_Plotting_funct.SP_mean_resp_across_conditions_bootstrap_norm_block(animals,name_channel,sessions_per_animals,dir,intensity, LL_window,conditions_GABA)

# Across intensities, calculate and plot the mean area under the I/O curve with bootstrapped 95%CI
Pulse_Plotting_funct.SP_AUC_across_condition_norm_block(animals, name_channel,sessions_per_animals,dir,protocol='SP',hue_order=conditions_GABA,metric=metric,no_rescale = True)

# Same as before, but the network level using NMF
Pulse_Plotting_funct.SP_NMF_AUC_norm_by_block_bootstrap(animals,sessions_per_animals,1,dir,conditions_GABA,metric,show=False)