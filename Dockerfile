# Start the image with Python image
#FROM ubuntu:22.04
FROM python:3-alpine

# Install app
# RUN apt-get update && apt-get install -y python3 python3-pip
# COPY requirements.txt /TestCenter4Jenkins/
COPY . /TestCenter4Jenkins/

# Set the Work directory
WORKDIR /TestCenter4Jenkins/

# Install Application modules
#COPY app /TestCenter4Jenkins/
#COPY logs /TestCenter4Jenkins/
#COPY crawler*.py /TestCenter4Jenkins/
#RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install -r requirements.txt

# Final configuration
EXPOSE 8000

# RUN THE FLASK SERVER
CMD waitress-serve --host 0.0.0.0 --port 8000 app.server:app
