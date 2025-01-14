import requests
import re

def get_mwaa_constraints():
    # Get constraints file for MWAA Airflow 2.8.1
    url = "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.10.txt"
    response = requests.get(url)
    constraints = response.text
    
    # Define the providers we're interested in
    providers = [
        "apache-airflow-providers-jdbc",
        "apache-airflow-providers-snowflake",
        "apache-airflow-providers-microsoft-azure",
        "apache-airflow-providers-databricks",
        "apache-airflow-providers-google",
        "croniter",
        "flask-admin",
        "flask-appbuilder",
        "flask-babel",
        "azure-storage-blob",
        "jaydebeapi"
    ]
    
    # Extract versions
    versions = {}
    for provider in providers:
        match = re.search(f"{provider}==([0-9.]+)", constraints)
        if match:
            versions[provider] = match.group(1)
        else:
            print(f"Warning: {provider} not found in constraints")
    
    return versions

if __name__ == "__main__":
    versions = get_mwaa_constraints()
    print("\nDependency versions from MWAA constraints file:")
    print("=============================================")
    for package, version in versions.items():
        print(f'"{package}=={version}",')