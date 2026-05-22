# Makefile for common tasks

.PHONY: build run docker

build:
	go build ./...

run:
	go run ./cmd -config=config.yaml

docker:
	docker build -t atheneum:local .
