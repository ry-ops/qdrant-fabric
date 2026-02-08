# Qdrant MCP Server - Complete API Coverage Plan

## Overview

This document outlines the complete Qdrant API surface that will be exposed through the MCP server, covering both Cloud Management and Database operations.

## API Surface Summary

### Cloud Management API (gRPC)
- **Protocol**: Protocol Buffers / gRPC
- **Source**: `qdrant-cloud-public-api` proto files
- **Total Services**: 20
- **Total RPC Methods**: 118
- **Base URL**: `https://cloud.qdrant.io/`

### Database API (REST)
- **Protocol**: REST / OpenAPI 3.0
- **Source**: Qdrant Database OpenAPI spec
- **Total Resource Groups**: 10
- **Total Operations**: 71
- **Base URL**: `https://{cluster-url}:6333/` or `https://{collection-url}:6333/`

### Combined Total
**189 operations** across both APIs

---

## Cloud Management API Breakdown

### 1. AccountService (17 methods)
Account lifecycle, invitations, and member management:
- ListAccounts, GetAccount, CreateAccount, UpdateAccount, DeleteAccount
- LeaveAccount, SuggestCompanies
- ListAccountInvites, GetAccountInvite, CreateAccountInvite, DeleteAccountInvite
- ListReceivedAccountInvites, AcceptAccountInvite, RejectAccountInvite
- ListAccountMembers, GetAccountMember, DeleteAccountMember

### 2. ClusterService (13 methods)
Managed cluster operations:
- ListClusters, GetCluster, CreateCluster, CreateClusterFromBackup
- UpdateCluster, DeleteCluster
- RestartCluster, SuspendCluster, UnsuspendCluster
- EnableClusterJwtRbac, SuggestClusterName
- ListQdrantReleases, GetQdrantRelease

### 3. IAMService (18 methods)
Identity, roles, and permissions:
- GetAuthenticatedUser, ListUsers, UpdateUser
- GetUserProfile, UpdateUserProfile
- GetUserConsent, RecordUserConsent
- ListPermissions, ListRoles, GetRole, CreateRole, UpdateRole, DeleteRole
- ListEffectivePermissions, ListUserRoles, ListRoleUsers
- AssignUserRoles, LogoutUser

### 4. BackupService (11 methods)
Backup and restore operations:
- ListBackups, GetBackup, CreateBackup, DeleteBackup
- ListBackupRestores, RestoreBackup
- ListBackupSchedules, GetBackupSchedule, CreateBackupSchedule
- UpdateBackupSchedule, DeleteBackupSchedule

### 5. PaymentService (9 methods)
Billing and payment methods:
- ListPaymentMethods, GetPaymentMethod, GetPaymentMethodAvailability
- CreatePaymentMethod, UpdatePaymentMethod, DeletePaymentMethod
- GetStripeCheckoutSession, CreateStripeCheckoutSession
- RecordCloudMarketplaceEntitlement

### 6. BookingService (7 methods)
Packages and pricing:
- ListPackages, GetPackage, ListGlobalPackages
- GetQuote, GetBackupQuote
- ListInferenceModels, ListStorageTierTypes

### 7. PlatformService (6 methods)
Cloud providers and regions:
- ListGlobalCloudProviders, ListCloudProviders
- ListGlobalCloudProviderRegions, GetGlobalCloudProviderRegion
- ListCloudProviderRegions, GetCloudProviderRegion

### 8. HybridCloudService (6 methods)
Hybrid cloud environments:
- ListHybridCloudEnvironments, GetHybridCloudEnvironment
- CreateHybridCloudEnvironment, UpdateHybridCloudEnvironment
- DeleteHybridCloudEnvironment, GenerateBootstrapCommands

### 9. DatabaseApiKeyService (6 methods)
Database API key management (v1 + v2):
- ListDatabaseApiKeys, CreateDatabaseApiKey, DeleteDatabaseApiKey (×2 for v1/v2)

### 10. MonitoringService (5 methods)
Cluster monitoring and metrics:
- GetClusterSummaryMetrics, GetClusterUsageMetrics
- GetClusterLogs, GetClusterEvents
- GetClusterInferenceMetrics

### 11. CollectionService (4 methods)
Serverless collections:
- ListCollections, CreateCollection
- UpgradeCollection, DeleteCollection

### 12. AuthService (3 methods)
Management API keys:
- ListManagementKeys, CreateManagementKey, DeleteManagementKey

### 13. CollectionApiKeyService (3 methods)
Serverless collection API keys:
- ListCollectionApiKeys, CreateCollectionApiKey, DeleteCollectionApiKey

### 14. BillingService (2 methods)
Invoices and discounts:
- ListInvoices, ListDiscounts

### 15. MeteringService (2 methods)
Usage metering:
- ListMonthlyMeterings, ListMeterings

### 16. QuotaService (2 methods)
Account quotas:
- GetAuthenticatedUserQuotas, GetAccountQuotas

### 17. AggregationService (1 method)
UI optimization endpoints:
- ListUsersWithRoles

### 18. ClusterDataService (1 method)
UI cluster data (beta):
- ListCollections

### 19. EphemeralDashboardTokenService (1 method)
Dashboard access:
- CreateEphemeralDashboardToken

### 20. FeatureFlagsService (1 method)
Feature flags:
- GetFeatureFlags

---

## Database API Breakdown

### 1. Collections (55 operations)
Core vector database operations:

**Collection Management (6)**
- GET /collections - List all collections
- PUT /collections/{name} - Create collection
- GET /collections/{name} - Get collection info
- DELETE /collections/{name} - Delete collection
- PATCH /collections/{name} - Update collection
- GET /collections/{name}/exists - Check if collection exists

**Point Operations (21)**
- PUT /points - Upsert points
- POST /points - Get points by IDs
- GET /points/{id} - Get single point
- POST /points/delete - Delete points
- POST /points/count - Count points
- POST /points/scroll - Scroll through points
- POST /points/search - Vector search
- POST /points/search/batch - Batch vector search
- POST /points/search/groups - Search with grouping
- POST /points/search/matrix/offsets - Matrix search offsets
- POST /points/search/matrix/pairs - Matrix search pairs
- POST /points/recommend - Recommendation
- POST /points/recommend/batch - Batch recommendation
- POST /points/recommend/groups - Group recommendations
- POST /points/discover - Discover points
- POST /points/discover/batch - Batch discovery
- POST /points/query - Universal query endpoint
- POST /points/query/batch - Batch queries
- POST /points/query/groups - Query with grouping
- POST /points/facet - Faceted search
- POST /points/batch - Batch updates

**Payload Operations (5)**
- POST /points/payload - Set payload
- PUT /points/payload - Overwrite payload
- POST /points/payload/clear - Clear payload
- POST /points/payload/delete - Delete payload fields

**Vector Operations (2)**
- PUT /points/vectors - Update vectors
- POST /points/vectors/delete - Delete vectors

**Index Management (2)**
- PUT /index - Create field index
- DELETE /index/{field_name} - Delete field index

**Cluster Operations (2)**
- GET /cluster - Collection cluster info
- POST /cluster - Update collection cluster

**Aliases (2)**
- GET /aliases - Get collection aliases
- POST /aliases - Update aliases (global)

**Shard Management (5)**
- GET /shards - List shard keys
- PUT /shards - Create shard key
- POST /shards/delete - Delete shard key

**Collection Snapshots (5)**
- GET /snapshots - List snapshots
- POST /snapshots - Create snapshot
- GET /snapshots/{name} - Get snapshot
- DELETE /snapshots/{name} - Delete snapshot
- PUT /snapshots/recover - Recover from snapshot
- POST /snapshots/upload - Recover from uploaded snapshot

**Shard Snapshots (5)**
- GET /shards/{id}/snapshots - List shard snapshots
- POST /shards/{id}/snapshots - Create shard snapshot
- GET /shards/{id}/snapshots/{name} - Get shard snapshot
- DELETE /shards/{id}/snapshots/{name} - Delete shard snapshot
- PUT /shards/{id}/snapshots/recover - Recover shard
- POST /shards/{id}/snapshots/upload - Recover from upload

**Optimization (1)**
- GET /optimizations - Get optimization status

### 2. Cluster (3 operations)
Cluster-wide management:
- GET /cluster - Cluster status
- DELETE /cluster/peer/{peer_id} - Remove peer
- POST /cluster/recover - Recover current peer

### 3. Snapshots (4 operations)
Full database snapshots:
- GET /snapshots - List full snapshots
- POST /snapshots - Create full snapshot
- GET /snapshots/{name} - Get full snapshot
- DELETE /snapshots/{name} - Delete full snapshot

### 4. Health & Monitoring (6 operations)
System health and metrics:
- GET / - Root endpoint
- GET /healthz - Health check
- GET /livez - Liveness probe
- GET /readyz - Readiness probe
- GET /metrics - Prometheus metrics
- GET /telemetry - Telemetry data

### 5. Issues (2 operations)
Issue tracking:
- GET /issues - List issues
- DELETE /issues - Clear issues

### 6. Aliases (1 operation)
Global alias management:
- GET /aliases - Get all collection aliases

---

## Tool Naming Convention

### Format
`qdrant_{api}_{resource}_{action}`

### Examples

**Cloud Management API:**
- `qdrant_cloud_clusters_list` - List clusters
- `qdrant_cloud_clusters_create` - Create cluster
- `qdrant_cloud_clusters_get` - Get cluster details
- `qdrant_cloud_backups_schedule_create` - Create backup schedule
- `qdrant_cloud_iam_roles_assign` - Assign IAM role

**Database API:**
- `qdrant_db_collections_list` - List collections
- `qdrant_db_collections_create` - Create collection
- `qdrant_db_points_upsert` - Upsert points
- `qdrant_db_points_search` - Search vectors
- `qdrant_db_points_recommend` - Get recommendations
- `qdrant_db_snapshots_create` - Create snapshot

### Resource Categories
- `collections` - Collection management
- `points` - Vector point operations
- `search` - Search operations (search, recommend, discover, query)
- `payload` - Payload management
- `vectors` - Vector operations
- `index` - Index management
- `shards` - Shard management
- `snapshots` - Snapshot operations
- `cluster` - Cluster operations
- `health` - Health checks

---

## Implementation Phases

### Phase 1: Core Database Operations (Priority: HIGH)
**Target: 30 tools**
- Collections CRUD (6 tools)
- Points CRUD (10 tools)
- Vector Search (4 tools: search, search_batch, recommend, recommend_batch)
- Payload operations (5 tools)
- Health checks (5 tools)

### Phase 2: Cloud Management Essentials (Priority: HIGH)
**Target: 25 tools**
- Cluster management (13 tools)
- Account management (10 tools)
- Authentication (2 tools: get user, list management keys)

### Phase 3: Advanced Search & Discovery (Priority: MEDIUM)
**Target: 20 tools**
- Advanced search (query, query_batch, discover, facet)
- Search grouping and matrix operations
- Recommendation groups

### Phase 4: Backup & Recovery (Priority: MEDIUM)
**Target: 20 tools**
- Backup service (11 tools)
- Snapshot operations (9 tools: collection + full DB)

### Phase 5: IAM & Security (Priority: MEDIUM)
**Target: 30 tools**
- IAM service (18 tools)
- API key management (9 tools)
- Role management

### Phase 6: Infrastructure & Monitoring (Priority: LOW)
**Target: 25 tools**
- Monitoring service (5 tools)
- Platform service (6 tools)
- Hybrid cloud (6 tools)
- Metering & quotas (4 tools)
- Issues (2 tools)
- Cluster operations (2 tools)

### Phase 7: Billing & Platform (Priority: LOW)
**Target: 20 tools**
- Payment service (9 tools)
- Billing service (2 tools)
- Booking service (7 tools)
- Feature flags (1 tool)
- Dashboard tokens (1 tool)

### Phase 8: Advanced Operations (Priority: LOW)
**Target: 19 tools**
- Shard management (8 tools)
- Vector operations (2 tools)
- Index management (2 tools)
- Aliases (3 tools)
- Optimization (1 tool)
- Telemetry (1 tool)
- Serverless collections (4 tools)

---

## Authentication Strategy

### Cloud Management API
- Bearer token from Qdrant Cloud
- Environment variable: `QDRANT_CLOUD_API_KEY`
- Header: `Authorization: Bearer <token>`

### Database API
- API key per cluster/collection
- Environment variable: `QDRANT_API_KEY`
- Header: `api-key: <key>`
- Alternative: JWT tokens with RBAC (for clusters with JWT enabled)

### Configuration Priority
1. Environment variables (for deployment)
2. MCP server initialization parameters (for testing)
3. Per-request overrides (for multi-tenancy)

---

## Project Structure

```
qdrant-mcp/
├── README.md
├── pyproject.toml
├── src/
│   └── qdrant_mcp/
│       ├── __init__.py
│       ├── server.py          # MCP server entrypoint
│       ├── config.py          # Configuration management
│       ├── cloud/             # Cloud Management API
│       │   ├── __init__.py
│       │   ├── client.py      # gRPC client
│       │   ├── accounts.py    # Account tools
│       │   ├── clusters.py    # Cluster tools
│       │   ├── backups.py     # Backup tools
│       │   ├── iam.py         # IAM tools
│       │   ├── monitoring.py  # Monitoring tools
│       │   └── ...
│       └── database/          # Database API
│           ├── __init__.py
│           ├── client.py      # REST client
│           ├── collections.py # Collection tools
│           ├── points.py      # Point tools
│           ├── search.py      # Search tools
│           ├── snapshots.py   # Snapshot tools
│           └── ...
├── tests/
│   ├── test_cloud/
│   └── test_database/
└── docs/
    ├── API_COVERAGE_PLAN.md  # This file
    ├── cloud_api_surface.txt
    └── database_api_operations.txt
```

---

## Next Steps

1. ✅ Extract Cloud Management API surface (118 methods)
2. ✅ Extract Database API surface (71 operations)
3. ⏳ Design tool naming convention
4. ⏳ Create project structure
5. ⏳ Implement Phase 1: Core Database Operations
6. ⏳ Implement Phase 2: Cloud Management Essentials
7. ⏳ Add comprehensive tests
8. ⏳ Add documentation and examples
9. ⏳ Implement remaining phases incrementally

---

## Success Metrics

- **Coverage**: All 189 operations exposed as MCP tools
- **Testing**: >80% code coverage
- **Documentation**: Every tool has description + examples
- **Performance**: <100ms p95 latency for simple operations
- **Reliability**: Error handling for all API failure modes
