FROM python:3.9
COPY . /monitoring
WORKDIR /monitoring
ENV PYTHONPATH=/monitoring
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD python services/kafka_producer/producer_runner.py