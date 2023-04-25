FROM python:3.11-alpine

WORKDIR /app

RUN pip install --upgrade pip
RUN apk add --no-cache build-base openldap-dev python3-dev linux-headers make git wget bash gcc
# https://stackoverflow.com/questions/70182720/python-ldap-3-4-installation-fails-on-alpine-images
RUN echo -n "INPUT ( libldap.so )" > /usr/lib/libldap_r.so
RUN wget "https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh" -O /bin/wait-for-it && chmod +x /bin/wait-for-it

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY Makefile /app/Makefile
COPY .git /app/.git
COPY better_ais /app/better_ais

RUN make app_gen_build_info

CMD [ "wait-for-it", "db:5432", "--", "python", "-m", "better_ais" ]

EXPOSE 8000