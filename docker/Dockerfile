FROM apache/airflow:latest

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates wget dirmngr gnupg software-properties-common unzip gosu

# Download and set up the Eclipse Adoptium (Temurin) GPG key and repository
RUN wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | tee /usr/share/keyrings/adoptium.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print $2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list

# Install Temurin JDK 11 (the successor to AdoptOpenJDK)
RUN apt-get update && \
    apt-get install -y build-essential pkg-config temurin-11-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME and update PATH
ENV JAVA_HOME=/usr/lib/jvm/temurin-11-jdk
ENV PATH=$JAVA_HOME/bin:$PATH

# Ensure that the Java environment variables are available to all processes, including Airflow
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> /etc/profile.d/java.sh && \
    echo "export PATH=${JAVA_HOME}/bin:${PATH}" >> /etc/profile.d/java.sh

USER airflow

# Copy the requirements.txt file into the container and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Fix a warning with the Azure provider and install Python dependencies
RUN pip uninstall --yes azure-storage && \
    pip install -U azure-storage-blob apache-airflow-providers-microsoft-azure>=1.1.0 flask_admin>=1.5.8 croniter>=0.3 \
    apache-airflow-providers-databricks jaydebeapi apache-airflow-providers-jdbc apache-airflow-providers-snowflake>=2.0.0 apache-airflow-providers-google

# Install Vaultspeed plugin
#COPY vs_fmc_plugin.zip /opt/airflow/plugins/vs_fmc_plugin.zip
#RUN pip install --upgrade /opt/airflow/plugins/vs_fmc_plugin.zip
