from setuptools import setup, find_packages

setup(
    name="airflow-provider-vaultspeed",
    version="5.5.0.4",
    description="A VaultSpeed provider for Apache Airflow",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="VaultSpeed",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "vs_fmc_plugin": ["hooks/*.py", "operators/*.py"],
    },
    install_requires=[
        "apache-airflow>=2.0.0",
        "croniter>=0.3",
        "flask_admin>=1.5.8",
        "flask_appbuilder",
        "flask_babel",
        "apache-airflow-providers-microsoft-azure>=1.1.0",
        "azure-storage-blob",
        "apache-airflow-providers-databricks",
        "jaydebeapi",
        "apache-airflow-providers-jdbc",
        "apache-airflow-providers-snowflake>=2.0.0",
        "apache-airflow-providers-google"
    ],
    entry_points={
        "apache_airflow_provider": [
            "provider_info=vs_fmc_plugin.__init__:get_provider_info"
        ]
    },
    python_requires=">=3.7"
)