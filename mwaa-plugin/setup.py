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
        "apache-airflow>=2.8.1",
        "apache-airflow-providers-jdbc",
        "apache-airflow-providers-snowflake",
        "apache-airflow-providers-microsoft-azure",
        "apache-airflow-providers-databricks",
        "apache-airflow-providers-google",
        "croniter",
        "azure-storage-blob",
        "flask-admin",
        "flask-appbuilder",
        "flask-babel",
        "jaydebeapi"
    ],
    entry_points={
        "apache_airflow_provider": [
            "provider_info=vs_fmc_plugin.__init__:get_provider_info"
        ]
    },
    python_requires=">=3.7,<4.0"
)