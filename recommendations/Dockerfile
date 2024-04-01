FROM python

RUN mkdir /recommendations
COPY . /recommendations

WORKDIR /recommendations
RUN pip install -r requirements.txt

EXPOSE 8083
ENV FLASK_APP=recommendations.py
ENTRYPOINT [ "flask", "run", "-p", "8083"]