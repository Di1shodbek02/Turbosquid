FROM python:3.11-alpine

WORKDIR /app

COPY . .

#COPY entrypoint.sh /app/entrypoint.sh
RUN pip install --upgrade pip
RUN pip install -r req.txt

RUN chmod +x ./entrypoint.sh
RUN sed -i 's/\r$//g' ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]