


# Use the latest version of the Apache Airflow image as the base
FROM apache/airflow:latest

# Switch to the root user to install software
USER root

# Update package lists, install git, and clean up
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# Switch back to the airflow user
USER airflow
