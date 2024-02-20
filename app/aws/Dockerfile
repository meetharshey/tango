# Use Amazon Linux as the base image for better compatibility with AWS Lambda
FROM amazonlinux

# Update the package repository and install necessary dependencies
RUN yum update -y && \
    yum install -y \
    gcc \
    openssl-devel \
    zlib-devel \
    libffi-devel \
    wget && \
    yum -y groupinstall development && \
    yum clean all

# Set the working directory
WORKDIR /opt/python

# Install Python 3.8
RUN wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz && \
    tar -xf Python-3.8.12.tar.xz && \
    cd Python-3.8.12 && \
    ./configure --enable-optimizations && \
    make altinstall

# Verify Python 3.8 installation
RUN python3.8 -V

# Install pip for Python 3.8
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.8 get-pip.py && \
    rm get-pip.py

# Verify pip installation
RUN pip3.8 -V

# Set the working directory for Selenium and ChromeDriver
WORKDIR /opt/output/

# Install Selenium and ChromeDriver
RUN pip3.8 install selenium==3.14.0 && \
    wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip

# Download and install Headless Chromium
RUN curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip && \
    unzip headless-chromium.zip && \
    rm *.zip

# Set the working directory for the app
WORKDIR /usr/src/app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip3.8 install -r requirements.txt

# Copy the run.sh script to the container
COPY run.sh /opt/output/run.sh

# Set the entry point to run the run.sh script
ENTRYPOINT /opt/output/run.sh
