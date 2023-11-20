FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN apk --no-cache add bash  # Install bash if not already present
RUN pip install --upgrade pip \
    && pip install -r req.txt

RUN chmod +x entrypoint.sh \
    && sed -i 's/\r$//g' entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
