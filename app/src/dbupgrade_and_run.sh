#!/bin/bash

source ./app-initdb.d/sql-commands.sh

# NOTE: file end of line characters must be LF, not CRLF (see https://stackoverflow.com/a/58220487/799921)

# create database if necessary
while ! ./app-initdb.d/create-database.sh
do
    sleep 5
done

# look for users sql file, should only be one, delete after loading sql into database
files=(/initdb.d/users-*.sql)
[ -f "$files" ] && ((${#files[@]}==1)) && docker_process_sql --database=users <$files && rm $files

# initial volume create may cause flask db upgrade to fail
# while ! flask db upgrade
# do
#     sleep 5
# done

flask db upgrade

exec "$@"
