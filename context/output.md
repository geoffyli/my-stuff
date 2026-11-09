# Hugo 交接：线上支持值班 + Pub/Sub 订阅过期策略修复 — 2026-11-09

**参与者：** Hugo M Li（讲解 / 布置任务）、Geoff Li（接手）
**时长：** 00:16:10
**录音：** `~/.recordings/2026-11-09-hugo-support-handover-and-pubsub-expiration/`
**转写质量：** 三路交叉（Gemini 主转写 + Gemini 尾段补转 + 本地 whisper 校验），已人工合并。
声纹分离在 [00:05:19] 附近整体翻转，**发言人归属为按内容重建，不是测量结果**。
> ASR 含混范围：[00:00:14]–[00:01:30]（术语密集区，已按截图校正）、[00:09:32]–[00:10:29]（共享屏幕自言自语）、[00:12:55]、[00:13:48]、[00:15:33]（三处专有名词听不清，已在文中标 ⚠）。

---

## 结论

Hugo 交接两块工作给 Geoff。

1. **线上支持值班**：Geoff 接手三个 Teams 群，负责组件咨询答复、性能测试 503、PR review，以及最大的一块——帮业务修 CICD build（如 pom 升版本）。Hugo 估这项工作约 **4 天**。[00:00:14] [00:03:13]
2. **Pub/Sub 订阅过期策略**：所有订阅因创建时**少了 `expiration_policy` 参数**，在无活动 31 天后被自动删除。[00:07:25] 修法是在 Terraform tfvars 里给每个订阅加 `expiration_policy = "never"`，跑 Ansible job 应用，页面上确认"31 天"消失后再 merge。[00:12:33]

Hugo 已开 **PR #2282**（+64/−0，4 个环境文件），对应 **TREATRANS-57126**，会后把 ticket 发给 Geoff。[00:15:18]

## 决策

| 决策 | 负责人 | 理由 | 时间 |
|---|---|---|---|
| 用 `expiration_policy = "never"` 修根因，而不是永久手动重建 | Hugo | 缺参数是丢订阅的真因；重建后仍是 31 天 | [00:07:25] |
| 先重建订阅让业务先用（重建后依旧 31 天，"够它用了"），再按 PR 修 | Hugo | 先解业务燃眉之急 | [00:12:57] |
| 在 DEV → SIT 逐环境验证，每次都要在页面上确认参数已变 | Hugo | 只 merge 不改环境等于没修 | [00:12:05] |
| 修复要赶在下游上线之前完成 | Hugo | 无线上客户影响，风险低 | [00:15:33] |
| 支持值班先看 PR review，这是主要工作量 | Hugo | build 不过是最常见求助 | [00:00:14] |

## 行动项

- [ ] 按 PR #2282 的改动，为 DEV、SIT 各跑一次 Ansible job 应用 tfvars，并在 GCP 页面确认订阅过期时间不再是 31 天 — owner: Geoff, due: unstated, at [00:12:33]
- [ ] merge 代码前，在每个已应用的环境复核参数生效 — owner: Geoff, due: unstated, at [00:12:05]
- [ ] UAT 由他人执行（Geoff 无权限，Ansible 表单里那一行不显示），需发 PR 请对方跑 — owner: Geoff（发起）, due: unstated, at [00:13:48]
- [ ] 把 TREATRANS-57126 的 ticket 链接发给 Geoff — owner: Hugo, due: unstated, at [00:15:18]
- [ ] 把 Geoff 拉进三个 Teams 群（Geoff 已有第 2 个，缺第 1、第 3）— owner: Hugo, due: unstated, at [00:03:13] [00:03:36]
- [ ] 通读那份 tfvars，理解 Pub/Sub 与 filter 是怎么一步步建起来的 — owner: Geoff, due: unstated, at [00:14:34]

## 我的承诺（Geoff）

- [ ] 三个群置顶；其他群静音，但看到红点就点开看 — due: unstated, at [00:05:19]
- [ ] 接手线上支持：组件咨询、503 答复、PR review、CICD build 修复、现网问题处理 — due: unstated, at [00:00:14]
- [ ] 遇到问题在自己的记录里登记，便于后续估工时 — due: unstated, at [00:00:14]
- [ ] 尽快做 Pub/Sub 这件事（"最多一天"，"这周有空就弄"）— due: unstated, at [00:15:33]
- [ ] 有问题再问 Hugo — due: unstated, at [00:15:27]

## 阻塞 / 等待他人

- UAT 环境 Geoff 跑不了：没有权限，Ansible 模板里对应行不显示 — waiting on 环境权限或代跑的人, at [00:13:48]
- 三个群中第 1、第 3 个还没加上 — waiting on Hugo, at [00:03:36]
- ticket 链接未到手 — waiting on Hugo, at [00:15:18]

## 开放问题

- Hugo 说"你又发起一个 PR，去找 ⚠（听不清）去 approve"——UAT 具体找谁？— at [00:13:48]
- 问题记录写在哪个系统？ASR 听作"TII/TC"，⚠ 不确定，疑为 Jira ticket — at [00:00:14]
- Hugo 提到 support 的 epic 已建（whisper 确认"I created an epic"），epic 编号未说 — at [00:00:14]
- Hugo 说现网遇到两个问题、其中一个还在处理中——是哪两个、当前状态？— at [00:00:14]
- 下游 "⚠ 秘友 / BIB / Murex"（听不清）的上线日期是哪天？"赶在他们上线之前"没有具体日期 — at [00:15:33]
- 重建订阅时是否也要重设 filter、DLQ、retry 等参数，还是只用控制台默认值？— at [00:12:57]
- 为什么 GCP 控制台里的订阅名是 `workflow-outbound-dev2-topic-*`，而 tarraform 文件里读作 `workflow-outbound-local-topic-*`？需确认命名 — 见"截图要点"

## 数字、日期与名称

**通话中出现**
- 订阅默认过期时间：**31 天**（无活动即删除）— [00:12:33]
- 支持值班工作量：Hugo 估 **4 天**；Geoff 可能花 **2 天** — [00:00:14]
- Pub/Sub 这项工作：**最多 1 天**，可能不到 — [00:15:33]
- Teams 群数量：**3 个** — [00:03:13]
- 需要改的 tfvars 文件：**4 个** — [00:14:11]
- 环境顺序：**DEV → SIT → UAT**（UAT 本人不可跑）— [00:13:12] [00:13:48]

**截图补充（非音频）**
- Jira：**TREATRANS-57126** "Set pubsub expiration_policy to 'never'"；Sprint **Eagle-Sprint-26-W46-47**；Target **09/Nov/26 – 14/Nov/26**；估时 **1d 2h**；1 branch / 4 commits / 1 PR（IMG_8749）
- PR：**#2282**，`feature/TREATRANS-57126_pubsub_expiration_policy_never` → `master`；**+64 / −0**；Operability Score 43（Passed）；已请求 1 位 reviewer（IMG_8753 / 8761）
- 四份文件：`gcp_projects/hsbc-12401463-trsyplat-{dev,prod,devs,uatu}-dev/pubsub/WORKFLOW-INBOUND-OUTBOUND-{ENV}-PUBSUB.tfvars`（IMG_8754）
- 每份文件在多个 `pull_subscriptions` 块中插入 `expiration_policy = "never"`，位置行 57 / 69 / 81 / 93（IMG_8761）
- GCP 订阅实况（`hsbc-12401463-trsyplat-dev` / `workflow-outbound-dev2-topic-lim-sub`）：filter `attributes.callbackQueue = "queue_lim"`；DLQ 为 `workflow-outbound-dev2-deadletter-topic`；max delivery attempts **5**；exactly-once **Enabled**；message ordering **Enabled**；ack deadline **10 s**；message retention **7 days**；retain acknowledged **Yes**；**"Subscription expires in 31 days if there is no activity."**（IMG_8758 / 8759）
- 同一 topic 下 4 个订阅：`-topic-sub`、`-topic-lim-sub`、`-nli-sub`、`-entitlement-sub`（IMG_8752）
- Ansible 模板：`apex-infra-gcp-builder-apex-{dev,sit,uat}`；terraform module 选 `pubsub`；var 文件 `WORKFLOW-INBOUND-OUTBOUND-{ENV}-PUBSUB`（IMG_8756 / 8760）
- 操作文档：Confluence "How to create and modify pubsub topic"（IMG_8756 / 8760）；代码参考 PR #2062（`Feature/treatrans 41669 all workflow topic`，commit 922ff67）

## 需要跟进确认

1. **ticket 链接**：Hugo 只覆盖了主 topic 的 UAT.tfvars（`#L139`），PR 实际改了 4 个环境的文件——确认 PR 是权威清单。
2. **订阅命名**：截图里的 tfvars 读作 `workflow-outbound-local-topic-*`，控制台是 `workflow-outbound-dev2-topic-*`。改文件时以仓库实际内容为准。
3. **UAT 执行人**：Geoff 无法自己跑 UAT，需确认由谁 apply。
4. **重建方式**：Hugo 说"重新创建一遍还是 31 天，但够它用了"——需确认重建时 filter / DLQ / retry 是否手工补齐，否则重建出来的订阅与代码不一致。
5. **下游上线日期**："赶在 ⚠ 他们上线之前"，具体日期未说。
6. **记录位置**：问题登记写在 Jira 还是别的系统，未说清。
7. **TF 只加订阅级参数**：PR 未动 topic 级 `message_retention_duration`，确认无需改。

## 截图要点（16 张，`~/Downloads/IMG_8746–8761.JPG`）

| 截图 | 内容 |
|---|---|
| IMG_8746 | Jira TREATRANS-54705 评论 "Routine Support"：在 APEX UI 模拟 Gateway token 失效——在 localStorage 里用旧值 `dXNlcg==` 覆盖 `ecosystem-main-storage`。这是支持值班里的"例行咨询"典型例子 |
| IMG_8747 | Confluence "New Ansible Template on using entitlement API"：import/update 各类 entitlement 的流程、`rerunnable`/`fallback` 目录、pom.xml 升版本、feature branch → PR。与"帮业务 review/修构建"对应 |
| IMG_8748 | GitHub `entitlement-data/configs/rerunnable/DEV/20260115/7_excel_nii_svc_attr.json`（staffId GB-TRS-SB-D、roleName FInops、useCase IRRBB_MANAGEMENT 等）。与前一项工作的画面，非本议题 |
| IMG_8749 | **Jira TREATRANS-57126** 详情页：问题描述、tfvars#L139 链接、Sprint、日期、估时、1 PR |
| IMG_8750 | `UAT.tfvars` 代码：多个 subscription 的 `expiration_policy = "never"`（行 121/130/139/148），行 139 高亮 |
| IMG_8751 | GCP Console → Pub/Sub → Topics（`hsbc-12401463-trsyplat-dev`）：大量 topic，Retention 多为 `-`，仅 `lim_fech_notification_from_LIQ` 为 7 days |
| IMG_8752 | Topic `workflow-outbound-dev2-topic` 详情：列出 4 个订阅 |
| IMG_8753 | **PR #2282** 概览：4 commits、checks 通过、Operability 43、+64/−0、reviewer 待批 |
| IMG_8754 | PR Files changed：4 个环境 tfvars，每份加 `expiration_policy = "never"` |
| IMG_8755 | Jira 描述编辑态：正文 + PR 链接 |
| IMG_8756 | Confluence 操作文档：Ansible 模板 `apex-infra-gcp-builder-apex-sit`、branch `feature/TREATRANS-41144_add_workflow_topic`、module `pubsub`、var 文件 `WORKFLOW-INBOUND-OUTBOUND-SIT-PUBSUB` |
| IMG_8757 | Jira 描述（三个链接：tfvars、PR #2282、Confluence 文档） |
| IMG_8758 | 订阅 `workflow-outbound-dev2-topic-lim-sub` 详情：filter、DLQ、delivery 设置、**"expires in 31 days if there is no activity"** |
| IMG_8759 | 同上，拉近截图，文字更清晰（截图时间点 00:14:09，与通话中"看一下这个参数"对应） |
| IMG_8760 | Confluence：Find job template，三个 Ansible 模板 + 代码参考 PR #2062 |
| IMG_8761 | PR Files changed（与 8754 同，命名更清晰） |

## 备注（推断，非录音内容）

- "31 天"是 GCP Pub/Sub 订阅的默认 `expirationPolicy`（`expires_in 31 days`）。截图直接印证，因此这条不是Hugo 口述的数字误差。
- PR 只新增 `expiration_policy`，没有改 filter、DLQ、retry（+64/−0，无删除行），因此"改完参数就生效、其他行为不变"这个判断成立。
- Hugo 说"我当时没有用我这个新的代码，所以所有环境还是 31 天"——意味着**代码已改但环境未应用**，这正是他让 Geoff 跑 Ansible job 的原因。
- "下线在 31 天后" 只作用于**订阅**；topic 本身不因无活动被删。丢的是 subscription，因此消息不再投递（Hugo 说"东西都丢了"）。
- 通话里 Hugo 提到的估时（4 天 / 2 天 / 1 天）是他的口头估算，未经校验。
