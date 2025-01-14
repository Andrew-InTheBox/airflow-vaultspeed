
# VaultSpeed Airflow Provider Plugin for MWAA

This package contains the VaultSpeed Airflow provider plugin packaged for installation in Amazon MWAA environments without requiring access to PyPI.

## Package Contents

- VaultSpeed Airflow provider (v5.5.0.4) including all hooks and operators
- Required dependency wheels packaged for offline installation
- Supports Airflow 2.0.0 and above

## Prerequisites

- Python 3.7 or higher
- `pip`
- `build`
- `wheel`
- `setuptools`

## Package Structure

```
mwaa-plugin/
├── README.md
├── pyproject.toml            # Build system requirements
├── setup.py                  # Package configuration and dependencies
├── requirements.txt          # Additional dependencies for MWAA
├── MANIFEST.in               # File inclusion rules for the package
└── vs_fmc_plugin/            # Main package directory
    ├── __init__.py
    ├── hooks/                # Hook implementations
    │   ├── __init__.py
    │   └── *.py
    └── operators/            # Operator implementations
        ├── __init__.py
        └── *.py
```

## Building the Plugin

1. **Create and activate a Python virtual environment**:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2. **Install build tools**:

    ```bash
    python -m pip install --upgrade pip
    python -m pip install build wheel setuptools
    ```

3. **Verify your source files**:
   - Ensure all required hook and operator files are in their respective directories.
   - Check that all `__init__.py` files are present.
   - Verify package metadata in `setup.py`.
   - Confirm file inclusion patterns in `MANIFEST.in`.

4. **Build the plugin wheel**:

    ```bash
    python -m build --wheel
    ```

5. **Create the MWAA plugin package**:

    ```bash
    mkdir -p plugin_package
    cd plugin_package
    cp ../dist/airflow-provider-vaultspeed-5.5.0.4-py3-none-any.whl .
    pip wheel -r ../requirements.txt -w .
    zip -r plugins.zip *.whl
    ```

## Installation in MWAA

1. **Upload the plugins.zip file to your MWAA environment's S3 bucket**:

    ```bash
    aws s3 cp plugins.zip s3://YOUR-MWAA-BUCKET/plugins/plugins.zip
    ```

2. **In the MWAA console**:
   - Navigate to your environment.
   - Select **Edit**.
   - Under **DAG code configuration**, update the **Plugins file** field to point to your uploaded `plugins.zip`.
   - Save changes and wait for the environment update to complete.

## Verifying the Installation

### Local Verification

To verify the plugin package before MWAA deployment:

```bash
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate
mkdir test_wheels
unzip plugins.zip -d test_wheels
pip install test_wheels/*

# Verify imports
python -c "from vs_fmc_plugin.hooks import jdbc_hook; from vs_fmc_plugin.operators import jdbc_operator"
```

### MWAA Verification

After deployment to MWAA:

1. Access the Airflow UI.
2. Navigate to **Admin → Providers**.
3. Look for "VaultSpeed" in the providers list.
4. Verify that all hooks and operators are listed under the provider.

## Notes

- This package uses wheel-based installation, which is the recommended approach for MWAA plugins.
- All hooks and operators are packaged within the wheel file and don't need to be separately included in `plugins.zip`.
- The `plugins.zip` file will contain only wheel (`.whl`) files.
- Python dependencies are automatically handled through the wheel installation process.

## Troubleshooting

If you encounter issues:

- Verify wheel contents:

    ```bash
    unzip -l dist/airflow-provider-vaultspeed-5.5.0.4-py3-none-any.whl
    ```

- Check MWAA logs for any import or dependency errors.
- Ensure all required dependencies are listed in both `setup.py` and `requirements.txt`.

## Support

For questions about:

- **VaultSpeed provider functionality**: Refer to the [VaultSpeed Documentation](https://docs.vaultspeed.com/space/VPD/3012624432/Airflow)
- **MWAA plugin issues**: Check AWS MWAA documentation or contact AWS Support
