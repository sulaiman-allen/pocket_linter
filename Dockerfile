FROM alpine:3.7
EXPOSE 3031
WORKDIR /usr/src/pocket_linter
RUN apk add --no-cache \
        python3 \
        uwsgi-python3

RUN mkdir /install_requirements

COPY ./requirements.txt /install_requirements/requirements.txt
RUN pip3 install --no-cache-dir -r /install_requirements/requirements.txt

ENV FLASK_APP=/usr/src/pocket_linter/routes.py
ENV FLASK_DEBUG=1 

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "uwsgi", \
               "--wsgi", "routes" ]
