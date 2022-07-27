# syntax=docker/dockerfile:1

FROM python:3.9.5

# build from `app` folder
# WORKDIR /SynologyDrive/dikart/pricing/docker/app/
WORKDIR /app

COPY requirements.txt requirements.txt

# Microsoft SQL Server Prerequisites
RUN apt-get update
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get install -y --no-install-recommends \
        locales \
        apt-transport-https
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen 
#RUN apt-get install libodbc1
#RUN apt-get -y install odbcinst1debian2
#RUN apt-get -y install unixodbc
RUN apt-get update
RUN apt-get -y --no-install-recommends install unixodbc-dev
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get -y --no-install-recommends install msodbcsql17

#RUN python -m pip install -U pip && \
#    pip install -U setuptools SQLAlchemy pandas
#RUN pip install pyodbc

RUN python -m pip install -U pip
RUN pip install -r requirements.txt

COPY ../.. .

#CMD [ "python", "app/casts.py"]
#CMD [ "python", "casts.py"]
EXPOSE 8000
ENTRYPOINT [ ]
CMD ["uvicorn", "pricing_server:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD [ "uvicorn", "pricing_server:app"]
# CMD [ "python", "pricing_server.py" ]         # same,