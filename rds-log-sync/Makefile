
test:
	mkdir -p rds-logs
	docker build --pull -t rds-log-sync .
	docker run --rm -it -e AWS_ACCESS_KEY_ID='$(AWS_ACCESS_KEY_ID)' \
	                    -e AWS_SECRET_ACCESS_KEY='$(AWS_SECRET_ACCESS_KEY)'\
			    -e AWS_DEFAULT_REGION='us-west-2' \
			    -v "$$(pwd)/rds-logs:/rds-logs" \
			    rds-log-sync
