#!/bin/bash

##########################
echo alias k=kubectl >> /home/vscode/.zshrc

chmod +x ./aws-profile.sh
./aws-profile.sh

aws sso login --profile default
aws eks list-clusters
