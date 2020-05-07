# PoseTrackEvaluation
Provides a docker container for a posetrack evaluation daemon.

## Required Structure:
The Pose (Tracking) results for each sequence are required to be stored in a folder _sequences_ like:
* Experiments
  * Exp_1
    * sequences
      * *.json
    * results.txt (will be generated)
  * Exp_2
    * sequences
      * *.json
    * results.txt (will be generated)

The Evaluation Daemon will search for such folders and runs the official posetrack evaluation toolbox on each folder.

A file with all results is saved as shown above.

## Usage 

> bash run_evaluation_daemon.sh $EXPERIMENT_PATH $POSETRACK_GT_PATH $NUM_SEQUENCES 

where 
> $POSETRACK_GT_PATH = '$POSETRACK_DIR/posetrack_data/annotations/val'
for the validation set.
