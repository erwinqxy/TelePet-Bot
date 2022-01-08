FROM python:3.8.10

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

#RUN mkdir /app
#ADD . /app
#WORKDIR /app

RUN pip install -r requirements.txt

#CMD python telepet_bot.py
CMD ["python", "./telepet_bot.py"]