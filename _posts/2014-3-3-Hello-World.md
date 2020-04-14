---
layout: post
title: Invariant Risk Minimization
---

The work [1] is motivated by the fact that the data we collected from observation or experiments can suffer from selection bias and confounding bias etc..
In these cases, minimizing a regular training error confronts the risk of fitting the model to capture any statistical associations. This is okay if all the probability distributions are the same across the training and test sets, which may not be true in real-world applications.

For example, we want to identify which relationships the model captures are spurious. For example, the co-appearance of green pastures and cows may result in image classifiers that tend to label any image with green pastures to be a cow.

Therefore, in contrast, we aim to consider the causal relationships between the observed and potentially unobserved variables to avoid training classifiers that exploit spurious correlations. One possible approach is to develop a new loss function that is causality-aware. Previously, there exists some methods such as causal regularization [2], unbiased learning to rank [3] and debiased recommendation systems [4] which are working on similar directions.

[1] Arjovsky, Martin, Léon Bottou, Ishaan Gulrajani, and David Lopez-Paz. "Invariant risk minimization." arXiv preprint arXiv:1907.02893 (2019).
[2] Bahadori, Mohammad Taha, Krzysztof Chalupka, Edward Choi, Robert Chen, Walter F. Stewart, and Jimeng Sun. "Causal regularization." arXiv preprint arXiv:1702.02604 (2017).
[3] Joachims, Thorsten, Adith Swaminathan, and Tobias Schnabel. "Unbiased learning-to-rank with biased feedback." In Proceedings of the Tenth ACM International Conference on Web Search and Data Mining, pp. 781-789. 2017.
[4] Schnabel, Tobias, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims. "Recommendations as treatments: debiasing learning and evaluation." In Proceedings of the 33rd International Conference on International Conference on Machine Learning-Volume 48, pp. 1670-1679. 2016.