FROM python:3.8.5

COPY ./erudite /erudite
COPY ./.env /

COPY ./requirements.txt /
RUN pip install -r requirements.txt

EXPOSE 6000

WORKDIR /erudite

CMD ["uvicorn", "main:app", "--port", "6000"]
