#!/bin/bash
USER=microlab
PASS=
VHOST=microlab
TAG=microlab

if [ -z "${PASS}" ]; then
    echo -n "Set PASS in ./rabbitmq_install.sh and set the same password"
    echo " to AMPQ_PASS in microlab/settings.py"
    exit 1
fi

if [ -z "`which lsb_release`" ]; then
    echo "This script only works for Ubuntu/Debian systems."
    echo "To install rabbitMQ, please vitis their instructions"
    echo "at https://www.rabbitmq.com/download.html"
    exit 1
fi


if ! [ -z "`which lsb_release`" ]; then
    if ! [ -f rabbitmq-server_3.7.7-1_all.deb ] && ! [ -z "`which rabbitmq-server`" ]; then
        wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.7/rabbitmq-server_3.7.7-1_all.deb
        sudo dpkg -i rabbitmq-server_3.7.7-1_all.deb
        sudo apt -f install
        rm rabbitmq-server_3.7.7-1_all.deb
    fi
    sudo systemctl start rabbitmq-server
fi

sudo rabbitmqctl add_user ${USER} ${PASS}
sudo rabbitmqctl add_vhost ${VHOST}
sudo rabbitmqctl set_user_tags ${USER} microlab
sudo rabbitmqctl set_permissions -p ${VHOST} ${USER} ".*" ".*" ".*"

