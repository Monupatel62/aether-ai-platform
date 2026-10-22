# Aether AI — Data Infrastructure Evaluation

**Research date:** 2026-10-22  
**Status:** options analysis; no vendor or database choice has been accepted.  
**Scope:** transactional database, vector retrieval, durable job queue, cache, and search. A logical repository does not automatically imply a separately deployed service.

## Executive recommendation

For an initial, cost-conscious TypeScript product, evaluate **PostgreSQL as the transactional system of record**, with PostgreSQL full-text search and **pgvector** as the first retrieval baseline. Add a separate vector service only if measured corpus size, query latency, filtering/recall, indexing throughput, or operational requirements justify it. Evaluate **BullMQ with a Redis-compatible backend** for the first Node.js job-queue spike, while comparing **NATS JetStream** if Aether needs replayable event streams, multiple independent consumers, and cross-service messaging. Use cache only for reconstructible, short-lived data; do not use it as the durable source of truth for agent runs, billing, permissions, or audit records.

This is a **proposed starting point**, not an accepted final stack. Hosted-provider capabilities, costs, backup/restore, deployment environment, tenant count, workload, and license terms still need validation.

## 1. Transactional database

### Candidate: PostgreSQL

PostgreSQL is the leading candidate for durable product state: users/tenants, sessions and configuration, conversation metadata, file/knowledge metadata, billing ledger records, run state, audit metadata, and job/outbox records. It provides transactions, relational constraints, indexing, full-text search, and mature backup/PITR options.

Official evidence:
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html): row-level policies can restrict row visibility and modifications, but owners/superusers/BYPASSRLS roles may bypass policies. RLS is defense-in-depth, not a replacement for application authorization and role design.
- [PostgreSQL continuous archiving/PITR](https://www.postgresql.org/docs/current/continuous-archiving.html): base backups plus WAL archives can support recovery to a selected point in time; this needs an operated and tested backup plan.
- [PostgreSQL full-text search](https://www.postgresql.org/docs/current/textsearch-intro.html): linguistic normalization and ranked text matching are available.

### Requirements before accepting

- Define authoritative ownership of every table/domain; do not let all 33 repositories share arbitrary tables.
- Use explicit migrations, forward/backward compatibility policy, connection pooling, least-privilege service roles, and separate migration credentials.
- Tenant scoping must be explicit in queries and authorization checks. If RLS is used, test under the real non-owner runtime role and test pooled-connection context reset; never rely on RLS with a superuser/bypass role.
- Define encryption, secrets handling, data residency, retention/deletion, export, backup frequency, RPO/RTO, PITR, restore drills, and incident access.
- Treat billing ledger and audit history as durable append-oriented records with integrity/access controls; cache is never authoritative for them.
- Define an outbox/inbox or equivalent transactional event pattern so committing a state change and publishing its event cannot silently diverge.

### Alternative

A different relational database should be considered only if deployment/provider constraints or a documented workload show PostgreSQL is unsuitable. Avoid selecting a database solely because an ORM supports it.

## 2. Vector retrieval and search

### Baseline: PostgreSQL + pgvector + PostgreSQL full-text search

[pgvector](https://github.com/pgvector/pgvector) supports exact nearest-neighbor search and approximate HNSW/IVFFlat indexes, multiple distance metrics, and integration with ordinary SQL data. PostgreSQL full-text search can provide lexical search; the RAG layer can combine lexical and vector candidates and rerank them.

Trade-offs:
- One data platform and SQL authorization path can reduce operational complexity early.
- HNSW trades additional memory/build cost for search performance; IVFFlat has different build/memory/recall trade-offs. Exact search should remain the evaluation baseline for recall.
- Approximate index filtering can return fewer matching rows than expected; test with real tenant filters and compare against exact search. pgvector documents partitioning/separate tables as options where multi-tenant approximate-index interference affects recall.
- Extension availability and version must be verified on the chosen managed PostgreSQL provider.

### Separate vector database candidate: Qdrant

[Qdrant multitenancy documentation](https://qdrant.tech/documentation/manage-data/multitenancy/) describes payload-filter partitioning, dedicated shards, and tiered tenancy. This can be useful for larger vector workloads or specialized indexing needs, but tenant filters still must be mandatory and tested in the application; the vector store is not the authority for user permissions.

### Decision rule

Start with pgvector unless a representative benchmark proves it misses required latency, throughput, recall, filter, indexing, or operational targets. Evaluate Qdrant (or another dedicated vector store) with identical data, embedding model, tenant filters, deletion cases, and recall metrics. Do not select a vector engine before the embedding model and chunking strategy are chosen, because dimensions, cost, and retrieval quality depend on them.

### Retrieval acceptance tests

- Compare vector and lexical retrieval against a labeled evaluation set, measuring recall@k, precision/nDCG where applicable, latency and cost.
- Verify every chunk carries tenant, source, document/version, ACL and deletion metadata as appropriate.
- Test cross-tenant and revoked-access queries, file deletion, reindexing, stale embeddings, duplicate chunks and partial indexing failures.
- Verify search filters are applied before results leave the retrieval boundary and before model context is assembled.
- Define embedding version/dimension migration and backfill behavior.

## 3. Durable queue and event transport

### Candidate A: BullMQ

[BullMQ](https://docs.bullmq.io/) is a Node.js queue built on Redis. Its documented features include delayed jobs, concurrency, retries/backoff, job dependencies and rate limiting. It is a reasonable first candidate for Aether's TypeScript worker ecosystem.

Important limits:
- Job processing can be redelivered after failures; job handlers must be idempotent and side effects must use idempotency keys or a reconciliation protocol.
- The queue is not the authoritative durable run-state database. Store run state, step/checkpoint status, approvals, and terminal outcomes in the database under orchestration ownership.
- Redis-compatible backend compatibility, persistence, failover, memory policy and managed-service support must be verified for the chosen BullMQ version.
- Avoid placing full prompts, files, secrets or large outputs in queue payloads; send opaque IDs and fetch data through authorized APIs.

### Candidate B: NATS JetStream

[NATS JetStream](https://docs.nats.io/concepts/jetstream) adds persistent streams, replay, durable consumers and acknowledgement/redelivery on top of NATS. It is attractive if Aether needs event fan-out, independent consumers, replay, and cross-service messaging beyond a work queue.

Important limits:
- At-least-once delivery means consumers still need idempotency. Acknowledgement and storage configuration affect durability.
- JetStream is another service to operate and monitor. Document replication, retention, disk capacity, backup/recovery and security before production.
- Use bounded messages and object references for large content.

### Decision rule

Use BullMQ for the first worker-queue spike if the workload is primarily Node.js job processing and a Redis-compatible backend is acceptable. Prefer JetStream only if the proof-of-concept shows that persistent replay, independent durable consumers, or event fan-out is a real requirement. Do not operate both by default. The orchestration contract must be broker-neutral enough to test recovery and idempotency, but do not create an elaborate generic messaging abstraction without a second backend need.

### Queue acceptance tests

- Crash a worker before side effect, during side effect, and after side effect but before acknowledgment; prove no duplicate irreversible action occurs.
- Test delayed/retried jobs, dead-letter/manual recovery, cancellation, backpressure, poison messages, worker rolling deploys and broker restart.
- Verify durable run state reconciles with queue state after a crash or lost event.
- Use transactional outbox/inbox or equivalent for database-to-queue event publication.
- Confirm tenant fairness, per-provider rate limits, queue quotas, and that job payloads contain no secrets or full prompt content by default.

## 4. Cache

### Candidate: Valkey or another managed Redis-compatible cache

[Valkey](https://github.com/valkey-io/valkey) is an open-source in-memory datastore under the BSD 3-Clause license, with roots in Redis 7.2.4. Redis licensing differs by release; [Redis licensing information](https://redis.io/about/) currently describes RSALv2 or SSPLv1 for the Redis product page. Review the exact server and managed service license, not just client-library license, before choosing.

Use cache only for reconstructible data: short-lived rate-limit counters, model capability/catalog snapshots, transient coordination, and safe response caches where privacy rules permit. Define TTL, eviction, namespace, tenant-keying, invalidation, memory budget and outage behavior. Do not cache private responses without a complete key that includes the authorization scope and relevant data version.

Cache is not the source of truth for sessions, billing, permissions, audit history, durable run state, or approvals unless a separately reviewed design proves the required durability and recovery properties.

## 5. Search service

Do not create a dedicated search deployment merely because a repository exists. Start with a search interface implemented using PostgreSQL full-text search and pgvector hybrid retrieval. Keep query parsing, ranking policy and authorization in Aether's search/RAG contracts. Add OpenSearch or another search engine only after benchmark evidence shows requirements such as high-volume indexing, specialized analyzers, aggregations, independent scaling or operational separation cannot be met economically by PostgreSQL.

If a dedicated engine is later selected, its index is a derived/rebuildable projection. The authoritative source remains the database/files/knowledge domain; support versioned indexing, replays, deletion tombstones, backfill, and authorization-aware query filters.

## 6. Proposed initial architecture (not accepted)

| Capability | Initial candidate | Authority / boundary | Exit trigger |
|---|---|---|---|
| Transactional data | PostgreSQL | Database repository defines migrations/contracts; domain owners own their schemas and data | Measured workload, provider constraint or availability target disproves fit |
| Vector search | pgvector | RAG/search owns retrieval; source ACLs and tenant permissions remain authoritative outside vector index | Recall/latency/indexing/scale benchmark fails target |
| Lexical search | PostgreSQL full-text | Search contract; index is rebuildable | Analyzer, indexing or query performance requirement exceeds fit |
| Background jobs | BullMQ spike | Orchestration owns durable run state; queue carries opaque job IDs | Need for durable replay/event fan-out or BullMQ/backend fails recovery tests |
| Cache | Valkey-compatible cache candidate | Reconstructible data only; no source-of-truth records | Provider license/operations or measured workload changes decision |
| Object/file bytes | Separate object-storage adapter, provider undecided | Files repository owns metadata/lifecycle; object storage holds bytes | Select after retention, region, signed URL, scanning and cost requirements are clear |

## 7. Decisions deliberately left open

- Managed vs self-hosted PostgreSQL, provider, region and data residency.
- Exact PostgreSQL and pgvector versions/extensions.
- BullMQ backend vs NATS JetStream and queue topology.
- Valkey vs another cache and exact managed-service license/compatibility.
- pgvector vs Qdrant or a dedicated search engine after benchmark.
- Object storage vendor and malware/content scanning pipeline.
- RPO/RTO, retention, tenant isolation model, per-tenant quotas, expected tenant/data volume and cost ceilings.

## 8. Sources

- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [PostgreSQL point-in-time recovery](https://www.postgresql.org/docs/current/continuous-archiving.html)
- [PostgreSQL full-text search](https://www.postgresql.org/docs/current/textsearch-intro.html)
- [pgvector README](https://github.com/pgvector/pgvector)
- [Qdrant multitenancy](https://qdrant.tech/documentation/manage-data/multitenancy/)
- [BullMQ queues](https://docs.bullmq.io/guide/queues/)
- [BullMQ retries](https://docs.bullmq.io/guide/retrying-failing-jobs)
- [BullMQ rate limiting](https://docs.bullmq.io/guide/rate-limiting)
- [NATS JetStream](https://docs.nats.io/concepts/jetstream)
- [Valkey project/license](https://github.com/valkey-io/valkey)
- [Redis licensing/product information](https://redis.io/about/)
