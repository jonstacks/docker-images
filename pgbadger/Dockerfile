FROM alpine

RUN apk add --no-cache perl make

# Directory to put the html reports in. This will create the
# directory. We'll use a separate nginx container with a volume
# mount to serve these files.
WORKDIR /var/www/html

WORKDIR /tmp
ADD https://github.com/dalibo/pgbadger/archive/v9.2.tar.gz pgbadger-9.2.tar.gz
RUN tar xzf pgbadger-9.2.tar.gz && \
    cd pgbadger-9.2 && \
    perl Makefile.PL && \
    make && make install

WORKDIR /postgres-logs
ADD docker-entrypoint.sh /

CMD ["/docker-entrypoint.sh"]
