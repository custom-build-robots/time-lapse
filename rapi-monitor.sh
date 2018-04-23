#! /bin/bash
sleep 2s
now="$(date '+%Y%m%d%H%M%S')"

echo "Year;Month;Day;Hour;Minute;Second;CPU Temp;Volts;clock" >> /home/pi/monitor_$now.csv

while true; do
	act_time="$(date '+%Y;%m;%d;%H;%M;%S')"
	cpu_temp=`/opt/vc/bin/vcgencmd measure_temp` 
	volts=`/opt/vc/bin/vcgencmd measure_volts`
	clock=`/opt/vc/bin/vcgencmd measure_clock arm`
	echo $act_time";"$cpu_temp";"$volts";"$clock >> /home/pi/monitor_$now.csv
	sleep 1s
done
