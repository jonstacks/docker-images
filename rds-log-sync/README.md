# RDS Log Sync

Syncs your RDS logs to a given directory. Logs are collected for all RDS
instances and sorted by DB Instance Identifier.

# Example

```
docker run --rm -it -e AWS_ACCESS_KEY_ID='ABCD' \
                    -e AWS_SECRET_ACCESS_KEY='ABCD' \
                    -v '$(pwd)/rds-logs:/rds-logs' \
                    rds-log-sync
```
