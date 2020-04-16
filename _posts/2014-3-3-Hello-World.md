---
layout: post
title: Invariant Risk Minimization
---

####Introduction

The work [1] is motivated by the fact that the data we collected from observation or experiments can suffer from selection bias and confounding bias etc..
In these cases, minimizing a regular training error confronts the risk of fitting the model to capture any statistical associations. This is okay if all the probability distributions are the same across the training and test sets, which may not be true in real-world applications. In fact, the current standard way to test a ML model is to use randomly shuffled training-test split may cause some problems. Doing such shuffling can lead to loss of the information about how data distribution changes when the data source or data collection configuration changes. Often spurious correlations may not hold when there is a change in the distribution of the data.

For example, we want to identify which relationships the model captures are spurious. For example, the co-appearance of green pastures and cows may result in image classifiers that tend to label any image with green pastures to be a cow. However, when we test the classifier with images with a cow in a desert, the spurious correlation (green pasture -- cow) would not hold, therefore, relying on spurious correlations can lead to errors.

Therefore, in contrast, we aim to consider the causal relationships between the observed and potentially unobserved variables to avoid training classifiers that exploit spurious correlations. Thus, authors want to take a step back to assume that the data is collected from different *environments*. Then, they aim to let the ML model capture the correlations robust across multiple environments, which are not likely to be spurious.

####Invariant Risk Minimization

We consider the dataset with instances from multiple environment -- $D_{e}:=\{(x_{i}^{e}, y_{i}^{e})\}_{i=1}^{n_{e}}$. We want to learn a function $f(X)\approx Y$.




[1] Arjovsky, Martin, Léon Bottou, Ishaan Gulrajani, and David Lopez-Paz. "Invariant risk minimization." arXiv preprint arXiv:1907.02893 (2019).
