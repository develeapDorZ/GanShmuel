FROM python:alpine3.14
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . /billing
WORKDIR /billing
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "flask" , "run" ]