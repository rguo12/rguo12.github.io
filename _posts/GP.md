---
layout: post
title: Gaussian Process
---

A GP models functions as samples from an infinite dimensional multivariate normal distribution.
The shape of a function is determined by the mean and covariance (or kernel) function of the GP.
We use a GP as the prior distribution over the laten function:
\[f(\mathbf{x})\sim GP(m(x),k_{\theta}(x,x'))\].

