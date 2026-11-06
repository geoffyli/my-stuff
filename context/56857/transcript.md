# Transcript — Apex Gateway 蓝绿路由（Vincent Wang × Geoff Li）— 2026-11-06

- **Source:** `Vincent Gateway Bluegreen Routing - 2026-11-06.m4a`
- **Duration:** 00:18:20
- **Method:** two independent transcripts merged:
  - Gemini `gemini-3.5-transcribe` (cloud, with diarization) → `transcript.gemini-raw.md`
  - whisper.cpp `ggml-large-v3-turbo-q8_0` (local, no diarization) → `whisper/transcript.whisper-raw.txt`
  - The text below uses the whisper timeline and wording. Gemini and the 28 screenshots were used to check words, names, and identifiers.
- **Speaker labels:** reconciled by the agent, not measured.
  - Gemini diarization collapsed: `spk_1` = 98% of speech, 15 turns. It cannot separate the two people.
  - `SPEAKER_1 = Vincent Wang`: the presenter who shares the screen. Name source: screenshot tiles and the banner "Vincent Wang's screen".
  - `SPEAKER_0 = Geoff Li`: the listener who asks questions. Name source: screenshot tiles.
  - Attribution for each turn comes from content (who asks, who explains). Treat it as inferred.
- **Reconstructed range:** the whole recording. No turn has a measured speaker boundary.
- **⚠ marks:** uncertain ASR word or name. Verify before you quote it.
- **Facts from the user:** this recording is about JIRA task "Implement register, swap, and remove APIs for blue-green routing in gateway service". The user says the task is assigned to Geoff. The screenshot shows the assignee is **Vincent Wang** (see Open questions in `output.md`).

---

## [00:00:06] SPEAKER_0_GEOFF

对，哈喽。

## [00:00:07] SPEAKER_1_VINCENT

这个是 ⚠Belwin 领导的一个东西，他让我们帮做，你帮忙做一下。就是他做整体的前后端蓝绿部署，你知道大概的蓝绿部署的概念吗？

## [00:00:32] SPEAKER_0_GEOFF

蓝绿部署应该是发布的时候，我们有两个版本，然后把流量切到新版本；有问题就退回旧版本，对吗？

## [00:00:46] SPEAKER_1_VINCENT

对，就是这样。他现在前后端都要做，UI 那部分他负责。后端的话，他访问 gateway，切换到绿的时候，也要根据一个路由切过去。现在我们做的是 API 部分。这个你也知道，是 Spring Gateway。它的路由我们有一些配置文件在这里，你可以先找一下。

## [00:01:12] SPEAKER_1_VINCENT

API 部分实际上你也知道是吧？

## [00:01:18] SPEAKER_0_GEOFF

这个我知道。

## [00:01:20] SPEAKER_1_VINCENT

Spring Gateway 的话，它的路由我们也有一些 ⚠SED（可能是 YAML）文件在这里。这个请求不用看。这个是 actuator，应该大概也知道，它集成了很多 endpoint，可以查路由、查各种信息。Spring Gateway 有一个 endpoint 可以查已注册的路由。你访问 gateway 再加上前缀，它就会路由到目的地，对不对？

## [00:02:42] SPEAKER_0_GEOFF

OK，明白。

## [00:02:46] SPEAKER_1_VINCENT

这个官方文档你看一下。你的学习能力很强。Spring Gateway 其实很简单，我也可能有一段时间没看了，还要再看看文档。这些实际上都已经有了，我们都实现完了。现在要做的，实际上是组合。现在只是讲一些背景，我不知道怎么开展好。

现在是讲背景。他所有服务的路由都注册在这里。还有两种：这个是他改造过的，原生写法可以一个个定义路由。他自己改造了一下，用一种写法去注册，有点长，常人看不懂。但大概就是路由 ID，然后是路由的目的地。如果他不写 ⚠predicate（原文 "帕子"），就按这个去路由，比如自动按这个去路由。

我们现在的路由可能第一条你自己看看更好。我觉得可以保持不同。你可以随时问任何问题，我觉得你的能力应该完全没有问题，只是我们需要沟通，了解你的想法。

路由已经在这里了。可以新增、可以改，但这些是静态路由，重启之后又重置了。所以当时已经引入了 Redis，动态管理路由。官网也是 built-in 的 feature。我们只要把 Redis 开起来，然后我们已经注册了 Spring Data，它就会自动注册。这样我们就可以动态地增加路由。静态路由重启就重置了，但动态管理的路由，我们删了就没了，不会重启后又恢复；我们加了，它也一直在那里。

我给你看一个正式的例子。原来静态那边你可以看到它配了这个，然后再加一些，只要 ID 不重复就可以了。它就根据 ⚠Predicate 去路由到什么地方。这就是一个完整的路由。其他你自己去看，看概念就好了。

## [00:05:52] SPEAKER_1_VINCENT

好的。这样就可以。然后调它的接口，就是这个 API。它可以新增路由。新增路由之后，刷新一下就可以了。删除就是 ⚠DELETE 的接口。

## [00:06:49] SPEAKER_1_VINCENT

现在我们要做的，是支持蓝绿部署，把那个组合起来。它那边有两个版本：一个 UI 是蓝，一个 UI 是绿。它不想这样写很多东西，所以要提供一个简单的 API。我提供一个高级 API，我就自动加一组 API。我假设这个是蓝，这个是绿。我想的就是这样。

我们可以加一个 header。header 有两部分：一个是名字，一个是值。这个我们可以自己定义。这个在做之前，你可以先把设计写出来，因为现在很快，也可以直接写出来，让他满足需求。我设想的就是这个。要起个名字，要自己设计一下，对吧？

对。然后让它传一个请求。我请求一个 API，我带了一个 header，header 名字叫这个，它的值是这个，那么它就会路由到这里。就是这么简单。

这里给你一个例子，看完那个路由你就知道了。我看一下在哪里。就像我请求一个 API，我加一个 header，是什么就是什么。刚才那个 ⚠"BlueGreen Tag"（header 名 `x-blue-green-tag` 来自截图 IMG_8694/8696，音频不清楚）再加一个 blue，它就会命中这个路由；green 就命中那个路由。完全一样，复制过来就行。它一个是 1，一个是 2。

我现在要组织这么大的一个 body，不想那么复杂，我们就简单一点。它要做的是蓝绿。它那里首先已经有它的服务在这里。比如我要对这个服务做蓝绿：我们想法是，API 一进来，注册的时候，我就新增一组路由。参数我们定义好了吧，就是它要传一个已存在服务的路由 ID 过来。然后蓝的路由目的地是什么，绿的路由目的地是什么。其他参数，比如 retry、circuit breaker 之类的功能，就复制它已有的。我只复制已有的路由，然后修改它的路由目的地，以及 predicate。它原来是 Path，我再加一个 header。

这样就满足了。看完文档，我就加一组 order 都是 -1 的路由，order 越小优先级越高。我加了蓝绿之后，原来那个路由就失效了，永远不会命中它，因为按优先级来。请求过来，即使 path 相同，但只要带了那个 header，一旦命中新增的那一组路由，就已经完成路由了，流量已经出去了。原来那个路由就不会命中。这个路由还留在那里，每次重启它都在。

所以我们现在新增一个 API，它可以组合，一次性就加两组路由。body 不要这么复杂，它只需要传一个路由 ID，以及两个 URL 就行了。它这里已经是一次批量就能新增两组路由了，但 body 还是很复杂，它不想这么复杂。现在我们是在 gateway 里再加一个 API 来做这件事。

## [00:12:24] SPEAKER_0_GEOFF

大概……意思我明白了。

## [00:12:27] SPEAKER_1_VINCENT

对。现在它已经有一个 gateway 自己的 API，但我们要定一个简化的 API，简化它的请求体。大概就是这样。它现在还在 POC 的状态，但慢慢进入状态了，之后慢慢开始改，也还是初始的状态。我看它还在 dev，我们也在 dev 做。

我们可以做一个 register（注册），再加一个 swap（交换）。它只要调我，我就把蓝绿的 URL 交换下去，上面下面交换一下。它说不需要的话，也可以。不需要的话，我们也可以做 remove（删除），把那一组蓝绿都删掉，因为不要的话也是一个后门，可以删掉。我就不要蓝绿功能，我可以下线。最主要是前面两个，register 和 swap。我们就做一个 API，做两个 API 就行。

## [00:13:46] SPEAKER_0_GEOFF

好的。

## [00:13:48] SPEAKER_0_GEOFF

大概我明白了。

## [00:13:49] SPEAKER_1_VINCENT

这个东西，我看有些要设计的。我觉得之后再沟通一下吧。对，我们沟通一下。他下周要……

## [00:14:00] SPEAKER_1_VINCENT

我下周 ⚠疫情假（原文可能是 "请假"，ASR 不稳定；Gemini 版本没有这句）。主要是他下周要。我们都在 dev 开发，并且这个本地的 setup，我以前就给你，就行了。你本地能起来，本地能起来，就需要配一些数据库。因为它这个，我们实际上不用数据库，只是用 Redis。但是 Redis 那些连接也依赖了数据库，所以要配对那些数据库才能在本地起来。

我们测试的话，可以改这个。比如说，我现在用的数据库，你看它和 dev 是相关的，它用了一个 5。你如果自己随意测试，你就用一个 7、8 那些。它一直好像有 16 个数据库。我就不会影响到那些 dev。你看，只要不要用 3，不要用 2 ⚠（whisper 为 "只要用2"，Gemini 为 "不要用二"，需要确认），那就没问题了。

## [00:14:54] SPEAKER_0_GEOFF

好的，好的。

## [00:14:56] SPEAKER_1_VINCENT

这是共用一个集群的。这个是一个 process，实际上这两个是同一个集群。你用一个 6 什么的，7 什么的。你可以看一下它的路由，都是那种静态的路由，不是存在 Redis 的路由。也有一些 Redis 的 API，去看一下它已有的路由。其实你看官方文档，它那个新增的路由，它的 key 是什么都能看到，然后就能 get 出来看一下。

但是，它刚才这个 API，也已经会从 Redis 里拿出所有的，不管是存在 Redis 的，还是存在静态路由的，都全都拿出来了。还有官方的 API。

## [00:15:44] SPEAKER_0_GEOFF

好的。

## [00:15:45] SPEAKER_1_VINCENT

大概是这个事情。只是提前交代，让你在有空的时候可以研究一下。

## [00:15:50] SPEAKER_0_GEOFF

我今天可以先看一下吧。

## [00:15:52] SPEAKER_1_VINCENT

对。有什么疑问我们就即时沟通。因为如果我自己接触这个，我的接受能力肯定没你快，但是可以沟通到。没事，没事。遇到问题，然后我再问一下吧。

## [00:16:09] SPEAKER_0_GEOFF

嗯，好。

## [00:16:13] SPEAKER_1_VINCENT

它也做了一些分支，在 ⚠K 位（原文 "K位"，无法确认）。像它那个是一个 ⚠分数（无法确认）。这个 ⚠chick（可能是 "check" 或 "trigger"）的话，你可以改。你可以自己弄一个 branch，部署上去做一些测试，也不会影响到任何人。像这个 Cloud Build 的一个 trigger，然后，类似 gateway 的，因为像 ⚠Wattflow（无法确认）你已经注意到了，它只会一和二。它就是因为在这个 trigger 配了。你可以配一个自己方便测试的分支，它就可以部署上去了。

你看，这是我们其他，它们各种配的一到五。所以只有一到五有环境。你可以继续加，加一些自己测试的，或者利用已有的一些东西。OK，就是一个分支，然后按那个分支就可以用来测试了。

## [00:17:19] SPEAKER_0_GEOFF

好的，好的。

## [00:17:24] SPEAKER_1_VINCENT

像你要什么你做什么，就把那些东西发给你就行了。

## [00:17:28] SPEAKER_0_GEOFF

好的，没问题。

## [00:17:30] SPEAKER_1_VINCENT

就是这样，这样的一个事情。

## [00:17:33] SPEAKER_0_GEOFF

那个 ⚠x meta（无法确认），那个他没批，是不是要 reschedule 到今天下午六点了？

## [00:17:39] SPEAKER_1_VINCENT

我看一下。我也在咨询一下。这种对，他说没关系，就是在之前、在之后都 reschedule。你刚才说是几点啊？

## [00:17:48] SPEAKER_0_GEOFF

下午六点吗？

## [00:17:52] SPEAKER_1_VINCENT

六点，那六点应该没问题。我也要本来让 ⚠Tim 提了一个，他那个没批。我也要做这个，六点应该也行吧。

## [00:18:06] SPEAKER_0_GEOFF

OK，好的好的。

## [00:18:08] SPEAKER_1_VINCENT

就六点，或者……

## [00:18:10] SPEAKER_0_GEOFF

没有其他问题了。嗯，好，谢谢。

## [00:18:13] SPEAKER_1_VINCENT

好，拜拜。

## [00:18:15] SPEAKER_0_GEOFF

拜拜。
