#!/bin/bash

stop_all_processes()
{
	run=False
	echo "stopping process"
}
trap stop_all_processes TERM
run=True

echo "running process"
counter=1
while [ $run == True ]
do
	echo "running ..${counter}"
	python3 /app/outdu_cvat_create_manifest.py /data/wip /data/processed /home/django/utils/dataset_manifest/create.py
	sleep 10s
	counter=$((counter+1))
done
echo "process exited"
