package main

import (
	"context"
	"log"
	"time"

	"github.com/libp2p/go-libp2p"
	"github.com/libp2p/go-libp2p-core/crypto"
	"github.com/libp2p/go-libp2p-core/host"
	"github.com/libp2p/go-libp2p-core/peer"
	"github.com/libp2p/go-libp2p-core/routing"
	"github.com/libp2p/go-libp2p-discovery"
	"github.com/libp2p/go-libp2p-kad-dht"
	"github.com/libp2p/go-libp2p-p2p/net/connmgr"
	"github.com/libp2p/go-libp2p-p2p/security/noise"
	libp2ptls "github.com/libp2p/go-libp2p-p2p/security/tls"
	"github.com/libp2p/go-libp2p-p2p/discovery/mdns"
)

func main() {
	run()
}

func run() {
	// The context governs the lifetime of the libp2p node
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Generate a key pair for this host
	priv, _, err := crypto.GenerateKeyPair(crypto.Ed25519, -1)
	if err != nil {
		log.Fatal(err)
	}

	var idht *dht.IpfsDHT

	// Create a connection manager
	connmgr, err := connmgr.NewConnManager(100, 400, connmgr.WithGracePeriod(time.Minute))
	if err != nil {
		log.Fatal(err)
	}

	// Create a host with additional options like security, transports, and connection manager
	h, err := libp2p.New(
		libp2p.Identity(priv),
		libp2p.ListenAddrStrings("/ip4/0.0.0.0/tcp/10000", "/ip4/0.0.0.0/udp/10000/quic"),
		libp2p.Security(libp2ptls.ID, libp2ptls.New),
		libp2p.Security(noise.ID, noise.New),
		libp2p.DefaultTransports,
		libp2p.ConnectionManager(connmgr),
		libp2p.NATPortMap(),
		libp2p.Routing(func(h host.Host) (routing.PeerRouting, error) {
			idht, err = dht.New(ctx, h)
			return idht, err
		}),
		libp2p.EnableNATService(),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer h.Close()

	// Setup mDNS discovery
	mdnsService, err := mdns.NewMdnsService(ctx, h, discovery.MdnsServiceTag)
	if err != nil {
		log.Fatal(err)
	}
	defer mdnsService.Close()

	// Setup DHT
	if err := idht.Bootstrap(ctx); err != nil {
		log.Fatal(err)
	}

	// Discover peers using mDNS
	mdns := discovery.NewMdnsService(ctx, h, time.Hour, discovery.ServiceTag)
	mdns.RegisterNotifee(&discoveryNotifee{h})

	// Connect to bootstrap nodes
	bootstrapPeers := dht.DefaultBootstrapPeers
	for _, peerAddr := range bootstrapPeers {
		peerinfo, _ := peer.AddrInfoFromP2pAddr(peerAddr)
		if err := h.Connect(ctx, *peerinfo); err != nil {
			log.Println("Error connecting to bootstrap peer:", err)
		}
	}

	log.Printf("Hello World, my hosts ID is %s\n", h.ID())
}

// discoveryNotifee is notified when a new peer is discovered
type discoveryNotifee struct {
	h host.Host
}

func (n *discoveryNotifee) HandlePeerFound(pi peer.AddrInfo) {
	log.Println("Discovered new peer:", pi.ID)
	n.h.Connect(context.Background(), pi)
}
