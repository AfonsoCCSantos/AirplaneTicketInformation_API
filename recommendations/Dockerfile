FROM python

RUN mkdir /recommendations
COPY . /recommendations

WORKDIR /recommendations
RUN pip install -r requirements.txt

EXPOSE 8083
ENV FLASK_APP=recommendations.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8083"]