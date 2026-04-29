#! /bin/bash

city=Casablanca

curl -s wttr.in/$city?T --output weather_report

#To extract Current Temperature
obs_temp=$(curl -s wttr.in/$city?T | grep -m 1 '°.' | grep -Eo -e '-?[[:digit:]].*')
echo "The current Temperature of $city: $obs_temp"

# To extract the forecast tempearature for noon tomorrow
fc_temp=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°.' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*')
echo "The forecasted temperature for noon tomorrow for $city : $fc_temp C"

TZ='Africa/Casablanca'
read year month day <<< "$(TZ="$TZ" date +'%y %m %d')"

record=$(echo -e "$year\t$m\t$day\t$obs_temp\t$fc_temp C")
echo "$record">>rx_poc.log