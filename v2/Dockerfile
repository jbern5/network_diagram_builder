FROM python:3.6

# Create app directory
WORKDIR /app

ADD ./ files/

# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

EXPOSE 8080
CMD [ "python3", "main.py" ]