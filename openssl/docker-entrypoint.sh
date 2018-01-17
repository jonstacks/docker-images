#!/bin/sh


fail () { printf "FAIL\n"; }
ok () { printf "OK\n"; }

opts='-ssl3 -tls1 -tls1_1 -tls1_2'

for opt in $opts
do
  echo "Q" | openssl s_client -connect ${HOST}:443 $opt -servername ${HOST} > /dev/null 2>&1
  rc=$?
  printf "$opt - "
  if [[ $rc != 0 ]]
  then
    fail
  else
    ok
  fi
done
