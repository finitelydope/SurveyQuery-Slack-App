FROM python:3.11

WORKDIR /Apps

COPY . /Apps

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

CMD [ "python","first_slack_app.py" ]