#!/bin/bash
#set -x
WFSURL="http://geonode.wfp.org/geoserver/geonode/ows?service=wfs&version=1.1.0&request=GetFeature&typeName=geonode:global_24h&maxfeatures=1"

#set the connection timeout (in seconds)
TIMEOUT=30

# tomcat
TOMCAT_TIMEOUT=50
SERVICE="geoserver"
CMD_START="sudo service ${service} start"
CMD_STOP="sudo service ${service} stop"
LOGFILE="/var/log/geoserver/watchdog.log.geoserver"
RETRY=3

# geonode
USER=$GN_USER
PASSWORD=$GN_PWD

################### WATCHDOG #####################

url_test()
{
   TMPFILE=/tmp/urltest
   rm $TMPFILE
   sleep 15
   curl --max-time $TIMEOUT -u $USER:$PASSWORD $WFSURL > $TMPFILE 2>> $LOGFILE
   if grep 'numberOfFeatures="1"' $TMPFILE ; then
        return 0
   else
        return 1
   fi
}


times=0;

if [ ! -e "$LOGFILE" ]; then
    LOGFILE="/dev/stdout"
    echo "`date` WatchDog output file: DOES NOT EXIST: using ${LOGFILE}" >> "${LOGFILE}"
else
    echo "`date` WatchDog setting output to: ${LOGFILE}" >> "${LOGFILE}"
fi

#loop
while [ "$times" -lt "$RETRY" ]
do
      url_test

        #testing on url_test exit code
    if [ "$?" -eq 0 ] ; then
        echo "`date` WatchDog Status: OK -> $SERVICE is responding at URL $WFSURL" >> $LOGFILE
        #exit 0;
    else
        echo "`date` WatchDog Status: FAIL -> $SERVICE is NOT responding properly at URL $WFSURL" >> $LOGFILE
        echo "`date` WatchDog Action: Stopping service $SERVICE" >> $LOGFILE
        sudo killall -9 java
        sudo sh /opt/tomcat/bin/startup.sh
        sudo sh /opt/tomcat7/prod/tomcat/apache-tomcat-7.0.37/bin/startup.sh
        sudo sh /opt/tomcat7/stage/tomcat/apache-tomcat-7.0.37/bin/startup.sh
        sleep 60
    fi
done

return 100
