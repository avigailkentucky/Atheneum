# Start from golang builder then produce a small image

FROM golang:1.20-alpine AS builder
WORKDIR /src
COPY . .
RUN go build -o /bin/atheneum ./cmd

FROM alpine:3.18
RUN apk add --no-cache ca-certificates
COPY --from=builder /bin/atheneum /usr/local/bin/atheneum
COPY config.yaml /etc/atheneum/config.yaml
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/atheneum", "-config", "/etc/atheneum/config.yaml"]
