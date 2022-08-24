#!/bin/bash
cron
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
	cat /tmp/app.log
	sleep 10s
	counter=$((counter+1))
done
echo "process exited"
