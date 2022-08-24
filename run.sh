#!/bin/bash
date && python3 /app/outdu_cvat_create_manifest.py /data/wip /data/processed /home/django/utils/dataset_manifest/create.py > /tmp/app.log
