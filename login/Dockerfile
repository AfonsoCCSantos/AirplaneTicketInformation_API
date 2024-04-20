FROM python

RUN mkdir /login
COPY . /login

WORKDIR /login
RUN pip install -r requirements.txt

EXPOSE 8085
ENV FLASK_APP=login.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8085"]