FROM python:3.11-alpine

WORKDIR /app

COPY . .

#COPY entrypoint.sh /app/entrypoint.sh
RUN pip install --upgrade pip
RUN pip install -r req.txt

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]