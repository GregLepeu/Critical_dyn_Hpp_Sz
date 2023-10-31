import matplotlib.pyplot as plt
from Lepeu_Nat_Com_2023 import Info_Experiment
import GL_module as gl
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV, permutation_test_score
import matplotlib.gridspec as gridspec
from sklearn.metrics import make_scorer, f1_score, roc_auc_score, auc, accuracy_score, balanced_accuracy_score, precision_recall_fscore_support,mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression, LogisticRegressionCV
from mne.decoding import Vectorizer, SlidingEstimator, cross_val_multiscore
import seaborn as sns

path = '/Volumes/LaCie/Acute_Pharmaco_Mod/'
animals = ["Ent_CamK2_09","Ent_CamK2_10","Ent_CamK2_11","Ent_CamK2_15","Ent_CamK2_16","Ent_CamK2_34","Ent_CamK2_40","Ent_CamK2_42"]
conditions_GABA = ['NaCl','Dz 5mg/kg','PTZ 20mg/kg']
passive_metrics = ["Autocorrelation","Variance","Skewness","Sum LL", 'Mean Spatial Correlation']
time_window_ms = 250
Sampling_freq = 2000

def cross_valdidaton_logistic_regression_multi_cnd(animals,hue_order,path,n_cv=5,n_perm=100):
    # "Active probing classifier": single-trial multilabel classifiers based on iEEG response to SP
    acc_per_animal = np.zeros(len(animals))
    chancelevel_per_animal = np.zeros(len(animals))
    p_value_per_animal  = np.zeros(len(animals))
    for idx_animal, animal in enumerate(animals):
        # Load data
        file = animal+'_All_first_pulse_Max Intensity'  # dataframe containing LFP response and labels
        df_data = pd.read_pickle(path  + animal+'/Data_Event_by_session/' + file)

        data = np.array(df_data['LFP'].to_list()) # Dimensions: n_trials x n_channels x n_timepoints
        data = data[:,:,250:]  #Remove baseline before pulse
        labels = np.array(df_data['Condition'].to_list()).flatten()

        #Check for duplicates in data
        seq, count_seq = np.unique(data,return_counts=True,axis=0)
        if any(count_seq>1):
            print('Duplicate in ', animal)
            break

        #### Keep only conditions to classify ####
        data_cnd = data[np.isin(labels,hue_order)]
        labels_cnd = labels[np.isin(labels,hue_order)]
        # Express labels as integers
        for idx, cnd in enumerate(hue_order):
            labels_cnd[labels_cnd == cnd] = idx
        labels_cnd = labels_cnd.astype(int)

        clf_cross_val = make_pipeline(Vectorizer(), StandardScaler(),LogisticRegressionCV(solver='newton-cg', cv=n_cv, random_state=42, penalty='l2'))
        acc, acc_empirical_chance_level, acc_p_value = permutation_test_score(clf_cross_val, data_cnd, labels_cnd, cv=n_cv,scoring=make_scorer(accuracy_score),n_permutations=n_perm, n_jobs=10)
        print(animal, ' : Acc CV: ', acc, 'Empirical chance level: ', str(np.mean(acc_empirical_chance_level)),', p-value: ', acc_p_value)
        acc_per_animal[idx_animal] = acc ; chancelevel_per_animal[idx_animal] = np.mean(acc_empirical_chance_level); p_value_per_animal[idx_animal] = acc_p_value
        acc_per_animal[idx_animal] = acc
    print('Mean score across anmial :', str(np.mean(acc_per_animal)),'Empirical chance level: ', str(np.mean(chancelevel_per_animal)), ', p-value: ', str(np.mean(p_value_per_animal)))


    df = pd.DataFrame({"Animal": animals, 'Accuracy':acc_per_animal, 'chance level': chancelevel_per_animal,
                   'p-value': p_value_per_animal, 'Condition': [gl.list_to_string(hue_order)] * len(acc_per_animal),
                   'Settings': [[n_cv, n_perm]] * len(acc_per_animal)})
    df.to_pickle(path + "/Values/Score_mulitLabel_classifier_SP")


    return acc_per_animal, chancelevel_per_animal, p_value_per_animal
def LFP_feature_cross_valdidaton_logistic_regression_multi_cnd(animals,hue_order,path,passive_metrics,n_cv=5,n_perm=100):
    # "Passive metrics" classifier: single-trial multilabel classifiers based on passive metrics
    score_per_animal = np.zeros(len(animals))
    chancelevel_per_animal = np.zeros(len(animals))
    p_value_per_animal  = np.zeros(len(animals))
    for idx_animal, animal in enumerate(animals):
        # Load data
        file = animal+'_All_LFP_feature'  # dataframe containing LFP response and labels
        list_channel = Info_Experiment.get_list_good_channel(animal,type='LFP')
        df_animal = pd.read_pickle(path  + animal+'/Data_Event_by_session/' + file)
        df_data = df_animal.loc[:,list_channel]
        df_data =df_data.reset_index(drop='yes')

        metrics_in_file = ["Autocorrelation", "Variance", "Skewness", "Sum LL", '1/f Exponent','Mean Spatial Correlation', 'SP']
        mask_metric = np.isin(metrics_in_file, passive_metrics)

        data = np.zeros((len(df_data),len(list_channel), len(np.argwhere(mask_metric==True)))) # Dimensions: n_trials x n_channels x n_features
        i_c = 0
        for name_c,columns in df_data.items():
            for i_r, row in columns.items():
                filtered_row = np.array(row)[mask_metric]
                data[i_r,i_c,:] = filtered_row
            i_c= i_c+1

        labels = np.array(df_animal['Condition'].to_list()).flatten()

        #Check for duplicates in data
        seq, count_seq = np.unique(data,return_counts=True,axis=0)
        if any(count_seq>1):
            print('Duplicate in ', animal)
            break

        # Remove trials with nan vlaue in it
        data_with_nan = np.isnan(data).any(axis=2).any(axis=1)
        index_to_keep = np.nonzero(data_with_nan==False)[0]
        data = data[index_to_keep]
        labels = labels[index_to_keep]

        #### Keep only conditions to classify ####
        data_cnd = data[np.isin(labels,hue_order)]
        labels_cnd = labels[np.isin(labels,hue_order)]
        # Express labels as integers
        for idx, cnd in enumerate(hue_order):
            labels_cnd[labels_cnd == cnd] = idx
        labels_cnd = labels_cnd.astype(int)

        clf_cross_val = make_pipeline(Vectorizer(), StandardScaler(),LogisticRegressionCV(solver='newton-cg', cv=n_cv, random_state=42, penalty='l2'))
        score, empirical_chance_level, p_value = permutation_test_score(clf_cross_val, data_cnd, labels_cnd, cv=n_cv,scoring=make_scorer(accuracy_score), n_permutations=n_perm,n_jobs=10)
        print(animal,' : Score CV: ', score, 'Empirical chance level: ', str(np.mean(empirical_chance_level)), ', p-value: ', p_value)
        score_per_animal[idx_animal] = score ; chancelevel_per_animal[idx_animal] = np.mean(empirical_chance_level); p_value_per_animal[idx_animal] = p_value

    print('Mean score across anmial :', str(np.mean(score_per_animal)),'Empirical chance level: ', str(np.mean(chancelevel_per_animal)), ', p-value: ', str(np.mean(p_value_per_animal)))
    df = pd.DataFrame({"Animal":animals,"Accuracy": score_per_animal, 'chance level': chancelevel_per_animal, 'p-value': p_value_per_animal, 'Condition':[gl.list_to_string(hue_order)] * len(score_per_animal), 'Settings':[[n_cv,n_perm]] * len(score_per_animal)})
    df.to_pickle(path + "/Values/Score_mulitLabel_classifier_LFP_feature")

    return score_per_animal, chancelevel_per_animal, p_value_per_animal
def cross_valdidaton_logistic_regression_multi_cnd_combined(animals,hue_order,path,n_cv=5,n_perm=100):
    # "Combined" classifier: single-trial multilabel classifiers based on iEEG response to SP + passive metrics
    score_per_animal = np.zeros(len(animals))
    chancelevel_per_animal = np.zeros(len(animals))
    p_value_per_animal  = np.zeros(len(animals))
    for idx_animal, animal in enumerate(animals):
        # Load SP data
        file = animal+'_All_first_pulse_Max Intensity'  # dataframe containing LFP response and labels
        df_SP_data = pd.read_pickle(path  + animal+'/Data_Event_by_session/' + file)

        SP_data = np.array(df_SP_data['LFP'].to_list()) # Dimensions: n_trials x n_channels x n_timepoints
        SP_data = SP_data[:,:,250:]  #Remove baseline before pulse
        labels = np.array(df_SP_data['Condition'].to_list()).flatten()

        # Load data
        file = animal + '_All_LFP_feature'  # dataframe containing passive metrics for each LFP bout
        list_channel = np.load(path + animal + '/Data_Event_by_session/' + animal + '_channels.npy').tolist()
        df_animal_LFP = pd.read_pickle(path + animal + '/Data_Event_by_session/' + file)
        df_LFP_data = df_animal_LFP.loc[:, list_channel]
        df_LFP_data = df_LFP_data.reset_index(drop='yes')

        LFP_data = np.zeros((len(df_LFP_data), len(list_channel), len(df_LFP_data.iat[0, 0])))  # Dimensions: n_trials x n_channels x n_features
        shape = LFP_data.shape
        SP_data_trimed = SP_data[:shape[0],:shape[1],:]
        data = np.concatenate((SP_data_trimed,LFP_data),axis=2)
        labels = labels[:shape[0]]

        #Check for duplicates in data
        seq, count_seq = np.unique(data,return_counts=True,axis=0)
        if any(count_seq>1):
            print('Duplicate in ', animal)
            break

        #### Keep only conditions to classify ####
        data_cnd = data[np.isin(labels,hue_order)]
        labels_cnd = labels[np.isin(labels,hue_order)]
        # Express labels as integers
        for idx, cnd in enumerate(hue_order):
            labels_cnd[labels_cnd == cnd] = idx
        labels_cnd = labels_cnd.astype(int)

        clf_cross_val = make_pipeline(Vectorizer(), StandardScaler(),LogisticRegressionCV(solver='newton-cg', cv=n_cv, random_state=42, penalty='l2'))
        score, empirical_chance_level, p_value = permutation_test_score(clf_cross_val, data_cnd, labels_cnd, cv=n_cv,scoring=make_scorer(accuracy_score), n_permutations=n_perm,n_jobs=10)
        print(animal,' : Score CV: ', score, 'Empirical chance level: ', str(np.mean(empirical_chance_level)), ', p-value: ', p_value)
        score_per_animal[idx_animal] = score ; chancelevel_per_animal[idx_animal] = np.mean(empirical_chance_level); p_value_per_animal[idx_animal] = p_value

    print('Mean score across anmial :', str(np.mean(score_per_animal)),'Empirical chance level: ', str(np.mean(chancelevel_per_animal)), ', p-value: ', str(np.mean(p_value_per_animal)))


    df = pd.DataFrame({"Animal": animals, "Accuracy": score_per_animal, 'chance level': chancelevel_per_animal,
                   'p-value': p_value_per_animal, 'Condition': [gl.list_to_string(hue_order)] * len(score_per_animal),
                   'Settings': [[n_cv, n_perm]] * len(score_per_animal)})
    df.to_pickle(path + "/Values/Score_mulitLabel_classifier_combined")


    return score_per_animal, chancelevel_per_animal, p_value_per_animal
def slidinng_cross_valdidaton_log_reg_multilabel(animals,hue_order,Sampling_freq,time_window,path,n_cv=5,n_perm=100):
    # Multilabel classifiers based on iEEG response to SP, but as a sliding window with different classifier at each time points
    timepoints = int(1.5 * time_window * Sampling_freq/1000)
    score_tp_per_animal = np.zeros((len(animals),timepoints))
    chancelevel_tp_per_animal = np.zeros((len(animals),timepoints))
    p_value_tp_per_animal  = np.zeros((len(animals),timepoints))

    for idx_animal, animal in enumerate(animals):
        # Load data
        file = animal+'_All_first_pulse_Max Intensity'  # dataframe containing LFP response and labels
        list_channel = np.load(path + animal+'/Data_Event_by_session/' + animal+'_channels.npy').tolist()

        df_data = pd.read_pickle(path + animal+'/Data_Event_by_session/' + file)

        data = np.array(df_data['LFP'].to_list())  # Dimensions: n_trials x n_channels x n_timepoints
        labels = np.array(df_data['Condition'].to_list()).flatten()


        # Check for duplicates in data
        seq, count_seq = np.unique(data, return_counts=True, axis=0)
        if any(count_seq > 1):
            print('Duplicate in ', animal)
            break

        #### Keep only conditions to classify ####
        data_cnd = data[np.isin(labels,hue_order)]
        labels_cnd = labels[np.isin(labels,hue_order)]

        # Express labels as integers
        for idx, cnd in enumerate(hue_order):
            labels_cnd[labels_cnd == cnd] = idx
        labels_cnd = labels_cnd.astype(int)

        # Classifier
        clf_tp = make_pipeline(Vectorizer(), StandardScaler(),LogisticRegressionCV(solver='newton-cg', cv=n_cv, random_state=42, penalty='l2'))

        # Sliding estimator
        sl = SlidingEstimator(clf_tp, scoring=make_scorer(accuracy_score)) # we apply the sliding estimator to 'clf'
        scores_all_folds = cross_val_multiscore(sl, data_cnd, labels_cnd, cv=n_cv, n_jobs=12)
        print(scores_all_folds.shape)

        # Mean the score for each timepoints across the cross vlaidation iterations
        score_cv = np.mean(scores_all_folds, axis=0)
        score_tp_per_animal[idx_animal] = score_cv

        # Calculate empricial chance level by permutating the test labels
        score_perm = np.zeros((n_perm, data.shape[-1]))
        for i in range(n_perm):
            perm_labels_train = np.copy(labels_cnd)
            np.random.shuffle(perm_labels_train)

            sl_perm = SlidingEstimator(clf_tp, scoring=make_scorer(accuracy_score))
            scores_all_data = cross_val_multiscore(sl_perm, data_cnd, perm_labels_train, cv=n_cv, n_jobs=12)
            scores_mean = np.mean(scores_all_data, axis=0)
            score_perm[i] = scores_mean

        emprical_chance = np.mean(score_perm, axis=0)
        chancelevel_tp_per_animal[idx_animal] = emprical_chance

        print(score_perm.shape)

        p_value_tp = np.zeros((len(score_cv)))
        for tp in range(len(score_cv)):
            C = len(np.where(score_perm[:, tp] >= score_cv[tp])[0])
            p_value_tp[tp] = (C + 1) / (score_perm.shape[0] + 1)

        p_value_tp_per_animal[idx_animal] = p_value_tp

    df = pd.DataFrame({"Animal": animals, "f1-score": score_tp_per_animal.tolist(), 'chance level': chancelevel_tp_per_animal.tolist(),'p-value': p_value_tp_per_animal.tolist(),'Condition': [gl.list_to_string(hue_order)] * len(animals),'Settings': [[n_cv, n_perm]] * len(animals)})
    df.to_pickle(path + "/Values/Score_mulitLabel_classifier_SP_sliding")
    return score_tp_per_animal, chancelevel_tp_per_animal, p_value_tp_per_animal


# Run the three classifiers
score_per_animal, chancelevel_per_animal, p_value_per_animal = cross_valdidaton_logistic_regression_multi_cnd(animals,conditions_GABA,path, n_cv=5,n_perm=100)

passive_score_per_animal, _, _ = LFP_feature_cross_valdidaton_logistic_regression_multi_cnd(animals,conditions_GABA,path,passive_metrics, n_cv=5,n_perm=100)

combined_score_per_animal, _, _ = cross_valdidaton_logistic_regression_multi_cnd_combined(animals,conditions_GABA,path, n_cv=5,n_perm=100)

sL_score_per_animal, sl_chancelevel_per_animal, sl_p_value_per_animal = slidinng_cross_valdidaton_log_reg_multilabel(animals,conditions_GABA, Sampling_freq, time_window_ms,path,n_cv=5,n_perm=100)

def plot_score_sliding_window(time_window_ms,Sampling_freq,sL_score_per_animal,sl_chancelevel_per_animal,sl_p_value_per_animal):
    # Mean score across animals
    score_cv = np.mean(sL_score_per_animal, axis=0)
    emprical_chance = np.mean(sl_chancelevel_per_animal, axis=0)
    p_value_tp = np.mean(sl_p_value_per_animal, axis=0)

    # Plot Accuracy scores across timepoints (Figure 6G)
    title =  'Mutilabel classifier score sliding window '+str(time_window_ms)+'ms'
    fig = plt.figure(title, figsize=(10, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    x = np.arange(-time_window_ms / 2, time_window_ms, 1000 / Sampling_freq)
    index_p = np.where(p_value_tp < 0.05)[0]
    signif = np.empty((len(Sampling_freq)))
    signif[:] = np.NaN
    signif[index_p] = 0.2 # Set height significant line

    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    ax1.plot(x, score_cv, label='score cross validation')
    ax1.plot(x, emprical_chance, label='empirical chance level', color='g')
    ax1.plot(x, signif, label='p<0.05')
    ax1.set_ylabel('Accuracy')
    ax1.set_xlabel('[ms]')
    ax1.set_ylim(0,1)
    ax1.legend()
def BoxPlot_score_multi_cnd_across_classifier(animals_to_plot,path):
    # Compare classifer among them (Figure 6H)
    df_SP = pd.read_pickle(path+ "/Values/Score_mulitLabel_classifier_SP")
    df_passive_metric = pd.read_pickle(path+ "/Values/Score_mulitLabel_classifier_LFP_feature")
    df_combined = pd.read_pickle(path + "/Values/Score_mulitLabel_classifier_combined")

    df_SP_chance_level = pd.DataFrame({'Animal':df_SP['Animal'],"Accuracy":df_SP['chance level'],'Classifier':'Emprical Chance Level'})

    df_SP['Classifier'] = 'SP Classifier'
    df_passive_metric['Classifier'] = 'Passive metrics classifier'
    df_combined['Classifier'] = 'Combined'

    plot_df = pd.concat([df_SP_chance_level,df_SP,df_passive_metric,df_combined])

    # Plot only a subset of the animals
    mask = np.isin(plot_df['Animal'], animals_to_plot)
    plot_df = plot_df.loc[mask,:]

    animals = plot_df['Animal'].unique()
    title = gl.list_to_string(animals) + ' f1 score multilabel ' + 'LFP feature'
    fig = plt.figure(title, figsize=(10, 8)).suptitle(title)
    gridspec.GridSpec(12, 12)
    ax1 = plt.subplot2grid((12, 12), (0, 0), rowspan=12, colspan=12)
    sns.boxplot(ax=ax1,data=plot_df, x="Classifier", y="Accuracy", orient='v',color='white', width=.5)
    sns.swarmplot(ax=ax1,data=plot_df, x="Classifier", y="Accuracy")
    ax1.set_ylim(bottom=0, top=1)
    ax1.set_ylabel('Accuracy')

# Plot results
BoxPlot_score_multi_cnd_across_classifier(animals,path)

plot_score_sliding_window(time_window_ms,Sampling_freq,sL_score_per_animal,sl_chancelevel_per_animal,sl_p_value_per_animal)
