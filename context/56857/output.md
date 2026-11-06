# Apex Gateway blue-green routing — 2026-11-06

**Participants:** Vincent Wang (SPEAKER_1, presenter, inferred), Geoff Li (SPEAKER_0, listener, inferred).
**Duration:** 00:18:20
**Recording:** `~/.recordings/2026-11-06-apex-gateway-bluegreen-routing/`
**Sources:** transcript merged from Gemini and whisper.cpp; 28 screenshots (IMG_8680–8707); JIRA screenshot TREATRANS-56857; post-call update from Geoff.
**Speaker labels:** inferred from content, not measured. Gemini diarization collapsed (spk_1 = 98% of speech). See `transcript.md` header.

> ASR quality degraded [00:09:35]–[00:10:55] and [00:12:24]–[00:13:50]: many filler words and broken sentences. Claims from these ranges are lower confidence.

## Outcome

Vincent explained the current gateway routing. The team agreed to add a simple blue-green API on top of the existing gateway API. The core scope is `register` (create a blue and a green route from one existing route) and `swap` (exchange the blue and green URLs). `remove` is optional. The API design is not final. Geoff owns the JIRA task (TREATRANS-56857). Geoff researches Spring Cloud Gateway and sets up a local run. Vincent is on leave next Monday.

## Decisions

| Decision | Owner | Rationale | At |
|---|---|---|---|
| Build `register` and `swap` APIs first. `remove` is optional. | unstated (proposed by Vincent) | "最主要是前面两个" | [00:12:27] |
| Store blue-green routes in Redis (dynamic), not in static config | unstated | Static routes reset on restart. Redis routes persist. | [00:05:00] |
| Blue and green routes use header predicate `x-blue-green-tag` (value `blue` or `green`) | proposed by Vincent | Header selects the group. Name from screenshot. | [00:07:56], IMG_8694/8696 |
| Simplify the request body to one existing route ID and two URLs | proposed by Vincent | Current batch body is "很复杂" | [00:11:44]–[00:12:13] |
| Local tests use a Redis database number above 5. Avoid DB 5 (normal dev). | Vincent (post-call) | Avoid disrupting normal dev operations | [00:14:00]–[00:14:54], post-call update |

## Action items

- [ ] Research Spring Cloud Gateway route definitions and actuator route endpoints — owner: Geoff, due: today (Geoff's words), at [00:15:50]
- [ ] Draft the simplified `register` / `swap` / optional `remove` API design — owner: Geoff, due: unstated, at [00:07:56]
- [ ] Set up the local run (Redis DB above 5, DB config) — owner: Geoff, due: unstated, at [00:14:00]
- [ ] Create a test branch that the Cloud Build trigger deploys — owner: Geoff, due: unstated, at [00:16:13]
- [ ] Send setup materials for running the gateway locally — owner: Vincent, due: unstated, at [00:17:24]
- [ ] Hold a follow-up meeting on the API design — owner: unstated, due: before Vincent's leave next Monday (inferred), at [00:13:49] ⚠ date not set

## My commitments

Only items Geoff owns. Geoff is now the JIRA assignee for TREATRANS-56857 (post-call update).

- [ ] Study Spring Cloud Gateway route docs and the actuator routes endpoint — due: today, at [00:15:50]
- [ ] Draft the simplified blue-green API design (`register`, `swap`, optional `remove`) — due: unstated, at [00:07:56]. Next week is acceptable (post-call update).
- [ ] Set up the gateway locally with a Redis DB above 5 and matching DB config — due: unstated, at [00:14:00]
- [ ] Create a branch for a test deploy (Cloud Build trigger) — due: unstated, at [00:16:13]

## Blocked / waiting on others

- Design details — waiting on the follow-up meeting with Vincent, at [00:13:49]
- Local setup materials — waiting on Vincent, at [00:17:24]
- Vincent is on leave next Monday. Plan the follow-up meeting around that date (post-call update).

## Open questions

- Final `order` values for blue and green. Vincent gave an example of both at -1 to give the endpoint higher priority. The design is not final (post-call update). Route JSON on screen shows blue = -2, green = -1 (IMG_8691/8692). Low impact for now.
- Exact header name. Screenshots show `x-blue-green-tag` (IMG_8694/8696) and one frame shows `X-Stable-Fallback-From` (IMG_8693). Confirm in the design.
- Which Cloud Build branch names map to which environment. Vincent says "只有一到五有环境". — [00:17:00] ⚠

## Resolved after call

- **Task owner:** Geoff Li. The JIRA assignee changed from Vincent Wang to Geoff Li after the call (Geoff's update).
- **Redis DB for local tests:** use a number above 5 and avoid 5. Vincent's suggestion (Geoff's update). The earlier "2 vs 3" conflict no longer applies.
- **Deadline:** next week is acceptable. Vincent is on leave next Monday (Geoff's update).
- **Leader name ("⚠Belwin"):** Geoff says it is not important. Not tracked further.
- **6 PM approval item:** out of scope for this task. Not tracked (Geoff's update).

## Numbers, dates, and names

- Redis in `application-local.yml`: port **6378**, database **5**. Avoid DB 5 for local tests. — IMG_8702
- Route IDs: `entitlement-service-blue` (order **-2**), `entitlement-service-green` (order **-1**). Path `/entitlement-service/{*segment}`. — IMG_8691/8692
- Blue URI: `user-entitlement-service-fe-1`. Green URI: `user-entitlement-service-fe-3`. — IMG_8691/8692
- Fallback path: `/fallback/entitlement-service-stable-proxy-from-gcp-to-hic/{segment}`. — IMG_8692
- Retry: retries 2, backoff 2000 ms, factor 2. Circuit breaker status codes 500, 502, 503, 504. — IMG_8691/8692
- Header predicate: `x-blue-green-tag` = `green` (or `blue`). — IMG_8694/8696
- Existing API endpoints (from the HTTP files): `GET /actuator/gateway/routes`, `POST /actuator/gateway/routes`, `DELETE /apex-gateway/route/routes/{id}`, `POST /apex-gateway/route/refresh`. — IMG_8689/8690
- JIRA TREATRANS-56857: "Implement register, swap, and remove APIs for blue-green routing in gateway service". Status OPEN. Assignee: Vincent Wang at the call, now Geoff Li. — IMG_8699–8701 + post-call update
- Related JIRA: TREATRANS-51922 (Devin Luo, IN PROGRESS); TREATRANS-56518 "Deploy entitlement-ui to slot 2" (Devin Luo, OPEN). — IMG_8699
- Cloud Build trigger branch rule: `^feature/TREATRANS-(0000|[1-5]|4322|4323|53326|54146|12345)_.+$`. Matches 15 branches. — IMG_8705–8707
- Repo: `ecosystem-gateway-service`, branch `feature/TREATRANS-54146_jdk_25`. — IMG_8680

## Follow-up needed

- Confirm the final blue and green `order` values in the design.
- Confirm the header name (`x-blue-green-tag` vs. the other name in IMG_8693).
- Confirm which Cloud Build branch names deploy to which environment before you create a test branch.
- Set a date for the follow-up design meeting before Vincent's leave next Monday.
- Ask Vincent for the setup materials he offered at [00:17:24].
- Re-check the ASR-degraded ranges against the audio if you quote them.
