#!/bin/bash

##########################
echo alias k=kubectl >> /home/vscode/.zshrc

aws sso login --profile default
aws eks list-clusters --region=eu-north-1


