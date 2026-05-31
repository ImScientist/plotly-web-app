FROM python:3.12-slim

ARG runtime_path
ENV app_dir="/home/app"
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY ${runtime_path} ${app_dir}
WORKDIR ${app_dir}

RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

EXPOSE 80

CMD ["gunicorn", "app_2:server", "-b", "0.0.0.0:80"]

# docker run -it --rm -p 80:80 plotly_app:1.0 /bin/bash
#"gunicorn app:server -b 0.0.0.0:80"