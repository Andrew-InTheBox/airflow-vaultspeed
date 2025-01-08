# VaultSpeed Airflow Provider Plugin for MWAA

This package contains the VaultSpeed Airflow provider plugin packaged for installation in Amazon MWAA environments without requiring access to PyPI.

## Package Contents

- VaultSpeed Airflow provider (v5.5.0.4) including all hooks and operators
- Required dependency wheels packaged for offline installation

## Building the Plugin

1. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Install build tools:

    ```bash
    python -m pip install --upgrade pip
    python -m pip install build wheel setuptools
    ```

3. Build the plugin wheel:

    ```bash
    python -m build --wheel
    ```

4. Create the MWAA plugin package:

    ```bash
    mkdir plugin_package
    cd plugin_package
    cp ../dist/airflow_provider_vaultspeed-5.5.0.4-py3-none-any.whl .
    pip wheel -r ../requirements.txt -w .
    zip -r plugins.zip *.whl
    ```

## Installation in MWAA

1. Upload the plugins.zip file to your MWAA environment's S3 bucket:

    ```bash
    aws s3 cp plugins.zip s3://YOUR-MWAA-BUCKET/plugins/plugins.zip
    ```

2. In the MWAA console:

    - Navigate to your environment
    - Edit environment
    - Set "Plugins file" to point to your uploaded plugins.zip
    - Save changes

## Testing Locally

To verify the plugin package before MWAA deployment:

```bash
python -m venv test_env
source test_env/bin/activate
mkdir test_wheels
unzip plugins.zip -d test_wheels
pip install test_wheels/*
```

## Directory Structure

```
mwaa-plugin/
├── README.md
├── pyproject.toml
├── requirements.txt
├── setup.cfg
├── setup.py
└── vs_fmc_plugin/
    ├── __init__.py
    ├── hooks/
    └── operators/
```

## Support

For questions about the VaultSpeed provider functionality, please refer to the [VaultSpeed Documentation](https://docs.vaultspeed.com/space/VPD/3012624432/Airflow).
