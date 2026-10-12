---
title: "关于因果机器学习、强化学习与生活的笔记"
date: 2026-07-19
lang: zh
permalink: /blog/zh/2026/demystifying/
layout: post
translation_key: demystifying
tags:
  - causal inference
  - reinforcement learning
  - personal notes
---

> 这是中文版。[Read the English version]({{ "/blog/2026/demystifying/" | relative_url }})


不再沉默。从今天开始我向伟大的Tony学习，写博客（当然他主要是写日记）。写文字最好的一点是，毫无压力地做自己，所以我会写中文，这样更自在。

今天去到南湾景观很好的Castle Rock State Park徒步。跟做Causal Inference的专家Xuan聊了一下Causal ML的相关话题。

# 技术

## Synthetic DiD
今天了解了Synthetic DiD这项技术，idea很简单，就是当你做DiD却找不到trend一致的真的control的时候，就利用synthetic control的想法制造一个synthetic的control，要求其pre treatment与treated unit的pre treatment trend一致。这里的玄学问题就来了：没有人知道pre treatment一致的synthetic control能否在post treatment跟treated unit的trend能够保持一致。Nobody knows！这是causal inference里面常常遇到的尴尬局面。这种时候我们怎么才能知道我的synthetic control跟你的synthetic control，哪个在post treatment里的trend更加真实呢？这将是一个美妙的，关于Counterfactual的问题。

## Confidence Interval依赖于假设，因此也是一种错觉
我对CI这个东西是陌生的，因为ML的论文常常满足于report mean和std，distribution在哪里？Noone f cares。但每当提到Conformal的interval很宽的时候，Confidence interval很窄就很令人疑惑，你就凭什么窄呢？噢，原来是因为假设啊！

GPT老师总结：Conformal interval 常常宽，是因为它诚实地覆盖 outcome-level randomness；SDID confidence interval 常常窄，是因为它只覆盖 estimator-level randomness，并假定最棘手的 counterfactual bias 已被 weighting 消除了。不知道对不对。希望有一天我能继续研究Conformal这个话题。


## 在RL中忽略Causality：虽然可耻但有用
因为考虑Causality更痛苦。特别是如果产生每个trajectory的policy是不一样的，如果环境是dynamic的，你怎么玩？

RL本质是多步的Causal Inference，这一点是非常清晰的。另外就是on-policy的RL本质是从interventional data中学习，这一点也是毫无疑问的。Q function就是potential outcome的多步版本。

大多数RL是痴迷于estimation的，而causal RL更重视identification。以后有机会再展开研究吧。


## bandit能取代A/B test吗
这是一个非常有意思的话题，本质上bandit是为了避免A/B test中对average outcome的负面作用。一边测treatment effect，一边提升average outcome。There is no free lunch!所以呢，提升average outcome的同时怎样不让treatment effect bias低呢？我还没有认真去研究这个问题。

## 我们不能做Intervention！
我司领导说，在某场景下做intervention是不现实的。你意思是告诉我，counterfactual那部分什么数据你都不给我，还想让我预测counterfactual？做个人吧！

## User simulator
如果你能够制造出user simulator的话，你已经解决了causal inference，所以，是谁在投资那些做user simulator的公司呢？

## 因果世界模型
最近在做这方面的东西，在离开Intu前的last dance了，Kasra帮助我把问题都搞清楚了，可惜需要graph这件事让人非常痛苦。所以我才说，对Causal ML非常悲观，也许我是错的。


# 生活



## 机器人与生产力的伟大构想
今天听张小珺采访Pi的研究员Kay，最喜欢的一段是说，如果机器人足够强大，那一个人就可以在一颗星球上搭建一切，生存下来并且自给自足，生产力变得十分地容易得到。太美妙了，太遥远了，但让人对机器人这件事心动。

## 不吃压力
很多博主在聊不吃压力。可能不吃压力才是对的，但也是不可能的。或者理解为，manager的工作就是给员工压力，而压力就是变成动力。但是压力太大就会影响员工的效率和长期的心理健康，把握得好尺度的manger是难得的。Shuai曾经说过，工作就是跟manager处关系，换位思考的话，可能压力就没那么大了。我个人最近的感悟是，你菜而且不堆时间，所以你才有压力。如果你能够轻松beat manager的expectation的话，你就会好很多。当然你也可以通过管理好manager的expectation来做到这一点。

## 萨卡帽子戏法
祝贺卡子在无法出场的半决赛后，能够首发并打入三球。估计以卡子的能力，再在世界杯上拿一次帽子戏法是很难的。希望你会阿森纳好好发挥吧。
