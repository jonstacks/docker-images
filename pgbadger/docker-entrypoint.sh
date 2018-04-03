#!/bin/sh

exec pgbadger -O /var/www/html --prefix '%t:%r:%u@%d:[%p]:' /postgres-logs/postgresql.log.*

