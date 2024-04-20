FROM python

RUN mkdir /recommendations
COPY . /recommendations

WORKDIR /recommendations
RUN pip install -r requirements.txt

EXPOSE 8083
ENV FLASK_APP=recommendations.py
ENV APP_SECRET_KEY=699b3d871c8e5daa1cd5a2bf6e2b9bf436a05b469bc61885a6a9c5026b71047c
ENV AUTH0_DOMAIN=tomasbarreto.eu.auth0.com
ENV AUTH0_CLIENT_ID=IEvRaY6CXjAAT4UElgICkfN12DydX71a
ENV AUTH0_CLIENT_SECRET=CpYur9-495GPTSc-rxT-NPoDm1rZ7uASFrdlWwDiTkcAyFns2utviMIh7Kq1BgAA
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8083"]