#!/bin/bash

# Exit script in case of error
set -e

INVOKE_LOG_STDOUT=${INVOKE_LOG_STDOUT:-FALSE}
invoke () {
    if [ $INVOKE_LOG_STDOUT = 'true' ] || [ $INVOKE_LOG_STDOUT = 'True' ]
    then
        /usr/local/bin/invoke $@
    else
        /usr/local/bin/invoke $@ > /usr/src/geonode/invoke.log 2>&1
    fi
    echo "$@ tasks done"
}

# Start cron && memcached services
service cron restart

echo $"\n\n\n"
echo "-----------------------------------------------------"
echo "STARTING DJANGO ENTRYPOINT $(date)"
echo "-----------------------------------------------------"

invoke update

source $HOME/.bashrc
source $HOME/.override_env

echo DOCKER_API_VERSION=$DOCKER_API_VERSION
echo POSTGRES_USER=$POSTGRES_USER
echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD
echo DATABASE_URL=$DATABASE_URL
echo GEODATABASE_URL=$GEODATABASE_URL
echo SITEURL=$SITEURL
echo ALLOWED_HOSTS=$ALLOWED_HOSTS
echo GEOSERVER_PUBLIC_LOCATION=$GEOSERVER_PUBLIC_LOCATION

# invoke waitfordbs

cmd="$@"

if [ ${IS_CELERY} = "true" ]  || [ ${IS_CELERY} = "True" ]
then
    echo "Executing Celery server $cmd for Production"
else

    invoke migrations
    invoke prepare

    STATIC_ROOT="${STATIC_ROOT:-/mnt/volumes/statics/static/}"
    LOCKFILE_DIR="$(dirname "$STATIC_ROOT")"
    if [ ${FORCE_REINIT} = "true" ]  || [ ${FORCE_REINIT} = "True" ] || [ ! -e "${LOCKFILE_DIR}/geonode_init.lock" ]; then
        invoke fixtures
        invoke initialized
        invoke updateadmin
    fi

    invoke statics

    echo "Executing UWSGI server $cmd for Production"
fi

echo "-----------------------------------------------------"
echo "FINISHED DJANGO ENTRYPOINT --------------------------"
echo "-----------------------------------------------------"

# Run the CMD 
echo "got command $cmd"
exec $cmd
