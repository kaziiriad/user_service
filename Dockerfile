FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.cargo/bin/:$PATH"

RUN uv venv /opt/venv
# Use the virtual environment automatically
ENV VIRTUAL_ENV=/opt/venv
# Place entry points in the environment at the front of the path
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt /app/

RUN uv pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Fixed code
CMD ["uv", "run", "manage.py", "migrate", "&&", "uv", "run", "manage.py", "runserver" "0.0.0.0:8000"]

