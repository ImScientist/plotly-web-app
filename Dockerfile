FROM python:3.8

ARG runtime_path
ENV app_dir="/home/app"
ENV log_dir="/var/log/app"

COPY ${runtime_path} ${app_dir}
RUN mkdir -p "${log_dir}"
WORKDIR ${app_dir}

RUN pip install -r requirements.txt
RUN python setup.py install

EXPOSE 80

#CMD ["gunicorn", "app:server", "-b", "0.0.0.0:80"]
#"gunicorn app:server -b 0.0.0.0:80"