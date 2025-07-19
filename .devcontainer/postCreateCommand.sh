#!/bin/bash
# postCreateCommand.sh

echo "START Install"

# Install libraries that are not in Kaggle Image
pip install pretty_errors==1.2.25
pip install fastmcp==2.10.5

echo "FINISH Install"