#!/bin/bash

# Exit on any error
set -e

echo "1. Cleaning up any existing build artifacts..."
rm -rf build/ dist/ *.egg-info/ plugin_package/ .venv/

echo "2. Creating and activating new virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "3. Upgrading pip and installing build tools..."
python -m pip install --upgrade pip
python -m pip install build wheel setuptools

echo "4. Building the wheel..."
python -m build --wheel

echo "5. Creating plugin package and collecting dependencies..."
mkdir -p plugin_package
cp dist/airflow_provider_vaultspeed-5.5.0.4-py3-none-any.whl plugin_package/
cd plugin_package
pip wheel -r ../requirements.txt -w .

echo "6. Creating plugins.zip..."
zip -r plugins.zip *.whl

echo "7. Moving plugins.zip to parent directory..."
mv plugins.zip ../

echo "8. Cleaning up..."
cd ..
rm -rf plugin_package/

echo "9. Deactivating virtual environment..."
deactivate

echo "Done! Your plugins.zip file is ready in the mwaa-plugin directory"
echo "You can verify the contents with: unzip -l plugins.zip"