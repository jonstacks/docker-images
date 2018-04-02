# Pgbadger

Dockerized version of [pgBadger](http://dalibo.github.io/pgbadger/).


## Usage

Put postgres logs into a local directory called `postgres-logs`. Make a
local directory, `html`, for output files. Running this command will
analyze the postgres logs and make an `out.html` file in the output
directory.


```
docker run --rm -it -v "$(pwd)/postgres-logs:/postgres-logs" -v "$(pwd)/html:/var/www/html" pgbadger
```
