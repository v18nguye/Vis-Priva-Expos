import os
import sys
import  configparser
import _init_paths
from ablation_studies.focusing_exposure import gamma_study, gamma_plot


def ablation_study():

    ##get root directory
    root = os.path.dirname(os.path.dirname(os.getcwd()))
    #/home/users/vnguyen/intern20/Vis-Priva-Expos/
    ##read the param config file
    conf = configparser.ConfigParser()
    conf.read(sys.argv[1])
    conf = conf[os.path.basename(__file__)]

    gamma_path = 'privacy/out/abalation/gamma' ## abalation path
    normalize = False
    regm = 'rf' #regression method
    score_type = 'kendall_corr' # or kendall_corr or pear_corr
    gamma_file = 'gamma_rf_kendall_corr_30_load_test_origin_optthresh_filter_2_cluster_pos_neg.json'
    feature_transform = 'pos_neg' # origin, abs, pos_neg
    debug = False
    train_all = True
    only_plot = False
    load_active_detectors = True

    if not only_plot:
        print('##########################################')
        print('######## Focusing Exposure Search ########')
        print('###########################################')
        gamma_list = [0, 1, 2, 3]
        gamma_study(gamma_list, conf, root, gamma_file, normalize, regm, score_type, debug, train_all, feature_transform, load_active_detectors)
        gamma_plot(os.path.join(root, gamma_path), gamma_file)

    else:
        gamma_plot(os.path.join(root, gamma_path), gamma_file)

if __name__ == '__main__':
    ablation_study()