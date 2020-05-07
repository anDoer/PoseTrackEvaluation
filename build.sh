# #!/usr/bin/env bash
USERNAME=user
CURR_DIR=$(pwd)

cd "$CURR_DIR/evaluation_daemon"

cp Dockerfile Dockerfile.bkp

echo "RUN adduser --disabled-password --gecos \"\" -u $UID $USERNAME"  >> Dockerfile
echo "USER $USERNAME" >> Dockerfile
echo "WORKDIR /home/$USERNAME/daemon" >> Dockerfile

docker build --tag='andoer/posetrack_eval_daemon' .

rm Dockerfile
mv Dockerfile.bkp Dockerfile

cd $CURR_DIR
