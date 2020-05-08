"""
 * experiment_evaluation_daemon
 * Created on 08.08.19
 * Author: doering
"""

import time
import os
import subprocess
import argparse
import random


def perform_evaluation(toolkit_path, gt_directory, prediction_directory, pose_only):

    result_str = subprocess.check_output(['./run_tracking_benchmark_dummy.sh',
                                          'Empty',
                                          toolkit_path,
                                          gt_directory,
                                          prediction_directory,
                                          'evalPoseEstimation'])

    results = result_str.decode('utf8').splitlines()
    pose_results = results[-2:]
    print('\t\tPose [x]')
    if not pose_only:
        result_str = subprocess.check_output(['./run_tracking_benchmark_dummy.sh',
                                              'Empty',
                                              toolkit_path,
                                              gt_directory,
                                              prediction_directory,
                                              'evalPoseTracking'])

        results = result_str.decode('utf8').splitlines()
        tracking_results = results[-7:]
        print('\t\tTracking [x]')
        return pose_results, tracking_results
    else:
        return pose_results, None


def get_files(experiment_data_path, evaluated_folders):
    files = os.listdir(experiment_data_path)
    files = [os.path.join(experiment_data_path, file) for file in files]

    folders = [file for file in files if os.path.isdir(file) and file not in evaluated_folders
               and not file.split('/')[-1] in ['sequences', 'pre_sequences']]

    random.shuffle(folders)

    sub_folders = []
    for folder in folders:
        if folder in ['sequences', 'pre_sequences']:
            continue
        else:
            est_sub_folders = get_files(folder, evaluated_folders)
            sub_folders += est_sub_folders

    folders += sub_folders

    return folders


def walk(folders, evaluated_folders, args):
    new_results = False

    for folder in folders:

        subfolders = [file for file in os.listdir(folder) if os.path.isdir(os.path.join(folder, file))]
        random.shuffle(subfolders)
        if 'sequences' in subfolders:
            print("\tEvaluating {}...".format(folder))
            seq_files = os.listdir(os.path.join(folder, 'sequences'))
            num_files = len(seq_files)

            if num_files == args.num_validation_sequences:
                if os.path.exists(os.path.join(folder, 'result_file.txt')):
                    print('\t\t[Skip]result_file.txt already available.')
                    continue

                # great, we can do the evaluation here
                pose_results, tracking_results = perform_evaluation(
                                                                    args.toolkit_path,
                                                                    args.gt_directory_path,
                                                                    os.path.join(folder, 'sequences/'),
                                                                    args.eval_pose_only)

                with open(os.path.join(folder, 'result_file.txt'), 'w') as f:
                    f.write("POSE ESTIMATION\n")
                    for item in pose_results:
                        f.write("%s\n" % item)

                    if not args.eval_pose_only:
                        f.write("POSE TRACKING\n")
                        for item in tracking_results:
                            f.write("%s\n" % item)

                evaluated_folders.append(folder)
                new_results = True

        elif 'pre_sequences' in subfolders:
           pass

    return new_results


def build_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_data_path', type=str)

    parser.add_argument('--gt_directory_path', type=str)

    parser.add_argument('--toolkit_path', type=str)

    parser.add_argument('--num_validation_sequences', type=int, required=True)

    parser.add_argument('--eval_pose_only', action='store_true')

    return parser.parse_args()


def main():
    args = build_parameters()

    evaluated_folders = []

    while True:
        print("[Check] for new folders...")
        if os.path.exists(args.experiment_data_path):
            folders = get_files(args.experiment_data_path, evaluated_folders)
            has_new_results = walk(folders, evaluated_folders, args)
            print("[Done]")
            if not has_new_results:
                print("[Sleep] for 5 minutes")
                time.sleep(300)
        else:
            print("[Info] Folder not found...")
            print("[Sleep] for 5 minutes")
            time.sleep(300)

if __name__ == '__main__':
    main()
