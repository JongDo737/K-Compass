FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

# Make port 80 available to the world outside this container
EXPOSE 6000


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
