FROM alpine:latest
RUN apk add --no-cache openssl ca-certificates
ADD docker-entrypoint.sh /
CMD ["/docker-entrypoint.sh"]
