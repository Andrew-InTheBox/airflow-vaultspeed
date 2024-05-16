# Airflow Docker Container

This Docker container sets up an Apache Airflow environment with custom dependencies and configurations. It is built using Docker Compose and includes the following components:

- Apache Airflow base image
- Temurin JDK 11 (successor to AdoptOpenJDK)
- Custom Python dependencies specified in `requirements.txt`
- Vaultspeed plugin (`vs_fmc_plugin.zip`)
- Azure, Databricks, JDBC, Snowflake, and Google provider packages

## Prerequisites

- Docker
- Docker Compose

## Usage

1. Clone this repository.
2. Navigate to the directory containing the `docker-compose.yaml` file.
3. Run the following command to build the Docker image:
  docker-compose build
4. Once the build process is complete, you can start the Airflow containers using:
  docker-compose up

The Airflow web interface will be accessible at `http://localhost:8080`.

## Configuration

The `docker-compose.yaml` file contains the configuration for the Airflow environment. You can customize the following:

- Airflow version
- Postgres and Redis settings
- Volumes for DAGs, logs, and plugins
- Additional Python dependencies in `requirements.txt`
- Vaultspeed plugin in `vs_fmc_plugin.zip`

## Directory Structure

- `dags/`: Directory for storing Airflow DAGs
- `docker/`: Contains the Dockerfile and additional files for building the custom Airflow image
 - `Dockerfile`: Dockerfile for building the custom Airflow image
 - `requirements.txt`: File listing the custom Python dependencies
 - `vs_fmc_plugin.zip`: Vaultspeed plugin ZIP file
- `logs/`: Directory for storing Airflow logs
- `plugins/`: Directory for storing Airflow plugins
- `docker-compose.yaml`: Docker Compose configuration file

For more information on using and configuring Airflow, please refer to the [Apache Airflow documentation](https://airflow.apache.org/docs/).