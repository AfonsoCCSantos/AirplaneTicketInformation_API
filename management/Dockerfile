FROM python

RUN mkdir /management
COPY . /management

WORKDIR /management
RUN pip install -r requirements.txt

EXPOSE 8081
ENV FLASK_APP=management.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8081"]