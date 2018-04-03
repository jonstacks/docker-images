#!/bin/sh

RDS_IDENTIFIER="$1"

for f in $(aws rds describe-db-log-files --db-instance-identifier $RDS_IDENTIFIER | awk '{print $3}')
do
  echo "Downloading $f.."
  aws rds download-db-log-file-portion --db-instance-identifier $RDS_IDENTIFIER --log-file-name $f --starting-token 0 --output text > $(basename $f)
done
