#!/usr/bin/python3

import os
import sys
import argparse
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import stats.stats as stats
import utils.utils as utils


def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="", epilog="""
      Documentation at https://github.com/SIMEXP/fmriprep-reproducibility
      """)

    parser.add_argument(
        "-i", "--input_dir", required=False, default=".", help="Input data directory (default: install directory)",
    )

    parser.add_argument(
        "--exp-anat-func", action="store_true", required=False, help="Experiment with independent anatomical and functionnal workflow",
    )

    parser.add_argument(
        "--exp-multithread", action="store_true", required=False, help="Experiment with multithreading",
    )

    parser.add_argument(
        "--exp-multiprocess", action="store_true", required=False, help="Experiment with multiprocessing",
    )

    parser.add_argument(
        "--sampling", required=False, default="ieee", help="Sampling method between \"ieee\" or \"fuzzy\" (default: \"ieee\")",
    )

    parser.add_argument(
        "--template", required=False, default="MNI152NLin2009cAsym", help="fMRIprep template (default: \"MNI152NLin2009cAsym\")",
    )

    parser.add_argument(
        "--version", action="version", version=utils.get_version()
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_parser()
    print("\n### Running make-reports\n")
    print(vars(args))
    # input path, where fmriprep experiments lives
    if args.input_dir == ".":
        input_path = os.path.join(os.path.dirname(__file__),
                                  "..", "..", "outputs", args.sampling)
    else:
        input_path = os.path.join(args.input_dir, "outputs", args.sampling)
    # create dataset, participant id and task dict
    dataset_sub_task_dict = {}
    for folder in sorted(os.listdir(input_path)):
        folder_path = os.path.join(input_path, folder)
        if os.path.isdir(folder_path):
            match_dataset_method = re.match("fmriprep_(.*)_1(.*)", folder)
            if match_dataset_method:
                if args.exp_multithread:
                    if not "multithreaded" in folder:
                        continue
                elif args.exp_multiprocess:
                    if not "multiprocessed" in folder:
                        continue
                elif args.exp_anat_func:
                    if not (("anat" in folder) | ("func" in folder)):
                        continue
                else:
                    if ("anat" in folder) | ("func" in folder) | ("multiprocessed" in folder) | ("multithreaded" in folder):
                        continue
                # get sub and task list
                list_tasks = utils.get_preproc_tasks(
                    dirpath=folder_path, template=args.template)
                list_tasks = list(set(list_tasks))
                list_subs = utils.get_preproc_sub(
                    dirpath=folder_path, template=args.template)
                list_subs = list(set(list_subs))
                dataset_name = match_dataset_method[1]
                dataset_sub_task_dict[dataset_name] = {
                    "subs": sorted(list_subs), "tasks": sorted(list_tasks)}
    print(dataset_sub_task_dict)
    for dataset in dataset_sub_task_dict.keys():
        for sub in dataset_sub_task_dict[dataset]['subs']:
            stats.compute_anat_statistics(
                fmriprep_output_dir=input_path
                , dataset=dataset
                , participant=sub
                , exp_anat_func=args.exp_anat_func
                , exp_multithread=args.exp_multithread
                , exp_multiprocess=args.exp_multiprocess
                , sampling=args.sampling
                , output_template=args.template)
            for task in dataset_sub_task_dict[dataset]['tasks']:
                stats.compute_task_statistics(
                    fmriprep_output_dir=input_path
                    , dataset=dataset
                    , participant=sub
                    , task=task
                    , exp_anat_func=args.exp_anat_func
                    , exp_multithread=args.exp_multithread
                    , exp_multiprocess=args.exp_multiprocess
                    , sampling=args.sampling
                    , output_template=args.template)