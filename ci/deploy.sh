#!/bin/bash

tf_instance_path=create_instance

source aws_env.sh

echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
echo $AWS_DEFAULT_REGION

pushd $tf_instance_path
echo "terraform apply main.tf"
popd
