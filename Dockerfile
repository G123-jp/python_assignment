#-----------Install requirements and setup virtualenv---------------

FROM python:3.7-slim-buster AS compile-image
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential python-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN python -m pip install --upgrade pip


#-----------Run unit tests---------------

FROM compile-image AS test-image
COPY requirements-dev.txt /
RUN pip install -r requirements-dev.txt
COPY app /app
COPY tests /tests
COPY tox.ini /
RUN tox

#-----------Run final image---------------

FROM python:3.7-slim-buster AS runtime-image
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
COPY financial /financial

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "600", "--chdir", "financial", "--worker-class", "gevent", "run:api"]