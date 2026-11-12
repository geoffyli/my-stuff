# Apex Gateway blue-green 路由 API：进展对齐 — 2026-11-12

**参与者：** Devin（主持人 / 评审，推断）、Geoff（实现与演示）、Vincent（技术评审，推断）
**时长：** 00:25:04
**录音：** `~/.recordings/2026-11-12-bluegreen-gateway-api-alignment/`
**转写质量：** 三路交叉（Gemini 主转写 + 两段尾段补转 + 四次定点复听 + 本地 whisper 全文与短切片）。
**说话人：** 声纹不可用（原始标签塌缩），归属为按内容推断；Devin / Vincent 的归属见 `transcript.md` 的"说话人"一节。
**配套材料：** `~/Downloads/IMG_8787–8797.JPG`（11 张，已读）。
> ASR 降级区间：[00:12:15]–[00:14:05]（权限控制 / 白名单 / Ansible 讨论，四路都吞词）；[00:24:31]–[00:25:04]（仅致别语）。这两段的引用需回听原文。
> 未能还原的术语：⚠ "12345"、"N-1"、默认 tag 值（听作 proven / groove-in）、slot/subscriber、"双活 GP 和 IC"、"ignore whitelist"。

## 结论

Geoff 演示了已部署在 **gateway infra dev** 的 blue-green 路由 API。四个动作都跑通了：`register`、`query/status`（含 routes 列表）、`swap`、`remove`。实现方式是约定一个 header（`x-active-slot`）加两个 tag 值（`fe-1` / `fe-2`），gateway 侧从 context 补全未提供的 header。[00:00:26] [00:02:40]

评审结论是**方案可行、可以继续**，但要动三件事：把 change 放到 ⚠ N-1 环境并做一套 N-1 的 setup（Devin 负责联系）、默认 tag 值要改、权限控制沿用现有白名单机制而不是新做。[00:07:28] [00:12:25]

上线方式是**渐进分流 + 一键回切**：先部署新的一套拿到新 route；等前端改完能发 header；再把部分用户分到 green；出错就全部走回 blue。切换前确认过：这一段前面没有任何有状态的东西，所以切换没有状态丢失风险。[00:15:09] [00:16:47]

最后 Devin 会把 Geoff 手上那个 story **拆成 register / swap / remove 三个 story**，testing 另起一个 ticket，然后发给 Geoff。会议结束时状态是**先暂存（parked）**，等 Geoff 的消息，今天再确认时间。[00:22:43] [00:23:39] [00:24:52]

## 决策

| 决策 | 负责人 | 理由 | 时间 |
|---|---|---|---|
| blue-green 用约定 header（`x-active-slot`）+ 两个 tag 值实现，gateway 侧补全缺省 header | Geoff（实现），评审通过 | 前端只需改一次发 header 的逻辑 | [00:00:26] |
| 参数都设默认值：metadata 里的 blue-green、role、blue tag、green tag 不传也有默认 | Geoff | 调用方可以只传必需参数 | [00:05:14] |
| blue 沿用原始路由 URI 作为默认 slot，green 是新 slot | Devin + Geoff | 减少对现有路由的改动 | [00:10:00] |
| 权限控制不新做，沿用 gateway 现有白名单（配在 Ansible template / application core） | Devin | 现有机制已经这样用 | [00:12:25] |
| 上线采用渐进分流，先部署新 route，再等前端，再分批把用户分到 green；出错全量回切 blue | Geoff（方案），Devin 认可 | 全程有回退路径 | [00:15:09] |
| 路由切换可以按批做，不强制在同一个 window 内一次做完 | Geoff | 有先后顺序，测试难限制在单个 window | [00:18:00] |
| 把 Geoff 手上那个 story 拆成 register / swap / remove 三个 story，testing 另起 ticket | Devin 拆，Vincent 同意 | 便于拆分与跟踪 | [00:23:39] |
| 先暂存，等 Geoff 消息后再定时间 | Devin | 时间未定 | [00:24:12] |

## 行动项

- [ ] 按评审意见改代码：默认 tag 值、`headerName`、参数默认处理 — owner: Geoff, due: unstated, at [00:07:53] [00:08:18]
- [ ] 改完后部署到 dev，再放 ⚠ N-1 环境 — owner: Geoff, due: unstated, at [00:07:49]
- [ ] 联系 ⚠ N-1 那边，做一套 N-1 的 setup — owner: Devin, due: unstated, at [00:07:28]
- [ ] 把 change 放到 ⚠ "12345"（疑为某个 ticket / 环境） — owner: unstated, at [00:07:33]
- [ ] 拆 story：register / swap / remove 三条 + testing 一条，发给 Geoff — owner: Devin, due: unstated, at [00:22:43] [00:23:52]
- [ ] 补测试 case 到测试 ticket — owner: Geoff, due: unstated, at [00:21:56]
- [ ] 把 UI 配置里的账号 / 白名单放到群里共享 — owner: Devin, due: unstated, at [00:14:20]
- [ ] 今天再确认一次时间安排 — owner: Devin, due: 今天, at [00:24:52]

## 我的承诺（Geoff）

- [ ] 改代码：默认 tag 值、`headerName`、参数缺省处理 — due: unstated, at [00:07:53] [00:08:18]
- [ ] 部署到 dev，再放 ⚠ N-1 — due: unstated, at [00:07:49]
- [ ] 清理 POC 代码后合并（"我在做那个清理，今天把 POC 的东西去掉就可以上"）— due: 今天, at [00:11:41]
- [ ] 补测试 case — due: unstated, at [00:21:56]
- [ ] 给出上线顺序指引：先切哪部分、再切哪部分 — due: unstated, at [00:18:39]
- [ ] 会后发消息给 Devin（"等 Jeff 的消息"）— due: 今天, at [00:24:52]

## 阻塞 / 等待他人

- 前端要能发送指定的 header，blue-green 分流才会真正生效 — waiting on 前端改动, at [00:15:09]
- ⚠ N-1 环境的 setup 与联系人 — waiting on Devin, at [00:07:28]
- story 拆分与 ticket 创建 — waiting on Devin, at [00:22:30]
- UI 配置的账号清单 — waiting on Devin（会放群里）, at [00:14:20]

## 开放问题

- ⚠ "12345" 指什么？是 ticket 号、分支还是环境？三路引擎都听成"12345"— at [00:07:33]
- ⚠ "N-1" 是"上一个版本环境"还是某个命名环境（也可能是 MVP1）？— at [00:07:28]
- 默认 tag 值要改成什么？听作"proven / groove-in"，未能还原 — at [00:07:53]
- swap 之后 metadata 的 `role` / `tag` 不跟着变（截图里 role 仍是 `blue`、tag 仍是 `fe-1`，而 active URI 已变成 fe-2），这是预期行为还是 bug？— 见 IMG_8793
- Vincent 提到的 ⚠ "双活 GP 和 IC" 是哪些系统？它们各自再引出 blue-green 时 role 怎么设计？— at [00:11:06]
- 切换时要保证"回滚也不会失败"，但强一致性下多 API 调用仍需回切——最终是否接受"网络问题导致部分失败"这一残留风险？— at [00:20:50] [00:21:19]
- 白名单的账号范围到底是谁（"不太清楚是有哪些账号"）— at [00:13:58]
- 测试 ticket 是"每个 API 一个"还是"合并成一个"，Vicent 说单起一个 ticket 不覆盖所有 case，最终粒度未定 — at [00:23:52]

## 数字、日期与名称

- header 名：`x-active-slot`；blue tag = `fe-1`，green tag = `fe-2` — 截图 IMG_8791/8792
- 演示用的 base route：`data-reconciliation-service`；生成 `data-reconciliation-service-blue` / `-green` — IMG_8791
- 演示环境：gateway infra dev（前天一测就通）— [00:02:40]
- register 响应：`status: ACTIVE`、`notifiedSubscribers: 17`、`registerTime: 2026-11-10T09:49:26.760226391Z`、`swapCount: 0` — IMG_8791
- swap 响应：`blueUri` 与 `greenUri` 互换、`swapCount: 1`、`lastSwappedAt: 2026-11-10T09:52:39.269556797Z` — IMG_8793
- metadata 字段：`useEntitlementService: "true"`、`blueGreen: true`、`role`、`headerName`、`tag`、`registerTime`、`swapCount` — IMG_8791
- 现有 tag 已用到 `fe-1` 到 `fe-4`（Vincent 提出）— [00:11:06]
- 环境/域名：`apex-dev5.uk.hsbc`；`X-Release-Scope: apex_sub_entitlement_ui`；`X-Deploy-Version: green` — IMG_8787/8789
- 三个 story：register、swap、remove — [00:23:39]
- 参会 3 人 — 全场

## 需要跟进确认

1. **Devin vs Vincent 的归属**：声纹塌缩，两人身份是按内容推断的。唯一硬锚点是 [00:11:01] 的"Vincent 你有个问题想要了解吗"。若猜错，只需换标签，内容不受影响。
2. **文件名拼写**：文件名写 "Devin"，口述说 "Dylan"。确认后我改三处（transcript / output / INDEX）。
3. **⚠ N-1 的真实语义**：整套变更计划都挂在这个词上（"放到 N-1"、"做 N-1 的 setup"、"我找 N-1 那边"）。这是最需要确认的一项。
4. **默认 tag 值**：[00:07:53] 说"默认的 tag 就改成…"，新值听不清。改错会影响所有未指定 tag 的调用方。
5. **swap 后 metadata 未更新**：如果 dashboard 依赖 `role` / `tag` 显示当前 active slot，swap 之后会显示旧值。需确认是否要跟着 swap 更新。
6. **权限控制位置**：[00:12:25]–[00:14:05] 这一段四路引擎都吞词，只保留大意（走 Ansible template / application core）。实施前要跟 Devin 再确认一次具体配置点。
7. **"12345"**：Devin 说"把这些 change 都放到 12345 那边"，指向不明。

## 截图要点（11 张，`~/Downloads/IMG_8787–8797.JPG`）

| 截图 | 内容 |
|---|---|
| IMG_8787 | DevTools 请求头（`apex-dev5.uk.hsbc`）：Referer 带 `?release=green`，`X-Deploy-Version: green`，`X-Release-Context-Id`，`X-Release-Scope: apex_sub_entitlement_ui`，`X-Request-Id`。说明**前端侧已经有 release 标记机制** |
| IMG_8788 | 同 IMG_8787，纵向更长 |
| IMG_8789 | 同上，`X-Release-Context-Id` 高亮（本次请求带的是另一组 ID） |
| IMG_8790 | 同上，`X-Release-Scope` 高亮为 `apex_sub_entitlement_ui` |
| IMG_8791 | **register 请求 + 响应全文**：payload（baseRouteId / blueUri fe-1 / greenUri fe-2 / headerName x-active-slot / blueTagValue fe-1 / greenTagValue fe-2）与响应（blue/green routeId、ACTIVE、notifiedSubscribers 17、metadata 7 个字段）。左侧是 Jira 验收要点与附件（DEV_01_register… 10/Nov/26） |
| IMG_8792 | 同 8791，红笔圈出 blueUri / greenUri / blueTagValue / greenTagValue；共享屏幕计时 00:06:15 |
| IMG_8793 | **swap 请求 + 响应**：swap 后 blueUri = fe-2、greenUri = fe-1，`swapCount: 1`，`lastSwappedAt` 09:52:39Z；红笔标出 metadata 的 `role: "blue"` 没变 |
| IMG_8794 | register payload，红括号标出 headerName 与两个 tag value；共享屏幕 00:08:37 |
| IMG_8795 | 同 8794，红括号仍在，共享屏幕 00:08:55 |
| IMG_8796 | 红笔underline 在 `blueUri` 上（fe-1），共享屏幕 00:09:14 |
| IMG_8797 | 红笔在 `baseRouteId` 与 `blueUri` 上做标记，右侧手写 "Sid" 字样；共享屏幕 00:09:49 |

## 备注（推断，非录音内容）

- 截图里的 `X-Deploy-Version: green` 与 `?release=green` 说明 Apex 前端**已经有一个"当前 release"标记**在请求头里传递。blue-green 的新增 header（`x-active-slot`）与它并行，两者不是同一个东西——录音里没有明确说这一点，是从截图推出来的。
- `notifiedSubscribers: 17` 说明 register 会通知 17 个订阅方更新路由，这与上一轮 Pub/Sub 那条线是同一套机制（推断）。
- swap 之后 metadata 的 `role` / `tag` 保持不变，是本次截图里唯一像缺陷的地方：`role: "blue"` + `tag: "fe-1"`，但 active URI 已经是 fe-2。
- Geoff 说的"这一段前面没有任何有状态的东西"是判断，不是审计结论；Devin 表示同意。
