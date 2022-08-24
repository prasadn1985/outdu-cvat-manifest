from cvat/server:latest

USER root

# General
RUN apt-get update && apt-get --no-install-recommends install -y \
    python3-dev python3-pip python3-venv pkg-config

# Library components
RUN apt-get install --no-install-recommends -y \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev

RUN pip install -U pip
RUN pip install -r utils/dataset_manifest/requirements.txt

RUN apt-get --no-install-recommends install -y bash apt-utils ffmpeg

RUN mkdir /app
ADD outdu_cvat_create_manifest.py /app
ADD run.sh /app

RUN chmod 0644 /app/run.sh
#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Add the cron job
RUN crontab -l | { cat; echo "* * * * * bash /app/run.sh"; } | crontab -
RUN touch /tmp/app.log
ADD run_live.sh /app
RUN chmod +x /app/run_live.sh
