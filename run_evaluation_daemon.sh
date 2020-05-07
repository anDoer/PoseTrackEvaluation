./build.sh
USERNAME=user
SRC_DIR="$PWD/daemon"

echo ""
if test "$#" -ne 3; then
    echo "Expected three keywords: \$experiment_dir \$gt_dir \$num_gt_files"
    echo ""
    exit 1
fi

EXP_INPUT="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
GT_INPUT="$(cd "$(dirname "$2")"; pwd)/$(basename "$2")"


if [ ! -d "$EXP_INPUT" ]; then
    echo "Input directory '$EXP_INPUT' does not exist! (exit)"
    echo ""
    exit 1
fi

if [ ! -d "$GT_INPUT" ]; then
    echo "Output directory '$GT_INPUT' does not exist! (exit)"
    echo ""
    exit 1
fi

docker run\
    --shm-size="2g"\
    -v "$SRC_DIR":/home/$USERNAME/daemon\
    -v "$EXP_INPUT":"/home/$USERNAME/experiments"\
    -v "$GT_INPUT":"/home/$USERNAME/gt_data"\
    --rm -it\
    andoer/posetrack_eval_daemon \
    python experiment_evaluation_daemon.py --num_validation_sequences=50 \
    --toolkit_path=/opt/poseval/py \
    --experiment_data_path="/home/$USERNAME/experiments" \
    --gt_directory_path="/home/$USERNAME/gt_data"
