# -----------------------------------------------------------------
# With ubuntu:22.04 (Takes more memory ~500MB)
# -----------------------------------------------------------------
#FROM ubuntu:22.04
# RUN apt-get update && apt-get install -y python3 python3-pip
# COPY . /TestCenter4Jenkins/
#Set the Work directory
# WORKDIR /TestCenter4Jenkins/
# Install the system, and app dependencies
# RUN apt-get update && apt-get install -y python3 python3-pip
# RUN pip install -r requirements.txt
#Final configuration
# EXPOSE 8000
# RUN THE FLASK SERVER
# CMD waitress-serve --host 0.0.0.0 --port 8000 app.server:app
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# With python:3.8.13-alpine3.16 (Takes less memory ~75MB)
# -----------------------------------------------------------------
# Start the image with Python image
FROM python:3.8.13-alpine3.16 as python
#
# Copy app source to /TestCenter4Jenkins/
COPY . /TestCenter4Jenkins/
#
# Set the Work directory to /TestCenter4Jenkins/
WORKDIR /TestCenter4Jenkins/
#
# Install Application modules
RUN pip install -r requirements.txt
#
# RUN THE FLASK SERVER
EXPOSE 8000
CMD waitress-serve --listen=*:8000 app.server:app
# -----------------------------------------------------------------
