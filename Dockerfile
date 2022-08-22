FROM python:3.9
COPY tn /root/tn
COPY fastapitn /root/fastapitn
COPY run.sh /root/run.sh
RUN apt-get update 
RUN apt-get install -y nginx 

COPY fastapi-nginx /etc/nginx/sites-enabled/fastapi-nginx
RUN rm /etc/nginx/sites-enabled/default
RUN pip3 install fastapi uvicorn python-dateutil inflect
EXPOSE 80
EXPOSE 443
CMD /root/run.sh

