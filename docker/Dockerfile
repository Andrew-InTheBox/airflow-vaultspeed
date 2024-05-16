FROM apache/airflow:latest

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates wget dirmngr gnupg software-properties-common

# Add the Eclipse Adoptium (Temurin) GPG key and repository
RUN wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    add-apt-repository --yes https://packages.adoptium.net/artifactory/deb/

# Install Temurin JDK 11 (the successor to AdoptOpenJDK)
RUN apt-get update && \
    apt-get install -y build-essential pkg-config temurin-11-jdk

# Clean up to keep the Docker image size small
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy the requirements.txt file into the container and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Fix a warning with the Azure provider and install Python dependencies
RUN pip uninstall --yes azure-storage && \
    pip install -U azure-storage-blob apache-airflow-providers-microsoft-azure==1.1.0 flask_admin>=1.5.8 croniter>=0.3 apache-airflow>=1.8.1 \
    apache-airflow-providers-databricks jaydebeapi apache-airflow-providers-jdbc apache-airflow-providers-snowflake==2.0.0 apache-airflow-providers-google

# Install Vaultspeed plugin
COPY vs_fmc_plugin.zip /opt/airflow/plugins/vs_fmc_plugin.zip
RUN pip install --upgrade /opt/airflow/plugins/vs_fmc_plugin.zip
