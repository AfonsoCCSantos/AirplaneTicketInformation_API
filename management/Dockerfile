FROM python

RUN mkdir /management
COPY . /management

WORKDIR /management
RUN pip install -r requirements.txt

EXPOSE 8081
ENV FLASK_APP=management.py
ENTRYPOINT [ "flask", "run", "-p", "8081"]