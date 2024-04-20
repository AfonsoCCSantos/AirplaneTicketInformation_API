FROM python

RUN mkdir /authentication
COPY . /authentication

WORKDIR /authentication
RUN pip install -r requirements.txt

EXPOSE 8085
ENV FLASK_APP=authentication.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8085"]