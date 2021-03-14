"""
The module verifies best trained models for situations within detectors

     python best_models.py --path /home/nguyen/Documents/intern20/models_FEo_pooling_VISPEL
     python best_models.py --path /home/nguyen/Documents/intern20/models_POOLINGx2_VISPEL
     python best_models.py --path /home/nguyen/Documents/intern20/models_POOLING_VISPEL
     python best_models.py --path /home/nguyen/Documents/intern20/models_OBJECT_VISPEL
     python best_models.py --path /home/nguyen/Documents/intern20/models_ORG
     python best_models.py --path /home/nguyen/Documents/intern20/models_OBJECT_VISPEL_31_10

     python best_models.py --path /home/nguyen/Documents/intern20/models_ORG_N_100

"""

import os
import pickle
import argparse
from pathlib import Path
import _init_paths
import warnings
warnings.filterwarnings("ignore")


def argument_parser():
    """
    Create a parser with some common arguments.

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="path to trained models")

    return parser


def main():
    """

    Returns
    -------
    """
    args = argument_parser().parse_args()
    # list of situations within corresponding detector
    sdetecs = os.listdir(args.path)
    mobis = []
    rcnns = []
    # directory to save the best configuration
    cfg_dir = os.path.join(Path(args.path).parent, "Bcfg_"+args.path.split("/")[-1].split("models_")[-1])

    if not os.path.isdir(cfg_dir):
        os.mkdir(cfg_dir)

    for sdetec in sdetecs:
        # list of trained models
        spath = os.path.join(args.path, sdetec)
        models = os.listdir(spath)
        best_result = -1
        best_cfg = None

        for model in models:
            mpath = os.path.join(spath, model)
            # loaded model
            lmodel = pickle.load(open(mpath, 'rb'))
            lmodel.set_seeds()
            lmodel.test_vispel(half_vis=True)
            test_result = lmodel.test_result

            if test_result > best_result:
                best_result = test_result
                best_cfg = lmodel.cfg

        print('#-----------------------#')
        print(sdetec)
        print(best_result)

        with open(os.path.join(cfg_dir, sdetec+".pkl"), 'wb') as handle:
            pickle.dump(best_cfg, handle, protocol=pickle.HIGHEST_PROTOCOL)

        if 'rcnn' in sdetec:
            rcnns.append(best_result)

        if 'mobi' in sdetec:
            mobis.append(best_result)

    print('RCNN avg: ',sum(rcnns)/len(rcnns))
    print('MOBI avg: ',sum(mobis)/len(mobis))


if __name__ == '__main__':
    main()