FROM apache/airflow:2.8.4

# Copy the requirements.txt file into the image
COPY requirements.txt /requirements.txt

# As root, install system packages
USER root
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user before running pip commands
USER airflow

# Upgrade pip and install required Python packages as the airflow user
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt
