FROM python:3.11-alpine

RUN apk add make git wget bash

WORKDIR /app

COPY better_ais /app/better_ais
COPY requirements.txt /app/requirements.txt
COPY Makefile /app/Makefile
COPY .git /app/.git

RUN wget "https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh" -O /bin/wait-for-it && chmod +x /bin/wait-for-it
RUN make app_gen_build_info && pip install -r requirements.txt

CMD [ "wait-for-it", "db:5432", "--", "python", "-m", "better_ais" ]

EXPOSE 8000