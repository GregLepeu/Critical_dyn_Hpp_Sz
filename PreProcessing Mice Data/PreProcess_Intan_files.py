import os
import time
import numpy as np
import mne
import matplotlib.pyplot as plt
from scipy import signal

# Scirpt created by GL
# Extract EEG, TTL and Accelerometers from intan ".dat" files based on the "open_IntanData_dat" function
#

def open_IntanData_dat(port,DigitalInput,channels,Recording):
    # Load .dat files and save them as .npy files (per channel)
    print(Recording)
    if channels[0]<10:
        dataname=str("amp-"+port+"-00"+str(channels[0]))
    if channels[0]>10:
        dataname=str("amp-"+port+"-0"+str(channels[0]))
    for i,x in enumerate(channels):
        v=len(str(x))
        dataname=dataname[:-v]+str(x)
        data=np.fromfile(str(dataname+".dat"),dtype=np.int16,sep="")
        data=0.195*data#convert electrode voltage in microvolts
        if i == 0:
            data_c = data
        else:
            data_c=np.vstack((data_c,data))
    if DigitalInput!=None:
        for DI in DigitalInput:
            ttl=np.fromfile(str(DI+".dat"),dtype=np.int,sep="")
            ttl = np.repeat(ttl, 2)
            a = np.count_nonzero(ttl)
            if a == 0:
                print(DI+' is empty')
            if len(ttl) == data_c.shape[1] -1:
                ttl = np.hstack((ttl,[0]))
            data_c = np.vstack((data_c, ttl))
            print("Digital Input Done")

    return data_c

dir =  '/Volumes/LaCie/Acute_Pharmaco_Mod/'  # path where to find the "Raw_data_Intan" containing the files

animals = ["Ent_CamK2_59"] # Animal to extract from the files
filenames = ["Ent_CamK2_59_Ent_CamK2_60_S01"] # List of files to loop through

Show = False # Specfiy if you want to plot the spectrgram as well as the extract traces
Sampling_freq = 2000 # in Hz

for filename in filenames:
    for animal in animals:
        os.chdir(dir + "/Raw_data_Intan/" + filename)
        session = filename[filename.rfind('_')+1:]
        file = animal +"_"+session
        start_all = time.time()
        # assign correct channels from the Intan recordings to animals
        if animal == "Ent_CamK2_59":
            port = "A"
            channels = np.arange(8, 24) #When only one 16 board is connect to a given porat, the chennels 8-24 are used
            Accelerometers = ["aux-A-AUX1", "aux-A-AUX2", "aux-A-AUX3"]
            ttl = ['board-DIGITAL-IN-01']
        elif animal == "Ent_CamK2_60":
            port = "A"
            channels = np.arange(40, 56)
            Accelerometers = ["aux-A-AUX4", "aux-A-AUX5", "aux-A-AUX6"]
            ttl = ['board-DIGITAL-IN-01']
        elif animal == "Ent_CamK2_61":
            port = "B"
            channels = np.arange(8, 24)
            Accelerometers = ["aux-B-AUX1", "aux-B-AUX2", "aux-B-AUX3"]
            ttl = ['board-DIGITAL-IN-01']
        elif animal == "Ent_CamK2_62":
            port = "B"
            channels = np.arange(40, 56)
            Accelerometers = ["aux-B-AUX4", "aux-B-AUX5", "aux-B-AUX6"]
            ttl = ['board-DIGITAL-IN-01']
        elif animal == "Ent_CamK2_63":
            port = "C"
            channels = np.arange(8, 24)
            Accelerometers = ["aux-C-AUX1", "aux-C-AUX2", "aux-C-AUX3"]
            ttl = ['board-DIGITAL-IN-01']
        elif animal == "Ent_CamK2_64":
            port = "C"
            channels = np.arange(40, 56)
            Accelerometers = ["aux-C-AUX4", "aux-C-AUX5", "aux-C-AUX6"]
            ttl = ['board-DIGITAL-IN-01']

        data = open_IntanData_dat(port, ttl, channels, filename)

        # Specify implant set-up for each animal
        if animal == 'Ent_CamK2_59' or  animal == 'Ent_CamK2_62' or animal == 'Ent_CamK2_64':
            channel_names = ["EEG R", "EEG L", "DG R", "CA1 R", "DG L", "CA1 L", "CA3 R", "CA3 L", "Sub R", "Sub L",
                             "ENT R ventral", "ENT R dorsal", "ENT L ventral", "ENT L dorsal", "EMG R", "EMG L", "TTL"]
            channel_types = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                             "eeg", "eeg", "emg", "emg", "stim"]
            Sort_index = [12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16]  # Mapping EIB 16 board to Intan channel

        elif animal == 'Ent_CamK2_60':
            channel_names = ["EEG L", "EEG R", "DG R", "CA1 R", "DG L", "CA1 L", "CA3 R", "CA3 L", "Sub R", "Sub L",
                             "ENT R ventral", " ", "ENT L ventral", " ", "EMG R", "EMG L", "TTL"]
            channel_types = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                             "eeg", "eeg", "emg", "emg", "stim"]
            Sort_index = [12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16]  # Mapping EIB 16 board to Intan channel

        elif animal == 'Ent_CamK2_61':
            channel_names = [" ", "EEG R", "DG R", "CA1 R", "DG L", "CA1 L", " ", "CA3 L", "Sub R", "Sub L",
                             "ENT R ventral","ENT R dorsal", "ENT L ventral", "ENT L dorsal", "EMG R", "EMG L", "TTL"]
            channel_types = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                             "eeg", "eeg", "emg", "emg", "stim"]
            Sort_index = [12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16]  # Mapping EIB 16 board to Intan channel


        elif animal == 'Ent_CamK2_63':
            channel_names = [" ", "EEG R", "DG R", "CA1 R", "DG L", "CA1 L", "CA3 R", "CA3 L", "Sub R", "Sub L",
                             "ENT R ventral", "ENT R dorsal", "ENT L ventral", "ENT L dorsal", "EMG R", "EMG L", "TTL"]
            channel_types = ["eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg", "eeg",
                             "eeg", "eeg", "emg", "emg", "stim"]
            Sort_index = [12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16]  # Mapping EIB 16 board to Intan channel


        nb_channel = len(channel_names);


        data = data[Sort_index]
        info = mne.create_info(channel_names, Sampling_freq, channel_types)
        raw = mne.io.RawArray(data, info)

        # event extract events as timestamps from the TTL signal
        events_TTL = []
        length_events = []
        if ttl!=None:
                ttl = data[-1,:]
                rowAv = np.median(ttl)
                row_zero_centered = np.subtract(ttl, rowAv)
                ttl = np.around(row_zero_centered)
                above_threshold = ttl > 0  # 600*Sampling_freq
                data[-1,:] = 0
                data[-1, above_threshold] = 1
                above_threshold = above_threshold.astype(int).flatten()
                events = np.argwhere(np.diff(above_threshold) == 1).flatten()
                end_events = np.argwhere(np.diff(above_threshold) == -1).flatten()
                length = np.subtract(end_events, events)
                length_events.append(length)
                events_TTL.append(events)

        events_TTL = np.array(events_TTL).flatten()
        length_events = np.array(length_events).flatten()

        annot = mne.Annotations(events_TTL/Sampling_freq, length_events/Sampling_freq,[""] * len(events_TTL), orig_time=raw.info['meas_date'])
        raw.set_annotations(annot)


        # ***Bandpass filter for EEG and EMG***
        print(" *** filter ***")
        raw = raw.filter(l_freq=0.1, h_freq=800, picks=np.arange(0,nb_channel), phase="zero")


        # ***zero-center each channel*** (substract the mean)
        data = raw[:,:][0]
        for i in np.arange(0, len(data)):
            rowAv = np.median(data[i])
            row_zero_centered = np.subtract(data[i], rowAv)
            data[i] = row_zero_centered
        raw = mne.io.RawArray(data, info)

        # Calculate spectrogram on baseline before Notch filter
        start = time.time()
        sample_before = data[5,10*Sampling_freq:10*Sampling_freq + 10*60*Sampling_freq]
        win = 20 * Sampling_freq # sliding window, need 2 cycle of the smaller Hz we are interested in (2 cycle / 0.1Hz => 20)
        freq_before, psd_before = signal.welch(sample_before, Sampling_freq, nperseg=win)

        end = time.time()
        print('Time to transform', end - start)

        # ***Notch Filter
        raw = raw.notch_filter(freqs=[50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800], picks=np.arange(0, nb_channel), phase="zero", method="fir")
        data = raw[:, :][0]

        if Show == True:
            # Calculate power spectrum after Notch to see difference after filtering
            sample_after = data[5,10*Sampling_freq:10*Sampling_freq + 10*60*Sampling_freq]
            win = 20 * Sampling_freq
            freq_after, psd_after = signal.welch(sample_after, Sampling_freq, nperseg=win)
            plt.figure(2).suptitle('Power spectrum before/after filtering')
            plt.plot(freq_before, psd_before, color='b', label='before')
            plt.plot(freq_after, psd_after, color='orange', label='after fir filter')
            plt.xlim(0,800)
            plt.yscale('log')
            plt.legend()

        # Save a version of the signal pre-processed as a MNE raw file
        os.chdir(dir+animal+'/Pre-processed_No_rescale_fif')
        raw = mne.io.RawArray(data, info)
        raw.set_annotations(annot)
        raw.save(str(file + "_filtered_No_rescale_raw.fif"), overwrite=True)

        if Show == True:
            # ***Visualisation***
            color = {"eeg": "k", "emg": "b"}
            scale = {"eeg": 300, "emg": 800}
            raw.plot(remove_dc=True, duration=10, n_channels=nb_channel, scalings=scale, color=color, title=str(file + "_filtered_raw.fif"), show=True, block=True, order=np.arange(0,nb_channel), show_options=True, show_first_samp=True)
