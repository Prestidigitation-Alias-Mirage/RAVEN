FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY raven ./raven
RUN python -m pip install --no-cache-dir .
COPY configs ./configs
COPY suites ./suites
RUN mkdir -p runs

ENTRYPOINT ["raventest"]
CMD ["--help"]
