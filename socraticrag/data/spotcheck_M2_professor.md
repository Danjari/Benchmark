# M2 Spot-Check — Retrieval Faithfulness

> **How to view formulas:** paste this file into [https://markdownlivepreview.dev/](https://markdownlivepreview.dev/) and all math will render automatically.

> **How to fill in:** open `spotcheck_M2_professor.csv` in Google Sheets and enter your verdict in the **YOUR\_VERDICT** column for each row ID shown below.

> **SUPPORTED** — the presupposition is a claim that can be directly derived from Context C.  
> **NOT SUPPORTED** — the claim is absent from or contradicts Context C.

---

## Item — *accurate* &nbsp;·&nbsp; rows 1–6

**Context C**

It's also true that, within a single neural network, we may well want to have different step sizes. As our networks become deep (with increasing numbers of layers) we can find that magnitude of the gradient of the loss with respect to the weights in the last layer, $\partial \log \partial W_L$, may be substantially different from the gradient of the loss with respect to the weights in the first layer $\partial \log \partial W_1$. If you look carefully at equation 8.3, you can see that the output gradient is multiplied by all the weight matrices of the network and is "fed back" through all the derivatives of all the activation functions. This can lead to a problem of exploding or vanishing gradients, in which the back-propagated gradient is much too big or small to be used in an update rule with the same step size.

**Tutor Response R**

How might using different step sizes for different layers help address the issue of varying gradient magnitudes during back-propagation?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 1 | Different layers can be assigned different step sizes (learning rates) during training | |
| 2 | Gradient magnitudes vary across different layers during back-propagation | |
| 3 | Varying gradient magnitudes during back-propagation is a recognized issue in neural network training | |
| 4 | Using different step sizes for different layers is a possible approach in optimization | |
| 5 | The step size used during training affects how updates are applied in response to gradients | |
| 6 | Back-propagation computes gradients that are used to update model parameters | |

---

## Item — *accurate* &nbsp;·&nbsp; rows 7–13

**Context C**

Another common strategy is to simply penalize the norm of all the weights, as we did in ridge regression. This method is known as weight decay, because when we take the gradient of the objective

$\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$

we end up with an update of the form

$W_{t}$ $=W_{t-1}-\eta\left(\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)+\lambda W_{t-1}\right)$
$=W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)\enspace.$

This rule has the form of first “decaying” $W_{t-1}$ by a factor of $(1-\lambda\eta)$ and then taking a gradient step.

**Tutor Response R**

How does reducing the weights by a factor of (1-λη) help in controlling the size of the weights and potentially reducing overfitting?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 7 | Reducing weights by a factor of (1-λη) is a specific operation that occurs during weight updates | |
| 8 | λ is a regularization parameter and η is a learning rate in this context | |
| 9 | This weight reduction mechanism has an effect on the size of the weights | |
| 10 | Controlling the size of weights is a relevant goal in machine learning | |
| 11 | Overfitting is a problem that can be addressed by controlling weight sizes | |
| 12 | Large weights are associated with or contribute to overfitting | |
| 13 | The factor (1-λη) is less than 1, meaning it shrinks the weights each update | |

---

## Item — *accurate* &nbsp;·&nbsp; rows 14–20

**Context C**

A model class $\mathcal{M}$ is a set of possible models, typically parameterized by a vector of parameters $\Theta$. What assumptions will we make about the form of the model? When solving a regression problem using a prediction-rule approach, we might try to find a linear function $h(x; \theta, \theta_0) = \theta^T x + \theta_0$ that fits our data well. In this example, the parameter vector $\Theta = (\theta, \theta_0)$.

**Tutor Response R**

How does including the bias term $\theta_0$ in the parameter vector $\Theta$ affect the flexibility of the linear function in fitting the data?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 14 | The bias term is denoted $\theta_0$ | |
| 15 | The bias term $\theta_0$ can be included in the parameter vector $\Theta$ | |
| 16 | The parameter vector $\Theta$ exists and contains model parameters | |
| 17 | A linear function is being used to fit data | |
| 18 | Including or excluding $\theta_0$ in $\Theta$ affects the behavior of the linear function | |
| 19 | The flexibility of a linear function in fitting data is a meaningful and measurable property | |
| 20 | The bias term affects the flexibility of the linear function differently than if it were excluded | |

---

## Item — *accurate* &nbsp;·&nbsp; row 21

**Context C**

Another common strategy is to simply penalize the norm of all the weights, as we did in ridge regression. This method is known as weight decay, because when we take the gradient of the objective

$\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$

we end up with an update of the form

$W_{t}$ $=W_{t-1}-\eta\left(\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)+\lambda W_{t-1}\right)$
$=W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)\enspace.$

This rule has the form of first “decaying” $W_{t-1}$ by a factor of $(1-\lambda\eta)$ and then taking a gradient step.

**Tutor Response R**

What in the objective function J(W) do you think mathematically causes the weights to be "kept small," and how does that term relate to the (1-λη) factor you see in the update rule?

> **Row 21** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *accurate* &nbsp;·&nbsp; row 22

**Context C**

If $y$ is a scalar and $\mathbf{X}$ is a matrix of size $[n \times m]$, then

$$
\frac{\partial y}{\partial \mathbf{X}} = \begin{pmatrix}
\frac{\partial y}{\partial x_{11}} & \frac{\partial y}{\partial x_{21}} & \cdots & \frac{\partial y}{\partial x_{n1}} \\
\vdots & \vdots & \vdots & \vdots \\
\frac{\partial y}{\partial x_{1m}} & \frac{\partial y}{\partial x_{2m}} & \cdots & \frac{\partial y}{\partial x_{nm}}
\end{pmatrix}
$$

The output is a matrix of size $[m \times n]$.

**Tutor Response R**

If the original matrix **X** has element $x_{ij}$ at row $i$ and column $j$, where exactly does $\frac{\partial y}{\partial x_{ij}}$ appear in the resulting $[m \times n]$ output matrix, and what does that tell you about how the rows and columns are being reorganized?

> **Row 22** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *accurate* &nbsp;·&nbsp; row 23

**Context C**

Formally, we define a state machine as $(\mathcal{S},\mathcal{X},\mathcal{Y},\mathfrak{s}_0,\mathfrak{f},\mathfrak{q})$ where

- $S$ is a finite or infinite set of possible states;
- $\mathcal{X}$ is a finite or infinite set of possible inputs;
- $\mathcal{Y}$ is a finite or infinite set of possible outputs;
- $s_0 \in S$ is the initial state of the machine;
- $f: S \times \mathcal{X} \to S$ is a transition function, which takes an input and a previous state and produces a next state;

**Tutor Response R**

Given that the transition function f maps from S × X to S, what do you think would happen to the machine's behavior if the transition function could only use the input, without any knowledge of the current state?

> **Row 23** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *accurate* &nbsp;·&nbsp; row 24

**Context C**

Now, given a data set and the hypothesis class of linear classifiers, our objective will be to find the linear classifier with the smallest possible training error.

This is a well-formed optimization problem. But it's not computationally easy!

We'll start by considering a very simple learning algorithm. The idea is to generate  $k$  possible hypotheses by generating their parameter vectors at random. Then, we can evaluate the training-set error on each of the hypotheses and return the hypothesis that has the lowest training error (breaking ties arbitrarily).

It's a good idea to think of the "stupidest possible" solution to a problem, before trying to get clever. Here's a fairly (but not completely) stupid algorithm.

**Tutor Response R**

Given that we're evaluating each hypothesis by its training error, what specific aspect of this random generation approach might make it computationally challenging, especially as the number of possible hypotheses grows?

> **Row 24** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *accurate* &nbsp;·&nbsp; row 25

**Context C**

Example: Let  $h$  be the linear classifier defined by  $\theta = \begin{bmatrix} 1 \\ -1 \end{bmatrix}, \theta_0 = 1$ .

The diagram below shows several points classified by  $h$ , one of which is misclassified. We compute the margin for each point:

$$
y ^ {(1)} \cdot \frac {\theta^ {T} x ^ {(1)} + \theta_ {0}}{\| \theta \|} = 1 \cdot \frac {- 2 + 1}{\sqrt {2}} = - \frac {\sqrt {2}}{2}
$$

$$
y ^ {(2)} \cdot \frac {\theta^ {T} x ^ {(2)} + \theta_ {0}}{\| \theta \|} = 1 \cdot \frac {1 + 1}{\sqrt {2}} = \sqrt {2}
$$

$$
y ^ {(3)} \cdot \frac {\theta^ {T} x ^ {(3)} + \theta_ {0}}{\| \theta \|} = - 1 \cdot \frac {- 3 + 1}{\sqrt {2}} = \sqrt {2}
$$

Note that since point  $x^{(1)}$  is misclassified, its margin is negative. Thus the margin for the whole data set is given by  $-\frac{\sqrt{2}}{2}$ .

**Tutor Response R**

That's a great observation! Given that the margin combines both distance from the boundary and correctness of classification, how does the formula given, $y ^ {(i)} \cdot \frac {\theta^ {T} x ^ {(i)} + \theta_ {0}}{\| \theta \|}$, achieve this?

> **Row 25** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *accurate* &nbsp;·&nbsp; row 26

**Context C**

It only works if batch size is sufficiently big. Suppose your batch size is 1. Then if you have an activation vector $\mathbf{z}$ and subtract the mean over the batch, you get $\mathbf{z} - \mathbf{z} = 0$. The model just zeroed out the activation vector and your net won't work. Worse, the variance is undefined for batch size 1 and that could cause bugs too. For small batch size the variance could be a very poor estimate of the true variance of the activations and cause numerical and optimization issues. [I had this bug in the original version of the pix2pix paper, and it made the baseline work worse than it should have (which might not have been a bad thing for making the paper popular...). See change log in appendix here: https://arxiv.org/abs/1611.07004]

**Tutor Response R**

Given that a batch size of 1 leads to zeroed activations, and small batch sizes can cause unreliable variance estimates, what characteristic should an "optimal" batch size possess to avoid these issues?

> **Row 26** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *erroneous* &nbsp;·&nbsp; rows 27–30

**Context C**

Rather than having just one way of attending, why not have k?

Each gets its own parameterized query(), key(), value() functions.

Run them all in parallel, then (weighted) sum the output token code vectors

$$
\mathbf{T}_{\text{out}}^i = \operatorname{attn}^i(\mathbf{T}_{\text{in}}) \quad \text{for } i \in \{1, \dots, k\}
$$

$$
\bar{\mathbf{T}}_{\text{out}} = \begin{bmatrix} \mathbf{T}_{\text{out}}^1[0,:] &amp; \dots &amp; \mathbf{T}_{\text{out}}^k[0,:] \\ \vdots &amp; \vdots &amp; \vdots \\ \mathbf{T}_{\text{out}}^1[N-1,:] &amp; \dots &amp; \mathbf{T}_{\text{out}}^k[N-1,:] \end{bmatrix} \quad \triangleleft \quad \bar{\mathbf{T}}_{\text{out}} \in \mathbb{R}^{N \times k\nu}
$$

$$
\mathbf{T}_{\text{out}} = \bar{\mathbf{T}}_{\text{out}} \mathbf{W}_{\text{MSA}} \quad \triangleleft \quad \mathbf{W}_{\text{MSA}} \in \mathbb{R}^{k\nu \times d}
$$

**Tutor Response R**

What role does the matrix \(\mathbf{W}_{\text{MSA}}\) play after concatenating the outputs from each head?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 27 | There exists a matrix called W_MSA | |
| 28 | The outputs from multiple heads are concatenated | |
| 29 | W_MSA is applied after the concatenation of head outputs | |
| 30 | W_MSA plays a specific role in the multi-head self-attention mechanism | |

---

## Item — *erroneous* &nbsp;·&nbsp; rows 31–38

**Context C**

How should we evaluate the performance of a learning algorithm? This is trickier. There are many potential sources of variability in the possible result of computing test error on a learned hypothesis $h$:

- Which particular training examples occurred in $\mathcal{D}_n$
- Which particular testing examples occurred in $\mathcal{D}_n$?
- Randomization inside the learning algorithm itself

Generally, we would like to execute the following process multiple times:

- Train on a new training set
- Evaluate resulting $h$ on a testing set that does not overlap the training set

Doing this multiple times controls for possible poor choices of training set or unfortunate randomization inside the algorithm itself.

**Tutor Response R**

How might the variability in training examples or randomization within the learning algorithm affect the reliability of evaluating performance using only one training and testing dataset?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 31 | Training examples can vary across different training datasets | |
| 32 | Learning algorithms may include randomization as part of their process | |
| 33 | Randomization within a learning algorithm can produce different outcomes across runs | |
| 34 | Performance evaluation can be conducted using a single training and testing dataset split | |
| 35 | Using only one training and testing dataset is a method for evaluating model performance | |
| 36 | The variability in training examples or algorithm randomization can affect measured performance | |
| 37 | Reliability of performance evaluation can be impacted by how the data is split | |
| 38 | Evaluating performance on a single dataset split may not produce a reliable estimate of true performance | |

---

## Item — *erroneous* &nbsp;·&nbsp; rows 39–46

**Context C**

This doesn't quite look like an adaptive step size. But what we can see is that, if we let  \(\eta = \eta'(1 - \gamma)\) , then the rule looks exactly like doing an update with step size  \(\eta'\)  on a moving average of the gradients with parameter  \(\gamma\) :

$$
M _ {0} = 0
$$

$$
M _ {t} = \gamma M _ {t - 1} + (1 - \gamma) \nabla_ {W} J (W _ {t - 1})
$$

$$
W _ {t} = W _ {t - 1} - \eta^ {\prime} M _ {t}
$$

**Tutor Response R**

How does the expression \(\eta = \eta'(1 - \gamma)\) suggest that \(\eta\) relates to the step size \(\eta'\) and the parameter \(\gamma\)?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 39 | The expression η = η'(1 - γ) is a mathematical relationship involving three terms | |
| 40 | η is a variable representing something distinct from η' | |
| 41 | η' represents a step size in some iterative or optimization process | |
| 42 | γ is a parameter in the expression η = η'(1 - γ) | |
| 43 | η is defined in terms of η' and γ via the expression η = η'(1 - γ) | |
| 44 | The value of η depends on both η' and γ | |
| 45 | η' and η are related but not equal in general | |
| 46 | The factor (1 - γ) scales η' to produce η | |

---

## Item — *erroneous* &nbsp;·&nbsp; row 47

**Context C**

The idea of gating networks can be applied to make a state-machine that is even more like a computer memory, resulting in a type of network called an LSTM for "long short-term memory." We won't go into the details here, but the basic idea is that there is a memory cell (really, our state vector) and three (!) gating networks. The input gate selects (using a "soft" selection as in the gated network above) which dimensions of the state will be updated with new values; the forget gate decides which dimensions of the state will have its old values moved toward 0, and the output gate decides which dimensions of the state will be used to compute the output value. These networks have been used in applications like language translation with really amazing results.

**Tutor Response R**

Based on what the context describes about the memory cell and the three gating networks, what do you think is the actual role of each gating network — are they storing data themselves, or are they doing something else to control the memory cell?

> **Row 47** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *erroneous* &nbsp;·&nbsp; row 48

**Context C**

Trick #2: Importance sampling

$$
\begin{array}{l}
p_{\theta}(\mathbf{x}) = \mathbb{E}_{\mathbf{z} \sim p_{\mathbf{z}}} \left[ p_{\theta}(\mathbf{x} \mid \mathbf{z}) \right] = \int_{\mathbf{z}} p_{\mathbf{z}}(\mathbf{z}) p_{\theta}(\mathbf{x} \mid \mathbf{z}) d\mathbf{z} = \int_{\mathbf{z}} q_{\mathbf{z}}(\mathbf{z}) \frac{p_{\mathbf{z}}(\mathbf{z})}{q_{\mathbf{z}}(\mathbf{z})} p_{\theta}(\mathbf{x} \mid \mathbf{z}) d\mathbf{z} \\
= \mathbb{E}_{\mathbf{z} \sim q_{\mathbf{z}}} \left[ \frac{p_{\mathbf{z}}(\mathbf{z})}{q_{\mathbf{z}}(\mathbf{z})} p_{\theta}(\mathbf{x} \mid \mathbf{z}) \right]
\end{array}
$$

Set $ q_{\mathbf{z}} = p_{\theta}(Z|\mathbf{x}) $

**Tutor Response R**

If q(z) is set to p_θ(Z|x), what does the ratio p_z(z)/q_z(z) actually simplify to, and does that mean the reweighting term disappears or becomes something more meaningful?

> **Row 48** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *erroneous* &nbsp;·&nbsp; row 49

**Context C**

Proof. We initialize  $\theta^{(0)} = 0$ , and let  $\theta^{(k)}$  define our hyperplane after the perceptron algorithm has made  $k$  mistakes. We are going to think about the angle between the hypothesis we have now,  $\theta^{(k)}$  and the assumed good separator  $\theta^*$ . Since they both go through the origin, if we can show that the angle between them is decreasing usefully on every iteration, then we will get close to that separator.

**Tutor Response R**

What does the proof say the algorithm is actually tracking — and is it directly comparing the hyperplane to the optimal separator, or measuring something else about their relationship?

> **Row 49** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *erroneous* &nbsp;·&nbsp; row 50

**Context C**

One way to handle this is to use experience replay, where we save our $(s, a, r, s')$ experiences in a replay buffer. Whenever we take a step in the world, we add the $(s, a, r, s')$ to the replay buffer and use it to do a Q-learning update. Then we also randomly select some number of tuples from the replay buffer, and do Q-learning updates based on them, as well. In general it may help to keep a sliding window of just the 1000 most recent experiences in the replay buffer. (A larger buffer will be necessary for situations when the optimal policy might visit a large part of the state space, but we like to keep the buffer size small for memory reasons and also so that we don't focus on parts of the state space that are irrelevant for the optimal policy.) The idea is that it will help you propagate reward values through your state space more efficiently if you do these updates. You can see it as doing something like value iteration, but using samples of experience rather than a known model.

**Tutor Response R**

Given the desire to propagate reward values efficiently and the constraints of memory and relevance to the optimal policy, what are the potential downsides of using a very large replay buffer?

> **Row 50** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *erroneous* &nbsp;·&nbsp; row 51

**Context C**

A module  $M$  is “ $(\alpha, \beta, \gamma)$ -sharp” if second derivatives obey:

I.  $\| \triangle w\nabla_w\nabla_wM\triangle \tilde{w}\| _y\leq \alpha *M.\mathrm{norm}(\triangle w)*M.\mathrm{norm}(\triangle \tilde{w})$
II.  $\| \triangle x\nabla_x\nabla_wM\triangle w\| _y\leq \beta *M.\mathrm{norm}(\triangle w)*\| \triangle x\| _\alpha$
III.  $\| \triangle x\nabla_x\nabla_xM\triangle \tilde{x}\| _y\leq \gamma *\| \triangle x\| _\alpha *\| \triangle \tilde{x}\| _\alpha$

**Tutor Response R**

How might the inequalities I, II, and III change if the values of $\alpha$, $\beta$, and $\gamma$ were larger, and what would that imply about the bounds on the second derivatives?

> **Row 51** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *erroneous* &nbsp;·&nbsp; row 52

**Context C**

Input sentence: 李克強此行將啟動中加速殘存,從前頂棲脫。為誰家大總殘存,請各舉行兩個總理首次年度對話. Translation (PBMT): Li Keqiang premier added this line to start the annual dialogue mechanism with the Canadian Prime Minister. Trudixiu two prime ministers held its first annual session. Translation (GMMT): Li Keqiang will start the annual dialogue mechanism with Prime Minister. Trudixiu of Canada and hold the first annual dialogue between the two premiers. Translation (human): Li Keqiang will initiate the annual dialogue mechanism between premiers of China and Canada during the visit, and hold the first annual dialogue with Premier Trudixiu of Canada.

**Tutor Response R**

While all three translations mention the dialogue, do they all specify *who* will be participating in the dialogue and the nature of the dialogue?

> **Row 52** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *comprehension* &nbsp;·&nbsp; rows 53–57

**Context C**

In fact, for different problem settings, we might prefer to pick a different prediction threshold. The field of decision theory considers how to make this choice from the perspective of Bayesian reasoning. For example, if the consequences of predicting  \(+1\)  when the answer should be  \(-1\)  are much worse than the consequences of predicting  \(-1\)  when the answer should be  \(+1\) , then we might set the prediction threshold to be greater than 0.5.

**Tutor Response R**

How does the severity of the consequences influence the decision on where to set the prediction threshold?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 53 | There exists a prediction threshold that can be set | |
| 54 | The prediction threshold can be set at different levels | |
| 55 | Consequences of predictions vary in severity | |
| 56 | The severity of consequences is a factor that influences where the prediction threshold is set | |
| 57 | There is a decision-making process involved in setting the prediction threshold | |

---

## Item — *comprehension* &nbsp;·&nbsp; rows 58–63

**Context C**

Recall that we have a training dataset  $\mathcal{D}_n$  with  $x\in \mathbb{R}^d$ , and  $y\in \{-1, + 1\}$ . The Perceptron algorithm trains a binary classifier  $\mathsf{h}(x;\theta ,\theta_0)$  using the following algorithm to find  $\theta$  and  $\theta_0$  using  $\tau$  iterative steps:

We use Greek letter  $\tau$  here instead of T so we don't confuse it with transpose!

PERCEPTRON(τ, Dn)

1  $\theta = \left[ \begin{array}{llll}0 &amp; 0 &amp; \dots &amp; 0 \end{array} \right]^T$
2  $\theta_0 = 0$
3 for  $t = 1$  to  $\tau$
4 for  $i = 1$  to n
5 if  $y^{(i)}\left(\theta^{\mathrm{T}}x^{(i)} + \theta_0\right)\leqslant 0$
6  $\theta = \theta +y^{(i)}x^{(i)}$
7  $\theta_0 = \theta_0 + y^{(i)}$
8 return  $\theta ,\theta_0$

**Tutor Response R**

How does the condition \( y^{(i)}(\theta^{\mathrm{T}}x^{(i)} + \theta_0) \leq 0 \) relate to the correctness of the prediction for the sample \( x^{(i)} \) with label \( y^{(i)} \)?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 58 | The expression θᵀx⁽ⁱ⁾ + θ₀ represents the decision function or raw score for sample x⁽ⁱ⁾ | |
| 59 | y⁽ⁱ⁾ is a label associated with sample x⁽ⁱ⁾ | |
| 60 | The product y⁽ⁱ⁾(θᵀx⁽ⁱ⁾ + θ₀) being less than or equal to zero has a specific meaning related to classification correctness | |
| 61 | A prediction can be characterized as correct or incorrect based on the sign relationship between the label y⁽ⁱ⁾ and the decision function θᵀx⁽ⁱ⁾ + θ₀ | |
| 62 | The condition y⁽ⁱ⁾(θᵀx⁽ⁱ⁾ + θ₀) ≤ 0 implies the predicted sign disagrees with the true label y⁽ⁱ⁾ | |
| 63 | θ and θ₀ are parameters of a linear classifier | |

---

## Item — *comprehension* &nbsp;·&nbsp; rows 64–67

**Context C**

If you choose to leave a feature as numeric, it is typically useful to scale it, so that it tends to be in the range $[-1, +1]$. Without performing this transformation, if you have one feature with much larger values than another, it will take the learning algorithm a lot of work to find parameters that can put them on an equal basis. So, we might perform transformation $\phi(x) = \frac{x - \overline{x}}{\sigma}$, where $\overline{x}$ is the average of the $x^{(i)}$, and $\sigma$ is the standard deviation of the $x^{(i)}$. The resulting feature values will have mean 0 and standard deviation 1. This transformation is sometimes called standardizing a variable.

**Tutor Response R**

What might be the consequence for the learning algorithm if we don't scale features with different value ranges?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 64 | Features can have different value ranges | |
| 65 | Feature scaling is a technique that can be applied to features with different value ranges | |
| 66 | Not scaling features with different value ranges has a consequence for the learning algorithm | |
| 67 | Learning algorithms are affected by the scale of input features | |

---

## Item — *comprehension* &nbsp;·&nbsp; row 68

**Context C**

Given two modules  $\mathsf{M}_1$  and  $\mathsf{M}_2$  their tuple

$$
M = \left(M _ {1}, M _ {2}\right)
$$

is the module with attributes:

I. M.forward  $= \left(M_{1}.\text{forward},M_{2}.\text{forward}\right)$
II. M.sensitivity  $= \mathsf{M}_1$  .sensitivity  $^+$ $\mathsf{M}_2$  .sensitivity
III. M.mass  $= \mathsf{M}_1$  .mass  $^+$ $\mathsf{M}_2$  .mass
IV. M.norm  $= \max (p*M_1.\text{norm},q*M_2.\text{norm})$

where  $p = M.\text{mass} / M_1.\text{mass}$

$$
q = M. \text {m a s s} / M _ {2}. \text {m a s s}
$$

**Tutor Response R**

What do the values of p and q represent in terms of the masses of M1, M2, and M, and how might that relationship affect which term ends up dominating?

> **Row 68** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *comprehension* &nbsp;·&nbsp; row 69

**Context C**

Example: Let  $h$  be the linear classifier defined by  $\theta = \begin{bmatrix} 1 \\ -1 \end{bmatrix}, \theta_0 = 1$ .

The diagram below shows several points classified by  $h$ , one of which is misclassified. We compute the margin for each point:

$$
y ^ {(1)} \cdot \frac {\theta^ {T} x ^ {(1)} + \theta_ {0}}{\| \theta \|} = 1 \cdot \frac {- 2 + 1}{\sqrt {2}} = - \frac {\sqrt {2}}{2}
$$

$$
y ^ {(2)} \cdot \frac {\theta^ {T} x ^ {(2)} + \theta_ {0}}{\| \theta \|} = 1 \cdot \frac {1 + 1}{\sqrt {2}} = \sqrt {2}
$$

$$
y ^ {(3)} \cdot \frac {\theta^ {T} x ^ {(3)} + \theta_ {0}}{\| \theta \|} = - 1 \cdot \frac {- 3 + 1}{\sqrt {2}} = \sqrt {2}
$$

Note that since point  $x^{(1)}$  is misclassified, its margin is negative. Thus the margin for the whole data set is given by  $-\frac{\sqrt{2}}{2}$ .

**Tutor Response R**

Given that the overall dataset margin is defined as the minimum margin across all points, what does it mean for the classifier's performance when even one point has a negative margin?

> **Row 69** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *comprehension* &nbsp;·&nbsp; row 70

**Context C**

To actually get the dimensions to match, we need to write this a bit more carefully, and note that it is true for any $l$, including $l = L$:

$$
\underbrace {\frac {\partial \operatorname {l o s s}}{\partial W ^ {L}}} _ {m ^ {1} \times n ^ {1}} = \underbrace {A ^ {L - 1}} _ {m ^ {1} \times 1} \underbrace {\left(\frac {\partial \operatorname {l o s s}}{\partial Z ^ {L}}\right) ^ {T}} _ {l \times n ^ {1}} \tag {8.1}
$$

**Tutor Response R**

What are the specific dimensions of each term in the equation — $A^{L-1}$, $\left(\frac{\partial \operatorname{loss}}{\partial Z^L}\right)^T$, and the resulting $\frac{\partial \operatorname{loss}}{\partial W^L}$ — and how do those dimensions relate to the sizes $m^l$ and $n^l$ indicated in the equation?

> **Row 70** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *comprehension* &nbsp;·&nbsp; row 71

**Context C**

Now, we can use methods that are a bit like running averages to describe strategies for computing  \(\eta\) . The simplest method is momentum, in which we try to "average" recent gradient updates, so that if they have been bouncing back and forth in some direction, we take out that component of the motion. For momentum, we have

$$
V _ {0} = 0
$$

$$
V _ {t} = \gamma V _ {t - 1} + \eta \nabla_ {W} J (W _ {t - 1})
$$

$$
W _ {t} = W _ {t - 1} - V _ {t}
$$

**Tutor Response R**

Given that \(V_t\) is a weighted average of the previous velocity and the current gradient, how does the hyperparameter \(\gamma\) (gamma) control the influence of past gradients on the current update direction?

> **Row 71** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *comprehension* &nbsp;·&nbsp; row 72

**Context C**

An alternative strategy for learning the Q function that is somewhat more robust than the standard Q-learning algorithm is a method called fitted Q.

FITTED-Q-LEARNING(A, s₀, γ, α, ε, m)

1.  $s = s_0$ // Or draw an s randomly from S
2.  $\mathcal{D} = \{\}$
3.  initialize neural-network representation of Q
4.  while True:
5.  $\mathcal{D}_{\mathrm{new}} =$ experience from executing $\epsilon$-greedy policy based on Q for m steps
6.  $\mathcal{D} = \mathcal{D} \cup \mathcal{D}_{\mathrm{new}}$ represented as $(s, a, r, s')$ tuples
7.  $\mathsf{D}_{\mathrm{sup}} = \{(x^{(i)},y^{(i)}))$ where $x^{(i)} = (s,a)$ and $y^{(i)} = r + \gamma \max_{a'\in A}Q(s',a')$
8.  for each tuple $(s,a,r,s')^{(i)}\in \mathcal{D}$
9.  re-initialize neural-network representation of Q
10. Q = supervised_NN_regression(Dsup)

Here, we alternate between using the policy induced by the current Q function to gather a batch of data $\mathcal{D}_{\mathrm{new}}$, adding it to our overall data set $\mathcal{D}$, and then using supervised neural-network training to learn a representation of the Q value function on the whole data set. This method does not mix the dynamic-programming phase (computing new Q values based on old ones) with the function approximation phase (training the neural network) and avoids catastrophic forgetting.

**Tutor Response R**

That's a great summary!

Given that $\mathcal{D}_{\mathrm{sup}}$ is used to train the neural network, how does the algorithm use the data tuples $(s, a, r, s')$ to construct the input-output pairs $(x^{(i)}, y^{(i)})$ for supervised learning?

> **Row 72** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *comprehension* &nbsp;·&nbsp; row 73

**Context C**

Now, we'll look at the second factor in equation 3.1. We note that since  $(x^{(i)},y^{(i)})$  is classified incorrectly,  $y^{(i)}\left(\theta^{(k - 1)^T}x^{(i)}\right)\leqslant 0$ . Thus,

$$
\begin{array}{l} \left\| \theta^ {(k)} \right\| ^ {2} = \left\| \theta^ {(k - 1)} + y ^ {(i)} x ^ {(i)} \right\| ^ {2} \\ = \left\| \theta^ {(k - 1)} \right\| ^ {2} + 2 y ^ {(i)} \theta^ {(k - 1) ^ {\mathrm {T}}} x ^ {(i)} + \left\| x ^ {(i)} \right\| ^ {2} \\ \leqslant \left\| \theta^ {(k - 1)} \right\| ^ {2} + R ^ {2} \\ \leqslant k R ^ {2} \\ \end{array}
$$

where we have additionally applied the assumption from (b) and then again used simple induction.

**Tutor Response R**

How does the condition \(y^{(i)}(\theta^{(k-1)^T}x^{(i)}) \leq 0\) contribute to the bound on the norm of the updated parameter vector?

> **Row 73** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *confusion* &nbsp;·&nbsp; rows 74–78

**Context C**

Given two modules  $\mathsf{M}_1$  and  $\mathsf{M}_2$  their tuple

$$
M = \left(M _ {1}, M _ {2}\right)
$$

is the module with attributes:

I. M.forward  $= \left(M_{1}.\text{forward},M_{2}.\text{forward}\right)$
II. M.sensitivity  $= \mathsf{M}_1$  .sensitivity  $^+$ $\mathsf{M}_2$  .sensitivity
III. M.mass  $= \mathsf{M}_1$  .mass  $^+$ $\mathsf{M}_2$  .mass
IV. M.norm  $= \max (p*M_1.\text{norm},q*M_2.\text{norm})$

where  $p = M.\text{mass} / M_1.\text{mass}$

$$
q = M. \text {m a s s} / M _ {2}. \text {m a s s}
$$

**Tutor Response R**

What might be the reason for combining the sensitivities of two modules by simply adding them, considering how attributes might accumulate or interact in a system?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 74 | Two modules each have a sensitivity value | |
| 75 | The sensitivities of two modules can be combined into a single value | |
| 76 | One method of combining the two sensitivities is by adding them | |
| 77 | Attributes can accumulate or interact within a system | |
| 78 | The way attributes accumulate or interact provides a rationale for choosing addition as the combination operation | |

---

## Item — *confusion* &nbsp;·&nbsp; rows 79–82

**Context C**

Now, let's figure out how to do backprop. We can start schematically: $$ \frac{\partial L}{\partial Z} = \frac{\partial L}{\partial \widetilde{Z}} \frac{\partial \widetilde{Z}}{\partial Z}. $$ And because dependencies only exist across the batch, but not across the unit outputs, $$ \frac{\partial L}{\partial Z_{ij}} = \sum_{k=1}^{K} \frac{\partial L}{\partial \widetilde{Z}_{ik}} \frac{\partial \widetilde{Z}_{ik}}{\partial Z_{ij}}. $$

**Tutor Response R**

What do you think happens to the gradient calculations if the outputs of different units are independent from each other?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 79 | gradient calculations exist in the context being discussed | |
| 80 | neural network or similar systems have multiple units with outputs | |
| 81 | the independence or dependence of unit outputs affects gradient calculations | |
| 82 | unit outputs can vary in their degree of independence from each other | |

---

## Item — *confusion* &nbsp;·&nbsp; rows 83–87

**Context C**

A Markov decision process (MDP) is a variation on a state machine in which:

- The transition function is stochastic, meaning that it defines a probability distribution over the next state given the previous state and input, but each time it is evaluated it draws a new state from that distribution.
- The output is equal to the state (that is $g$ is the identity function).
- Some states (or state-action pairs) are more desirable than others.

An MDP can be used to model interaction with an outside "world," such as a single-player game.

We will focus on the case in which $S$ and $\mathcal{X}$ are finite, and will call the input set $\mathcal{A}$ for actions (rather than $\mathcal{X}$). The idea is that an agent (a robot or a game-player) can model its environment as an MDP and try to choose actions that will drive the process into states that have high scores.

Formally, an MDP is $\langle S, \mathcal{A}, T, R, \gamma \rangle$ where:

- $T: S \times \mathcal{A} \times S \to \mathbb{R}$ is a transition model, where

$$
T(s, a, s') = P(S_t = s' | S_{t-1} = s, A_{t-1} = a),
$$

specifying a conditional probability distribution;

- $R: S \times \mathcal{A} \to \mathbb{R}$ is a reward function, where $R(s, a)$ specifies how desirable it is to be in state $s$ and take action $a$; and
- $\gamma \in [0,1]$ is a discount factor, which we'll discuss in section 2.2.

A policy is a function $\pi: S \to \mathcal{A}$ that specifies what action to take in each state.

**Tutor Response R**

How might the desirability of a state change based on the action you take in that state?

**Presuppositions — enter your verdict in the CSV**

| Row ID | Presupposition | YOUR\_VERDICT *(fill in CSV)* |
|--------|----------------|-------------------------------|
| 83 | A state has a property called desirability | |
| 84 | The desirability of a state can change | |
| 85 | Actions can be taken in a state | |
| 86 | The action taken in a state can affect the desirability of that state | |
| 87 | Different actions in the same state can lead to different desirability values for that state | |

---

## Item — *confusion* &nbsp;·&nbsp; row 88

**Context C**

The weights are the values defining the filter: there will be $m^l$ different $k^l \times k^l \times m^{l-1}$ tensors of weight values; plus each filter may have a bias term, which means there is one more weight value per filter. A filter with a bias operates just like the filter examples above, except we add the bias to the output. For instance, if we incorporated a bias term of 0.5 into the filter $F_2$ above, the output would be $(-0.5, 0.5, -0.5, 0.5, -1.5, 1.5, -0.5, 0.5)$ instead of $(-1, 0, -1, 0, -2, 1, -1, 0)$.

**Tutor Response R**

Looking at the example in the context, where adding a bias of 0.5 to filter F₂ changes every single element of the output — for instance, the first element goes from -1 to -0.5, and the second from 0 to 0.5 — what pattern do you notice about how each output value was affected by that 0.5 bias?

> **Row 88** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *confusion* &nbsp;·&nbsp; row 89

**Context C**

How does the test loss scale as a function of data, #parameters etc?

- autoregressive Transformer
- data: WebText2, 96GB of text, $2.29 \cdot 10^{10}$ tokens
1024 token context
- vary:
- model size: 768 - 1.5 billion non-embedding parameters
- data: 22M - 23B tokens
- shape (depth, with, attention heads, ...)
- batch size
- compute = 6 x #parameters x batchsize x #steps
- computation: in PF-days (petaflop/s-days)
1 PF-day = $8.64 \cdot 10^{19}$ FLOPs

**Tutor Response R**

What do you think would happen to the test loss if you took a fixed amount of compute and spent it all on a very large model trained on very few data tokens, versus a smaller model trained on many more tokens?

> **Row 89** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *confusion* &nbsp;·&nbsp; row 90

**Context C**

Now, we can use methods that are a bit like running averages to describe strategies for computing  \(\eta\) . The simplest method is momentum, in which we try to "average" recent gradient updates, so that if they have been bouncing back and forth in some direction, we take out that component of the motion. For momentum, we have

$$
V _ {0} = 0
$$

$$
V _ {t} = \gamma V _ {t - 1} + \eta \nabla_ {W} J (W _ {t - 1})
$$

$$
W _ {t} = W _ {t - 1} - V _ {t}
$$

**Tutor Response R**

What happens when you substitute V₀ = 0 into the formula for V₁, and how does that compare to a standard gradient update step?

> **Row 90** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *confusion* &nbsp;·&nbsp; row 91

**Context C**

Our theoretical results completely characterize shortcut solutions, whereby a shallow Transformer with only  $o(T)$  layers can exactly replicate the computation of an automaton on an input sequence of length  $T$ . By representing automata using the algebraic structure of their underlying transformation semigroups, we obtain  $O(\log T)$ -depth simulators for all automata and $O(1)$ -depth simulators for all automata whose associated groups are sc synthetic experiments by training Transformers to simulate a wide var shortcut solutions can be learned via standard training.

**Tutor Response R**

Given that the text mentions "O(1)-depth simulators for all automata whose associated groups are," what does "O(1)" (Big O notation of 1) typically imply about the relationship between depth and the input size T?

> **Row 91** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *confusion* &nbsp;·&nbsp; row 92

**Context C**

Another common strategy is to simply penalize the norm of all the weights, as we did in ridge regression. This method is known as weight decay, because when we take the gradient of the objective

$\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$

we end up with an update of the form

$W_{t}$ $=W_{t-1}-\eta\left(\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)+\lambda W_{t-1}\right)$
$=W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)\enspace.$

This rule has the form of first “decaying” $W_{t-1}$ by a factor of $(1-\lambda\eta)$ and then taking a gradient step.

**Tutor Response R**

How does the equation $W_{t} =W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)$ relate to the gradient of the objective function $\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$?

> **Row 92** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---

## Item — *confusion* &nbsp;·&nbsp; row 93

**Context C**

Hinge loss gives us another way, for binary classification problems, to make a smoother objective, penalizing the margins of the labeled points relative to the separator. The hinge loss is defined to be $$ \mathcal {L} _ {\mathrm {h}} (\text {g u e s s}, \text {a c t u a l}) = \max  (1 - \text {g u e s s} \cdot \text {a c t u a l}, 0), $$ when  $\text{actual} \in \{+1, -1\}$ . It has the property that, if the sign of guess is the same as the sign of actual and the magnitude of guess is greater than 1, then the loss is 0.

**Tutor Response R**

Consider the two cases where the signs match and where they don't. In which of those cases does increasing the magnitude of the `guess` *decrease* the loss?

> **Row 93** — No presuppositions extracted (vacuous response). Mark `N/A` in YOUR\_VERDICT.

---
