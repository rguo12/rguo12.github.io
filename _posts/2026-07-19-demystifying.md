---
title: "Notes on Causal ML, Reinforcement Learning, and Life"
date: 2026-07-19
lang: en
layout: post
translation_key: demystifying
tags:
  - causal inference
  - reinforcement learning
  - personal notes
---

> [中文版]({{ "/blog/zh/2026/demystifying/" | relative_url }}) (Chinese version) is available.


No more silence. Starting today, I am going to learn from the great Tony and write a blog (though he mostly writes a diary). The best thing about writing is being able to be myself without pressure. I will write in Chinese because it feels more natural—but here is an English version too.

Today I hiked at Castle Rock State Park in the South Bay, where the views are excellent. I also talked with Xuan, an expert in causal inference, about causal machine learning.

# Technology

## Synthetic DiD

Today I learned about Synthetic DiD. The idea is simple: when doing difference-in-differences, if you cannot find a real control group with a matching trend, you use the idea of synthetic control to construct one. Its pre-treatment trend should match that of the treated unit. Here comes the mystical part: nobody knows whether a synthetic control whose pre-treatment trend matches the treated unit will continue to track its trend after treatment. Nobody knows! This is an awkward situation that often arises in causal inference. How can we tell whether my synthetic control or yours has the more realistic post-treatment trend? It is a beautiful counterfactual question.

## Confidence intervals depend on assumptions, so they are also an illusion

Confidence intervals are unfamiliar to me. ML papers are often content to report a mean and standard deviation—but where is the distribution? Nobody f cares. Still, whenever someone says that conformal intervals are wide while confidence intervals are narrow, it is puzzling: why are the latter allowed to be narrow? Ah, because of assumptions.

GPT's summary: conformal intervals are often wide because they honestly cover outcome-level randomness; SDID confidence intervals are often narrow because they only cover estimator-level randomness and assume that weighting has removed the most difficult counterfactual bias. I do not know whether that is correct. I hope to study conformal methods further someday.

## Ignoring causality in RL: shameful, but useful

Accounting for causality is more painful—especially when the policy that generates each trajectory is different and the environment is dynamic. What can you do then?

RL is, at its core, multi-step causal inference. That is very clear. On-policy RL learns from interventional data; that is beyond doubt. The Q function is a multi-step version of a potential outcome.

Most RL is obsessed with estimation, while causal RL cares more about identification. Perhaps I will have a chance to study this further later.

## Can bandits replace A/B tests?

This is a very interesting question. At its core, bandits aim to avoid the negative effect an A/B test can have on average outcomes: estimate a treatment effect while improving the average outcome. There is no free lunch! So how can we improve the average outcome without biasing the treatment-effect estimate downward? I have not studied this carefully yet.

## We cannot intervene!

A leader at my company said that intervention is unrealistic in a certain setting. So you are telling me that you will give me no data at all for the counterfactual part, yet still expect me to predict the counterfactual? Come on.

## User simulators

If you can build a user simulator, you have already solved causal inference. So who is investing in companies building user simulators?

## Causal world models

I have been working on this recently. It is my last dance before leaving Intuit. Kasra helped me clarify all the questions, but needing a graph makes everything very painful. That is why I am so pessimistic about causal ML—though perhaps I am wrong.

# Life

## A grand vision of robots and productivity

Today I listened to Zhang Xiaojun's interview with Kay, a researcher at Pi. My favorite passage was this: if robots become powerful enough, one person could build everything on a planet, survive there, and become self-sufficient. Productivity would become extremely easy to obtain. It is wonderful and distant, but it makes robotics exciting.

## Do not eat pressure

Many bloggers have been talking about “not eating pressure”—not internalizing pressure. Maybe that is right, but it also feels impossible. Or perhaps a manager's job is to put pressure on employees, and pressure becomes motivation. But too much pressure hurts both efficiency and long-term mental health. Managers who strike the right balance are rare.

Shuai once said that work is about managing your relationship with your manager. Looking at things from their perspective may make the pressure feel smaller. My recent realization is: you feel pressure because you are not yet strong enough and you are not putting in the time. If you can easily beat your manager's expectations, things get much better. Of course, you can also get there by managing your manager's expectations well.

## Saka's hat trick

Congratulations to Saka for starting and scoring three goals after being unable to play in the semifinal. Given his ability, it will probably be difficult for him to score another hat trick at a World Cup. I hope he continues to perform well for Arsenal.
