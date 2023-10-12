# Start the image with ubuntu
FROM ubuntu:22.04

# Install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install -r ./requirements.txt

# Install Application
COPY app /TestCenter4Jenkins/
COPY logs /TestCenter4Jenkins/
COPY crawler*.py /TestCenter4Jenkins/

# Final configuration
ENV FLASK_APP=app
EXPOSE 8000

# RUN THE FLASK SERVER
CMD cd /TestCenter4Jenkins/
CMD waitress-serve --host 127.0.0.1 --port 8000 app.server:app
