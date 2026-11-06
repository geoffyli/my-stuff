# Screenshots — 2026-11-06 meeting (IMG_8680–IMG_8707)

Resized previews: `screenshots/` (IDs match `~/Downloads/IMG_XXXX.JPG`).
Frames came back in batches. The IDs below are grouped by topic and are
verified by content. Exact frame-to-ID mapping inside a range may be off by one.
Check the original file before you quote a single ID.

| IDs | Shows | Key facts |
|---|---|---|
| 8680–8681 | Meeting tiles + IDE route tree | Tiles: **Geoff Li** (left), **Vincent Wang** (right). Route folder `doc/http/route/`. |
| 8682–8684 | `entitlement_weight_route.http`; `workflow` / `apex-workflow` search | Clock 10:35. `GET …/actuator/gateway/routes`, `POST …/apex-gateway/route/refresh`. Routes `apex-workflow-service`, URI `…apex-workflow-service-fe-2…:80`. |
| 8685 | Spring Cloud Gateway WebFlux docs (5.0.4) | Clock 10:36. |
| 8686–8688 | `application-common.yaml` | Static routes (`orchestration-service`, `product-info-service`, …). `redis-route-definition-repository: enabled: true`. Banner "Vincent Wang's screen" (8686). |
| 8689 | `stage_1_hic_backup_route.json` | Route `entitlement-service-gcp-order`. |
| 8690 | `run_api_dev.yaml` | DELETE `/apex-gateway/route/routes/entitlement-service-gcp-order`; DELETE `…entitlement-service-stable-proxy-from-gcp-to-hic`; POST `/actuator/gateway/routes` (body `DEV/stage_2_bidirectional_header_backup_route.json`); POST `/apex-gateway/route/refresh`. |
| 8691 | `stage_1_hic_backup_route.json` | Route `entitlement-service-blue`, order **-2**, URI `user-entitlement-service-fe-1`, Path `/entitlement-service/{*segment}`, Retry 2 × 2000 ms. |
| 8692 | Same file, lines 29–57 | CircuitBreaker `statusCodes` 500, 502, 503, 504; fallback `forward:/fallback/entitlement-service-stable-proxy-from-gcp-to-hic/{segment}`. Route `entitlement-service-green`, order **-1**, URI `user-entitlement-service-fe-3`. |
| 8693 | Same file, lines 44–71 | Green Header predicate name shows `X-Stable-Fallback-From` (highlighted). RewritePath `/fallback/…/` → `/${remaining}`. PreventLoop filter. |
| 8694 | Same file | Green Header predicate: `x-blue-green-tag` = `green`. RewritePath with `(?<remaining>…)`. |
| 8695–8696 | `entitlement_weight_route.http` | Tests with header `x-blue-green-tag: green` (line 253). Version v2 test. Upsert `entitlement-service-weight` (50% → backend v1). |
| 8697–8698 | `apex-workflow` search (1/5, 5/5) | Routes `apex-workflow-service` (retries 2) and `apex-product-service`. |
| 8699–8701 | JIRA epic list (TREATRANS) | **TREATRANS-56857** "Implement register, swap, and remove APIs for blue-green routing in gateway service" — OPEN — assignee **Vincent Wang**. Related: 51922 (Devin Luo, IN PROGRESS), 56518 "Deploy entitlement-ui to slot 2" (Devin Luo, OPEN), 51924 (Kun Lun Yang). |
| 8702–8703 | `application-local.yml`; `redis.http` | Redis `port: 6378`, `database: 5`, `client-type: lettuce`. Postgres datasource (`network-bridge-dev…:10008/gateway`). `redis.http`: `GET/POST /apex-gateway/v1/redis/k1`. |
| 8704 | `GET …/actuator/gateway/routes` on `apex-gateway-dev2` | HTTP/2 200. Clock 11:17. |
| 8705–8707 | Cloud Build triggers (europe-west2); trigger edit | Branch regex `^feature/TREATRANS-(0000|[1-5]|4322|4323|53326|54146|12345)_.+$`. Matches 15 branches. |

Clock values seen: 10:35 (8682), 10:36 (8685), 11:17 (8704).
