FROM python:3.9
COPY tn /root/tn
COPY fastapitn /root/fastapitn
COPY run.sh /root/run.sh
#ENV PYTHONUNBUFFERED=1
#RUN apk add --update --no-cache python:3.7 && ln -sf python /usr/bin/python
#RUN python3 -m ensurepip
#RUN pip3 install --no-cache --upgrade pip setuptools
RUN apt-get update 
RUN apt-get install -y nginx 

COPY fastapi-nginx /etc/nginx/sites-enabled/fastapi-nginx
RUN rm /etc/nginx/sites-enabled/default
RUN pip3 install fastapi uvicorn python-dateutil inflect
EXPOSE 80
EXPOSE 443
CMD /root/run.sh

