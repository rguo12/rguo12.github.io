---
title: "Making the Right Decisions in Complex Environments"
date: 2026-07-20
lang: en
translation_key: decisions-in-complex-environments
tags:
  - causal machine learning
  - reinforcement learning
  - research
---

# Technology

## A Long-Term Goal

While reading the great Fei-Fei Li's memoir, *The Worlds I See*, I came across something that made me feel ashamed and recognize the gap between myself and top scholars: for a while after finishing my PhD, I lacked a long-term research goal and lost my sense of direction. Another difference, of course, is that I have not been as willing as she was to take risks and persist with a long-term goal when circumstances turned against her.

I had not known that ImageNet had faced so much skepticism: that without crowdsourcing there seemed to be no hope of completing it, and that after its release it went largely unnoticed for two years. I cannot imagine continuing for so long through that kind of despair and low point, even while facing doubts from my advisor's advisor. Without Mechanical Turk, without Google Image Search, and without the miraculously “unorthodox” AlexNet appearing in the third ImageNet competition and beating the best SVM by ten percentage points in one stroke, we might still be obsessively studying CatBoost and some form of SVM today. The turning point in deep learning history depended on more than Hinton and his students' devotion to neural networks, convolutional kernels, and backpropagation. Fei-Fei and her students also persevered through a workload initially estimated to require twenty years, criticism that such a large dataset was meaningless when traditional models were used, and the constant risk of running out of funding. I genuinely cried when I reached the part about AlexNet. ImageNet waited for AlexNet, while GPUs, crowdsourcing, and image search engines made it all possible behind the scenes. The success of deep learning truly was a miracle.

I am the kind of person who becomes obsessed with technical details. When I learned about conformal prediction or minimax regret, my immediate reaction was to understand it, incorporate it into my research, and publish related work. But I never stopped to consider what difficult problem these techniques would actually help me solve.

Fortunately, while reflecting with GPT on the years since I graduated, I realized that I have in fact carried a long-term research topic in my subconscious: **making the right decisions in complex environments**. I greatly admire the kind of obsession Fei-Fei described—the ability to see anything and immediately think of ImageNet. Now that I have this topic, I seem able to ask questions I would not have asked before, when I thought purely like a paper-producing machine. For example, how do humans decide the order in which to learn different things? Consider table tennis and a player using inverted rubber: we first practice topspin, then looping long backspin balls, then handling short topspin and backspin balls over the table, and finally training against opponents who use unusual rubbers—for example, long pips, which return an incoming topspin ball as backspin. This progression feels highly intuitive. But when designing a learning sequence for a machine, how can we draw inspiration from human learning to select and order the training data? Are humans actually better than machines at this task? I know Bengio proposed curriculum learning, but it still seems far removed from the curricula humans follow. Choosing such a curriculum appears to be a difficult decision in itself.

Causality and reinforcement learning offer different perspectives on this problem. One focuses on the assumptions hidden beneath observed data, on when bias will erode a decision model, and on how to mitigate those biases—though the bottleneck of needing a causal graph is frustrating yet unavoidable. The other focuses on estimating future returns from the current state and action: looking forward from this moment and imagining, in the mind, the search tree that branches into parallel universes.

Now that I have this long-term goal, I will begin observing each decision I make, reflecting on it, and improving it. Everything suddenly seems more interesting.
