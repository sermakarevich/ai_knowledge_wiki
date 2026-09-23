# Technical Analysis: livekit

**Repository:** https://github.com/livekit/livekit
**Version analyzed:** v1.x (go.mod module `github.com/livekit/livekit-server`, Go 1.26)
**Date:** 2026-05-28

---

## 1. Overview / What Problem It Solves

Real-time video and audio conferencing on the web is deceptively hard: WebRTC handles peer encryption and codecs, but does not define how to route media between more than two endpoints, how to scale to hundreds of participants, or how to coordinate across geographically distributed servers. The naive peer-mesh approach (each client connects to every other client) collapses at four or five participants due to upload bandwidth exhaustion and CPU load from encoding N copies of each stream.

LiveKit solves this with a **Selective Forwarding Unit (SFU)**: every publisher uploads once to the server, and the server relays each RTP packet to each subscriber. The server does not decode or re-encode, so it scales to large rooms with modest CPU. LiveKit adds on top: JWT-based API-key authentication, a room abstraction with participant identity, simulcast (publisher sends multiple quality layers; server selects the appropriate one per subscriber based on bandwidth), adaptive bitrate via sender-side BWE, end-to-end encryption, built-in TURN server, WHIP ingest, SIP bridging, and first-class support for AI "agent" participants.

The primary users are product engineering teams building video conferencing, live streaming, or real-time AI voice/video applications. The server is a single Go binary, deployable as Docker or on Kubernetes, and scales horizontally using Redis as the coordination layer. The Agents ecosystem (a separate repo) connects AI pipelines as room participants through the same signaling protocol.

---

## 2. High-Level Architecture

```
Client (Browser / Mobile / SDK)
        │  WebSocket /rtc or /rtc/v1
        ▼
┌─────────────────────────────────┐
│  RTCService  (pkg/service)      │  HTTP + WebSocket
│  RoomService / AgentService /   │  Twirp / HTTP/Protobuf
│  EgressService / IngressService │
│  SIPService / WHIPService       │
└──────────────┬──────────────────┘
               │ PSRPC (Redis pub/sub or NATS)
               ▼
┌─────────────────────────────────┐
│  RoomManager  (pkg/service)     │  one per node
│  ├─ rtc.Room  (pkg/rtc)         │  one per active room
│  │   └─ Participant (pkg/rtc)   │  one per connected client
│  │       ├─ Publisher PC        │  pion/webrtc PeerConnection
│  │       └─ Subscriber PC       │
│  └─ SFU layer (pkg/sfu)         │
│      ├─ Receiver (upstream)     │
│      └─ DownTrack (downstream)  │
└──────────────┬──────────────────┘
               │ Redis HSET/HGET (node registry, room→node map)
               ▼
┌──────────────────────┐   ┌─────────────────────┐
│  Redis               │   │  TURN Server         │
│  node registry       │   │  (in-process pion)   │
│  room_node_map       │   │  UDP 3478 / TLS 5349 │
│  object store        │   └─────────────────────┘
└──────────────────────┘
```

**Data flow from client join to media playback (end-to-end path):**

1. Client opens WebSocket to `/rtc/v1`, sending a base64-encoded `WrappedJoinRequest` proto with a JWT.
2. `RTCService.validateInternal()` verifies the JWT, constructs a `ParticipantInit` struct with identity, grants, and connection preferences.
3. `RoomAllocator.SelectRoomNode()` queries Redis `room_node_map` to find (or assign) the RTC node for this room; `Router.StartParticipantSignal()` opens a `MessageSink`/`MessageSource` channel pair to that node via PSRPC.
4. On the RTC node, `RoomManager.StartSession()` calls `rtc.NewParticipant()` with full config, then `room.Join()`. The participant initializes two `pion/webrtc` `PeerConnection`s — one for publishing, one for subscribing.
5. SDP offer/answer flows over the WebSocket signal channel. ICE candidates are exchanged; the client sends media via SRTP.
6. `pkg/sfu.WebRTCReceiver` buffers incoming RTP packets from the publisher's PC, depacketizes, runs interceptors (RTX, TWCC feedback), and feeds a `buffer.Buffer`.
7. `pkg/sfu.DownTrack` pulls from the buffer and writes RTP to each subscriber's PC, applying `Forwarder` logic: simulcast layer selection, sequence number/timestamp rewriting, and pacing via a leaky-bucket `Pacer`.
8. `StreamAllocator` continuously adjusts which spatial/temporal simulcast layers each `DownTrack` forwards, driven by BWE estimates and subscriber feedback.

Persistent state lives in **Redis** (distributed mode) or in-process Go maps (single-node `LocalStore`/`LocalRouter`). There is no on-disk database; rooms are ephemeral.

---

## 3. The Room and Participant Graph

The central domain abstraction is the **Room** (`pkg/rtc/room.go`) containing a set of **Participants** (`pkg/rtc/participant.go`), each holding published and subscribed **Tracks**.

**Room** (`pkg/rtc/room.go`):
- Holds `map[livekit.ParticipantIdentity]types.LocalParticipant`
- Owns a `buffer.Factory` (shared across all participants for zero-copy buffer allocation)
- Owns a `Trailer` for RTP extension headers
- Notifies on participant change, room update, and close via registered callbacks

**Participant** (`pkg/rtc/participant.go`, ~3,200 lines):
- Wraps two `pion/webrtc.PeerConnection`: `publisher` (receives tracks from the client) and `subscriber` (sends tracks to the client)
- Holds `UpTrackManager` (published tracks it owns) and `SubscriptionManager` (tracks it subscribes to)
- Implements `types.LocalParticipant` interface (`pkg/rtc/types/interfaces.go:35803 bytes`)
- Key kinds distinguished by `livekit.ParticipantInfo_Kind`: `STANDARD`, `INGRESS`, `EGRESS`, `SIP`, `AGENT`

**Track** kinds in the protocol (`github.com/livekit/protocol/livekit`):
- `TrackType_AUDIO`, `TrackType_VIDEO`, `TrackType_DATA`
- Source: `TrackSource_CAMERA`, `MICROPHONE`, `SCREEN_SHARE`, `SCREEN_SHARE_AUDIO`

**SFU Receiver** (`pkg/sfu/receiver_base.go`, ~850 lines):
- One `WebRTCReceiver` per published track
- Maintains up to three simulcast `TrackRemote` layers (low/medium/high)
- Uses `buffer.Buffer` per layer; pool-allocated via `sync.Pool` in `pkg/sfu/sfu.go`

**SFU DownTrack** (`pkg/sfu/downtrack.go`, ~2,200 lines):
- One per (subscriber, track) pair
- Maintains `Forwarder` state: which spatial/temporal layer is active, sequence number munger, timestamp offset
- Key method: `WriteRTP()` — called by the buffer goroutine for every inbound RTP packet

**Node selector** (`pkg/routing/selector/interfaces.go`):
```go
type NodeSelector interface {
    SelectNode(nodes []*livekit.Node) (*livekit.Node, error)
}
```
Implementations: `AnySelector`, `CPULoadSelector`, `SystemLoadSelector`, `RegionAwareSelector`. Sort criteria: `sysload`, `cpuload`, `rooms`, `clients`, `tracks`, `bytespersec`. Algorithms: `lowest` (scan all), `twochoice` (Power of Two random choices).

Node availability check (`pkg/routing/selector/utils.go:IsAvailable`): a node is available if `NodeStats.UpdatedAt` was within the last 5 seconds and `State == NodeState_SERVING`.

---

## 4. LLM / External Service Integration

LiveKit server does **not** call any LLM or AI API itself. It is pure infrastructure — a media router. The AI integration point is the **Agents SDK** (separate repos: `github.com/livekit/agents` for Python, `github.com/livekit/agents-js` for Node.js), which connects AI pipelines to rooms as `ParticipantKind_AGENT` participants using the same WebRTC signaling.

The server provides `pkg/agent/` as the agent coordination layer:
- `agent.Client` dispatches jobs to agent workers via PSRPC (`pkg/agent/client.go`)
- `AgentService` exposes HTTP endpoints so agent workers register themselves and receive room assignment events
- Agent workers connect as standard WebRTC participants; the server treats them identically from an RTP routing perspective

External services the server does connect to:
| Service | Purpose | Required |
|---------|---------|---------|
| Redis | Node registry, signal routing, object store | Optional (single-node works without) |
| Egress service | Room recording, composite layouts, RTMP multistream | Optional |
| Ingress service | RTMP/WHIP/HLS ingest | Optional |
| SIP service | SIP trunk bridging | Optional |
| STUN servers | ICE candidate gathering | Default: public Google STUN |
| Jaeger | Distributed tracing | Optional (`conf.Trace.JaegerURL`) |

---

## 5. The Participant Join Pipeline

This is the primary user-facing workflow: a client connects and begins publishing/subscribing media.

**Step 1 — HTTP Upgrade** (`pkg/service/rtcservice.go:serve`):
Client sends WebSocket upgrade to `/rtc/v1`. `RTCService.validateInternal()` decodes the base64-gzipped `WrappedJoinRequest` proto, verifies the JWT grant, and populates a `routing.ParticipantInit`.

**Step 2 — Node Selection** (`pkg/service/rtcservice.go:startConnection`):
`RoomAllocator.SelectRoomNode()` checks Redis `room_node_map`; if the room has no node yet, the `NodeSelector` picks one from the live node list and stores it. `Router.StartParticipantSignal()` creates a PSRPC channel to that node, returning a `MessageSink` (requests in) and `MessageSource` (responses out).

**Step 3 — Room and Participant Creation** (`pkg/service/roommanager.go:StartSession`):
On the chosen RTC node, `getOrCreateRoom()` loads or constructs an `rtc.Room`. `rtc.NewParticipant()` initializes the participant with two `pion/webrtc.PeerConnection`s, congestion control config, codec lists, and all callbacks. `room.Join()` adds the participant to the room and starts sending it a `JoinResponse` with existing participant info.

**Step 4 — SDP Negotiation** (`pkg/rtc/transport.go`, `pkg/rtc/participant_sdp.go`):
Initial SDP offer (publisher) or answer (subscriber) flows over the WebSocket. `TransportManager` coordinates the dual-PC negotiation state machine. ICE gathering runs in Pion; UDP mux and TCP mux are pre-allocated at server startup.

**Step 5 — Track Publication** (`pkg/rtc/uptrackmanager.go`, `pkg/sfu/receiver_base.go`):
Once DTLS/SRTP is established, the publisher's RTP stream arrives. `WebRTCReceiver` per track buffers packets, runs TWCC (transport-wide congestion control) feedback generation, NACK handling, and RED/OPUS FEC decapsulation.

**Step 6 — Subscription and Forwarding** (`pkg/rtc/subscriptionmanager.go`, `pkg/sfu/downtrack.go`):
`SubscriptionManager` matches subscribers to published tracks. For each match, a `DownTrack` is created and added to the room's subscriber PC via `rtc/Transport.AddTrack()`. `StreamAllocator` (`pkg/sfu/streamallocator/streamallocator.go`) runs a control loop using BWE signals to pick the highest-quality simulcast layer each subscriber can sustain.

**Step 7 — Signal Loop** (`pkg/service/roommanager.go:rtcSessionWorker`):
A dedicated goroutine per participant reads from the request `MessageSource` and dispatches signal messages (offers, answers, ICE candidates, mute events, data channel packets) to `participant.HandleSignalMessage()`. JWT refresh happens every 5 minutes.

---

## 6. Key Files

| File | Lines (approx) | What It Does |
|------|----------------|--------------|
| `pkg/rtc/participant.go` | ~3,200 | Core participant: dual PeerConnections, track management, signal dispatch, ICE config |
| `pkg/sfu/downtrack.go` | ~2,200 | RTP forwarding to one subscriber: layer selection, seq/ts rewriting, RTX, pacing |
| `pkg/sfu/forwarder.go` | ~2,100 | Simulcast/SVC spatial+temporal layer state machine, RTP munging state |
| `pkg/rtc/transport.go` | ~2,600 | Pion PeerConnection wrapper: negotiation state, ICE restart, DTLS fingerprint |
| `pkg/rtc/room.go` | ~2,000 | Room: participant set, data channel routing, update broadcasting, close lifecycle |
| `pkg/rtc/subscriptionmanager.go` | ~1,200 | Subscription lifecycle: create/remove DownTracks, handle track changes |
| `pkg/sfu/streamallocator/streamallocator.go` | ~1,200 | Per-participant stream quality allocation driven by BWE and subscriber requests |
| `pkg/service/roommanager.go` | ~1,000 | StartSession, getOrCreateRoom, rtcSessionWorker, ICE credential generation |
| `pkg/rtc/transportmanager.go` | ~850 | Coordinates publisher + subscriber Transport pair, ICE preference, fallback |
| `pkg/sfu/receiver_base.go` | ~850 | Upstream track buffering, NACK, TWCC feedback, RED handling |
| `pkg/sfu/bwe/sendsidebwe/congestion_detector.go` | ~900 | Send-side BWE: congestion signal detection from TWCC feedback |
| `pkg/service/rtcservice.go` | ~600 | WebSocket endpoint: upgrade, validate, pump messages, ping/pong |
| `pkg/service/wire_gen.go` | ~300 | Google Wire DI: full server assembly, all provider functions |
| `pkg/routing/redisrouter.go` | ~280 | Redis-backed node registry, room→node map, keepalive pub/sub |
| `pkg/routing/interfaces.go` | ~250 | Router, MessageSink, MessageSource, ParticipantInit definitions |
| `pkg/telemetry/telemetryservice.go` | ~400 | Event fan-out: Prometheus, analytics, webhook notifications |
| `cmd/server/main.go` | ~280 | CLI entry point, flag parsing, server bootstrap, signal handling |
| `pkg/config/config.go` | ~700 | Full config struct with yaml tags; `GenerateCLIFlags` generates flags from struct |
| `pkg/rtc/mediatrackreceiver.go` | ~850 | Track reception from Pion: simulcast layer binding, codec negotiation |
| `pkg/rtc/types/interfaces.go` | ~900 | All major interfaces: LocalParticipant, MediaTrack, SubscribedTrack, etc. |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `github.com/pion/webrtc/v4` | `v4.2.11` | WebRTC implementation (ICE, DTLS, SRTP, PeerConnection) |
| `github.com/pion/ice/v4` | `v4.2.3` | ICE candidate gathering and connectivity checks |
| `github.com/pion/dtls/v3` | `v3.1.2` | DTLS 1.2/1.3 for key exchange |
| `github.com/pion/turn/v5` | `v5.0.4` | In-process TURN server |
| `github.com/pion/rtcp` | `v1.2.16` | RTCP packet parsing and generation |
| `github.com/pion/rtp` | `v1.10.1` | RTP packet parsing and generation |
| `github.com/pion/sdp/v3` | `v3.0.18` | SDP offer/answer parsing |
| `github.com/pion/interceptor` | `v0.1.44` | RTP interceptors (NACK, TWCC, RTCP sender reports) |
| `github.com/pion/sctp` | `v1.9.5` | SCTP for WebRTC data channels |
| `github.com/livekit/protocol` | `v1.45.9-0.20260519061926-...` | Protobuf types, JWT auth, PSRPC definitions, RPC clients |
| `github.com/livekit/psrpc` | `v0.7.1` | PubSub RPC framework (Redis or NATS transport) |
| `github.com/livekit/mediatransportutil` | `v0.0.0-20260521171458-...` | RTC network config helpers |
| `github.com/redis/go-redis/v9` | `v9.18.0` | Redis client (node registry, routing, object store) |
| `github.com/gorilla/websocket` | `v1.5.3` | WebSocket upgrade and framing |
| `github.com/twitchtv/twirp` | `v8.1.3+incompatible` | HTTP/Protobuf RPC for Room/Egress/Ingress APIs |
| `github.com/prometheus/client_golang` | `v1.23.2` | Prometheus metrics exposition |
| `go.uber.org/zap` | `v1.27.1` | Structured logging |
| `github.com/google/wire` | `v0.7.0` | Compile-time dependency injection code generation |
| `github.com/urfave/cli/v3` | `v3.8.0` | CLI flags and subcommand routing |
| `gopkg.in/yaml.v3` | `v3.0.1` | YAML config file parsing |
| `google.golang.org/protobuf` | `v1.36.11` | Protobuf runtime |
| `github.com/florianl/go-tc` | `v0.4.7` | Linux Traffic Control (tc) for kernel-level packet shaping |
| `github.com/d5/tengo/v2` | `v2.17.0` | Tengo scripting language for client configuration matching rules |
| `github.com/jellydator/ttlcache/v3` | `v3.4.0` | TTL-expiring in-memory cache (ICE config cache) |
| `go.opentelemetry.io/otel` | `v1.43.0` | OpenTelemetry tracing (indirect via psrpc) |

---

## 8. CLI / Usage Surface

**Entry point** (`go.mod` + `.goreleaser.yaml`): `./cmd/server` → binary `livekit-server`

**Commands:**
```shell
# Start server (default action)
livekit-server [flags]
livekit-server --dev                        # development mode: placeholder keys, debug logs
livekit-server --config config.yaml         # YAML config file
livekit-server --config-body "$LIVEKIT_CONFIG"

# Utilities
livekit-server generate-keys               # print a new API key / secret pair
livekit-server ports                        # print all ports the server will use
livekit-server list-nodes                   # list Redis-registered nodes with stats
livekit-server help-verbose                 # show all generated config flags
```

**Key environment variables:**

| Variable | Purpose |
|----------|---------|
| `LIVEKIT_CONFIG` | Full YAML config body (same as `--config-body`) |
| `LIVEKIT_KEYS` | `key: secret\n` pairs |
| `LIVEKIT_REGION` | Region identifier for RegionAwareSelector |
| `NODE_IP` | Advertised node IP for ICE candidates |
| `UDP_PORT` | WebRTC UDP port or range |
| `REDIS_HOST` | Redis host:port |
| `REDIS_PASSWORD` | Redis password |
| `LIVEKIT_TURN_CERT` | TLS cert for TURN/TLS |
| `LIVEKIT_TURN_KEY` | TLS key for TURN/TLS |

**HTTP endpoints** (registered in `pkg/service/server.go`):

| Path | Protocol | Purpose |
|------|----------|---------|
| `/rtc` | WebSocket | Signal channel v0 (legacy, no join request) |
| `/rtc/v1` | WebSocket | Signal channel v1 (with `WrappedJoinRequest`) |
| `/rtc/validate` and `/rtc/v1/validate` | HTTP GET | Pre-flight JWT validation |
| `/twirp/livekit.RoomService/...` | HTTP/Protobuf | Room management API |
| `/whip/:resource` | HTTP | WHIP ingest |
| `/debug/pprof/...` | HTTP | pprof (dev mode only) |
| `:6789/metrics` | HTTP | Prometheus metrics (`conf.PrometheusPort`) |

**Config file** (`config-sample.yaml` at repo root):

| Path | Purpose |
|------|---------|
| `config-sample.yaml` | Annotated sample covering all knobs |
| `config.yaml` (user-supplied) | Active config; path via `--config` |
| Key file (user-supplied) | `key: secret` YAML; path via `--key-file`; must have `0--0` other permissions |

---

## 9. Extensibility Points

- **New node selector strategy**: implement `NodeSelector` in `pkg/routing/selector/interfaces.go:53` — add a `case` to `CreateNodeSelector()` in the same file and register a new `kind` string in config. The selector receives the full `[]*livekit.Node` list with current stats.

- **New codec support**: implement a `CodecMunger` in `pkg/sfu/codecmunger/` (see `vp8.go` for reference), satisfying the `CodecMunger` interface. Register the MIME type in `pkg/rtc/mediaengine.go`. The forwarder calls `CodecMunger.UpdateHeader()` on every forwarded RTP packet to rewrite codec-specific header fields.

- **New storage backend**: implement the `ObjectStore` interface in `pkg/service/interfaces.go`. Switch from Redis to the new store by adding a case in `createStore()` in `pkg/service/wire_gen.go` (or modify `wire.go` and regenerate).

- **New RPC transport**: replace `psrpc.NewRedisMessageBus()` with a custom `psrpc.MessageBus` implementation (NATS is already supported by psrpc). Change `getMessageBus()` in `pkg/service/wire_gen.go:getMessageBus`.

- **Custom telemetry sink**: implement `telemetry.AnalyticsService` in `pkg/telemetry/analyticsservice.go` and wire it into `createTelemetryService()` in `wire_gen.go`. The existing implementation sends to LiveKit Cloud analytics; a no-op or custom sink can replace it without touching the event emission code.

- **Agent worker integration**: implement the PSRPC `AgentService` worker protocol (defined in `livekit/protocol`) and register via `AgentService.HandleWorkerRegister`. The `pkg/agent/client.go` dispatches room/participant/track events to registered workers.

---

## 10. Limitations and Gotchas

- **Room pinned to one RTC node**: Redis `room_node_map` maps room name → single node ID. If that node crashes, every participant in the room loses their session. There is no hot-standby; clients must do a full reconnect and land on a new node.

- **`os.Exit(1)` on panic**: `rtcSessionWorker`, the WebSocket response goroutine in `RTCService`, and several other goroutines call `os.Exit(1)` after `rtc.Recover()`. A bug in any one participant's signal handler can kill the whole process, affecting all rooms on that node.

- **MoveParticipant / ForwardParticipant not implemented**: `pkg/service/roommanager.go:ForwardParticipant` and `MoveParticipant` both return `errors.New("not implemented")`. Live participant migration between nodes is not functional despite being in the RPC interface.

- **Config YAML strict mode is opt-out**: `--disable-strict-config` is a hidden flag, implying the YAML schema has known cases where strict parsing is too aggressive. Configs from older deployments may need this flag.

- **Linux TC dependency for packet shaping**: `github.com/florianl/go-tc` only works on Linux. The `magefile_unix.go` / `magefile_windows.go` split suggests some features are platform-gated, but the binary is compiled for all GOOS targets with `CGO_ENABLED=0`.

- **Node availability window is 5 seconds**: `selector.AvailableSeconds = 5`. If a node's stats update is delayed (e.g., load spike causing `statsWorker` goroutine starvation), it is immediately excluded from node selection. The `RedisRouter.statsWorker` dumps goroutine stacks and logs an error but does not self-heal.

- **Redis as SPOF in distributed mode**: all cross-node coordination (signal routing, keepalive, room→node mapping, object store) depends on Redis. There is no fallback path; a Redis outage prevents new participants from joining across nodes and breaks existing signal relay.

- **Counterfeiter-generated fakes are large**: `pkg/rtc/types/typesfakes/` contains hundreds of KB of generated mock code checked into the repo. These are compile-time dependencies for tests but inflate `go build` cold-cache times.

---

## 11. How It Compares to Alternatives

**mediasoup** (Node.js control plane, C++ Worker): Lower-level library with no built-in rooms, auth, or multi-node coordination. Gives finer control over media routing (pipe transports, custom data consumers) and is commonly used when application logic needs deep media manipulation. LiveKit trades that flexibility for a batteries-included platform (auth, recording, SIP, agents) with a hosted cloud option.

**Janus Gateway** (C): Plugin-based WebRTC server with broader protocol coverage (SIP, MQTT, Lua scripting). More operationally complex — plugins as shared libraries, no native distributed mode, manual TURN config. Janus predates the simulcast / BWE era and its scaling story relies on manual clustering. LiveKit has substantially better out-of-the-box BWE and a better Go ecosystem for cloud-native deployment.

**Jitsi Videobridge** (Java/Kotlin): Battle-tested for large-scale conferencing; uses Octo cascading for multi-node rooms (all nodes share a room, unlike LiveKit's single-node-per-room model). JVB's cascading is more resilient to node failure. The tradeoff: JVM startup/memory overhead, tighter coupling to the Jitsi Meet frontend, weaker SDK ecosystem for custom applications.

**Ion SFU** (Go, Pion): Simpler, no Redis, no agent framework, no built-in auth. A good reference for understanding Pion-based SFU architecture, but unsuitable for production conferencing at scale. LiveKit started from similar Pion foundations and adds the distributed coordination, congestion control, and service integrations that Ion SFU leaves to the application.

**Positioning**: LiveKit is the most complete open-source WebRTC SFU for teams building production real-time applications without operating a media server fleet themselves. Its cloud offering and SDK breadth make it the fastest path to production; the open-source server makes it auditable and self-hostable.

---

## Appendix: Selected Code Snippets

**`startConnection` — signal channel setup before WebSocket upgrade** (`pkg/service/rtcservice.go:443-478`)

```go
func (s *RTCService) startConnection(
    ctx context.Context,
    roomName livekit.RoomName,
    pi routing.ParticipantInit,
    timeout time.Duration,
) (connectionResult, *livekit.SignalResponse, error) {
    var cr connectionResult
    var err error

    if err := s.roomAllocator.SelectRoomNode(ctx, roomName, ""); err != nil {
        return cr, nil, err
    }

    // this needs to be started first *before* using router functions on this node
    cr.StartParticipantSignalResults, err = s.router.StartParticipantSignal(ctx, roomName, pi)
    if err != nil {
        return cr, nil, err
    }

    // wait for the first message before upgrading to websocket. If no one is
    // responding to our connection attempt, we should terminate the connection
    // instead of waiting forever on the WebSocket
    initialResponse, err := readInitialResponse(cr.ResponseSource, timeout)
    if err != nil {
        // close the connection to avoid leaking
        cr.RequestSink.Close()
        cr.ResponseSource.Close()
        return cr, nil, err
    }

    return cr, initialResponse, nil
}
```

**`SelectSortedNode` — "Power of Two" node selection** (`pkg/routing/selector/utils.go:76-106`)

```go
func SelectSortedNode(nodes []*livekit.Node, sortBy string, algorithm string) (*livekit.Node, error) {
    if sortBy == "" {
        return nil, ErrSortByNotSet
    }
    if algorithm == "" {
        return nil, ErrAlgorithmNotSet
    }

    switch algorithm {
    case "lowest":
        return selectLowestSortedNode(nodes, sortBy)
    case "twochoice":
        return selectTwoChoiceSortedNode(nodes, sortBy)
    default:
        return nil, ErrAlgorithmUnknown
    }
}

func selectTwoChoiceSortedNode(nodes []*livekit.Node, sortBy string) (*livekit.Node, error) {
    if len(nodes) <= 2 {
        return selectLowestSortedNode(nodes, sortBy)
    }
    node1, node2, err := selectTwoRandomNodes(nodes)
    if err != nil {
        return nil, err
    }
    return selectLowestSortedNode([]*livekit.Node{node1, node2}, sortBy)
}
```

**`RedisRouter.keepaliveWorker` — distributed node heartbeat** (`pkg/routing/redisrouter.go:161-183`)

```go
func (r *RedisRouter) keepaliveWorker(startedChan chan error) {
    pings, err := r.kps.SubscribePing(r.ctx, r.currentNode.NodeID())
    if err != nil {
        startedChan <- err
        return
    }
    close(startedChan)

    for ping := range pings.Channel() {
        if time.Since(time.Unix(ping.Timestamp, 0)) > r.nodeStatsConfig.StatsUpdateInterval {
            logger.Infow("keep alive too old, skipping", "timestamp", ping.Timestamp)
            continue
        }

        if !r.currentNode.UpdateNodeStats() {
            continue
        }

        if err := r.RegisterNode(); err != nil {
            logger.Errorw("could not update node", err)
        }
    }
}
```

**Wire-assembled server — complete dependency graph entry** (`pkg/service/wire_gen.go:19-100`, abbreviated)

```go
func InitializeServer(conf *config.Config, currentNode routing.LocalNode) (*LivekitServer, error) {
    universalClient, err := createRedisClient(conf)          // nil if no Redis
    messageBus := getMessageBus(universalClient)              // local or Redis bus
    router := routing.CreateRouter(universalClient, ...)      // LocalRouter or RedisRouter
    objectStore := createStore(universalClient)               // LocalStore or RedisStore
    roomAllocator, err := NewRoomAllocator(conf, router, objectStore)
    telemetryService := createTelemetryService(notifier, analyticsService)
    roomManager, err := NewLocalRoomManager(conf, objectStore, currentNode,
        router, roomAllocator, telemetryService, ...)
    rtcService := NewRTCService(conf, roomAllocator, router, telemetryService)
    livekitServer, err := NewLivekitServer(conf, roomService, ...,
        rtcService, ..., roomManager, signalServer, turnServer, currentNode)
    return livekitServer, nil
}
```
