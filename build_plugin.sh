#!/bin/bash

# Create temporary build directory
BUILD_DIR="build_plugin"
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

# Copy plugin files to build directory
cp -r plugins/vs_fmc_plugin/* $BUILD_DIR/

# Enter build directory
cd $BUILD_DIR

# Create distribution
python -m pip install --upgrade build
python -m build

# Create zip file from the package
cd ..
zip -r plugins/vs_fmc_plugin.zip vs_fmc_plugin/

# Clean up
rm -rf $BUILD_DIR