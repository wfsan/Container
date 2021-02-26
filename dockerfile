# load python 3.8 dependencies using slim debian 10 image.
FROM python:3.8
# build variables.
ENV DEBIAN_FRONTEND noninteractive
# install Microsoft SQL Server requirements.
ENV ACCEPT_EULA=Y
RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev
# # Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools \
  && echo 'exportPATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'exportPATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# # upgrade pip and install requirements.
COPY /requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# clean the install.
RUN apt-get -y clean
# copy all files to /app directory and move into directory.
COPY . /app
WORKDIR /app
CMD ["python", "./projeto-02-crud.py"]
    

  

