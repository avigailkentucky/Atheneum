package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/avigailkentucky/Atheneum/pkg/heartbeat"
	"github.com/avigailkentucky/Atheneum/pkg/mesh"
	"github.com/avigailkentucky/Atheneum/pkg/crypto"
)

func main() {
	cfg := flag.String("config", "config.yaml", "path to config file")
	flag.Parse()

	fmt.Printf("Starting Atheneum with config=%s\n", *cfg)

	// Initialize crypto (keys, KEM/signature)
	if err := crypto.Init(); err != nil {
		log.Fatalf("crypto init: %v", err)
	}

	// Start mesh subsystem
	if err := mesh.Start(); err != nil {
		log.Fatalf("mesh start: %v", err)
	}

	// Start heartbeat
	heartbeat.Start()

	// Block forever (TODO: graceful shutdown)
	select {}
}
