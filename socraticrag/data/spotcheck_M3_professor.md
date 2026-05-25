# M3 Spot-Check — Pedagogical Alignment

> **How to view formulas:** paste this file into [https://markdownlivepreview.dev/](https://markdownlivepreview.dev/) and all math will render automatically.

> **How to fill in:** open `spotcheck_M3_professor.csv` in Google Sheets and enter your scores in **YOUR\_P**, **YOUR\_O**, **YOUR\_E** for each row ID.

> **Scoring rubric (0–3 per dimension)**
>
> | Score | Perception *(reads student state)* | Orchestration *(manages response)* | Elicitation *(draws student out)* |
> |-------|-----------------------------------|-----------------------------------|-----------------------------------|
> | 0 | Ignores cognitive state | Directly gives answer | Closed yes/no or rhetorical |
> | 1 | Acknowledges but misreads | Hints but gives too much | Leads toward one answer |
> | 2 | Correctly identifies state | Scaffolds appropriately | Open, invites reasoning |
> | 3 | Identifies + adapts strategy | Fully withholds, guides only | Probes deeper, extends thinking |

---

## Row 1 — *accurate* &nbsp;·&nbsp; matrix transformation and redundancy

**Context C**

Study Question: Imagine  $k = 3$ . If we were to take the matrix  $U$  and multiply the first column by 2, the second column by 3 and the third column by 4, to make a new matrix  $U'$ , what would we have to do to  $V$  to get a  $V'$  so that  $U'V'^{\mathrm{T}} = UV^{\mathrm{T}}$ ? How does this question relate to the comments above about redundancy?

**Student Utterance**

If we multiply the first column of U by 2, the second by 3, and the third by 4, we need to divide the corresponding rows of V by 2, 3, and 4 respectively to keep U'V'^{T} equal to UV^{T}. This shows how changes in U can be compensated by changes in V, preventing redundancy in the transformation.

**Tutor Response**

What effect does multiplying a column of matrix U by a constant have on the corresponding elements in the product \( UV^{\mathrm{T}} \)?

**Enter your scores in the CSV for row 1**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 2 — *accurate* &nbsp;·&nbsp; gradient of the loss with respect to the pre-activation in the first layer

**Context C**

If we repeatedly apply the chain rule, we get this expression for the gradient of the loss with respect to the pre-activation in the first layer:

$$
\frac {\partial \text {l o s s}}{\partial Z ^ {1}} = \underbrace {\underbrace {\frac {\partial \text {l o s s}}{\partial A ^ {L}} \cdot \frac {\partial A ^ {L}}{\partial Z ^ {L}} \cdot \frac {\partial Z ^ {L}}{\partial A ^ {L - 1}} \cdot \frac {\partial A ^ {L - 1}}{\partial Z ^ {L - 1}} \cdots \cdot \frac {\partial A ^ {2}}{\partial Z ^ {2}} \cdot \frac {\partial Z ^ {2}}{\partial A ^ {1}} \cdot \frac {\partial A ^ {1}}{\partial Z ^ {1}}} _ {\partial \text {l o s s} / \partial Z ^ {2}}, \tag {8.2}
$$

**Student Utterance**

So, to find the gradient of the loss with respect to the pre-activation in the first layer, we need to apply the chain rule starting from the last layer and work our way back to the first, right?

**Tutor Response**

What role does each term in the chain rule expression play as you move from the last layer to the first layer?

**Enter your scores in the CSV for row 2**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 3 — *erroneous* &nbsp;·&nbsp; gradient computation using the chain rule

**Context C**

(4) Do backward pass to compute the gradients. For both $W^{\mathrm{sx}}$ and $W^{\mathrm{sx}}$ we need to find

$$
\frac {\mathrm {d} L _ {\text {s e q}}}{\mathrm {d} W} = \sum_ {u = 1} ^ {n} \frac {\mathrm {d} L _ {u}}{\mathrm {d} W} \tag {12.1}
$$

Letting $L_{u} = L_{\mathrm{elt}}(p_{u},y_{u})$ and using the total derivative, which is a sum over all the ways in which $W$ affects $L_{u}$, we have

$$
= \sum_ {u = 1} ^ {n} \sum_ {t = 1} ^ {n} \frac {\partial L _ {u}}{\partial s _ {t}} \cdot \frac {\partial s _ {t}}{\partial W} \tag {12.2}
$$

Re-organizing, we have

$$
= \sum_ {t = 1} ^ {n} \frac {\partial s _ {t}}{\partial W} \cdot \sum_ {u = 1} ^ {n} \frac {\partial L _ {u}}{\partial s _ {t}} \tag {12.3}
$$

**Student Utterance**

I think we can find the gradient of the loss with respect to W by just taking the derivative of the loss function directly with respect to W, without worrying about the sequence elements.

**Tutor Response**

How does the chain rule apply when $W$ affects the loss through intermediate variables like $s_t$ in a sequence?

**Enter your scores in the CSV for row 3**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 4 — *erroneous* &nbsp;·&nbsp; weight decay in neural networks

**Context C**

Another common strategy is to simply penalize the norm of all the weights, as we did in ridge regression. This method is known as weight decay, because when we take the gradient of the objective

$\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$

we end up with an update of the form

$W_{t}$ $=W_{t-1}-\eta\left(\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)+\lambda W_{t-1}\right)$
$=W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)\enspace.$

This rule has the form of first “decaying” $W_{t-1}$ by a factor of $(1-\lambda\eta)$ and then taking a gradient step.

**Student Utterance**

Weight decay just means we penalize the weights by reducing them, so there's no need for a gradient step in the update process.

**Tutor Response**

How does the gradient step contribute to the update process when combined with the weight decay term?

**Enter your scores in the CSV for row 4**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 5 — *comprehension* &nbsp;·&nbsp; forward pass in a neural network

**Context C**

For simplicity assume  $k$  is odd, let the input image  $X = A^0$ , and assume we are using squared loss. Then we can describe the forward pass as follows:

$$
\begin{array}{l} Z _ {i} ^ {1} = W ^ {1} ^ {T} \cdot A _ {[ i - \lfloor k / 2 \rfloor : i + \lfloor k / 2 \rfloor ]} ^ {0} \\ A ^ {1} = \operatorname {R e L U} \left(Z ^ {1}\right) \\ A ^ {2} = W ^ {2} ^ {T} A ^ {1} \\ \mathrm {L} \left(\mathrm {A} ^ {2}, \mathrm {y}\right) = \left(\mathrm {A} ^ {2} - \mathrm {y}\right) ^ {2} \\ \end{array}
$$

**Student Utterance**

Ah, I see — the forward pass involves calculating the intermediate values using weights and applying the ReLU activation before computing the final output with squared loss.

**Tutor Response**

How does the ReLU activation function affect the values in the forward pass?

**Enter your scores in the CSV for row 5**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 6 — *comprehension* &nbsp;·&nbsp; linear separability

**Context C**

Consider the data set:

\[
\begin{array}{l}
X = [[1], [2], [3], [4]] \\
Y = [[+1], [+1], [-1], [-1]]
\end{array}
\]

It is linearly separable in \(d = 1\) with \(\theta = [-1]\) and \(\theta_0 = 2.5\). But it is not linearly separable through the origin! Now, let

\[
X_{\text{new}} = \left[ \begin{array}{ll} [1] & [2] \\ [1] & [3] \\ [1] & [4] \end{array} \right]
\]

This new dataset is separable through the origin, with \(\theta_{\text{new}} = [-1, 2.5]^{\mathrm{T}}\).

**Student Utterance**

Ah, I see — the original dataset isn't linearly separable through the origin because the decision boundary doesn't pass through zero, but when we extend X with an extra dimension, it becomes separable through the origin with the new theta.

**Tutor Response**

How does adding an extra dimension to the original dataset affect the position of the data points relative to the decision boundary?

**Enter your scores in the CSV for row 6**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 7 — *confusion* &nbsp;·&nbsp; sequence-to-sequence training with special tokens

**Context C**

A language model is just trained on a set of input sequences, \((c_{1}^{(i)}, c_{2}^{(i)}, \ldots, c_{n^{(i)}})\), and is used to predict the next character, given a sequence of previous tokens:

A "token" is generally a character or a word.

$$
c _ {t} = \operatorname {R N N} \left(c _ {1}, c _ {2}, \dots , c _ {t - 1}\right)
$$

We can convert this to a sequence-to-sequence training problem by constructing a data set of \((x, y)\) sequence pairs, where we make up new special tokens, start and end, to signal the beginning and end of the sequence:

$$
x = (\langle \text {s t a r t} \rangle , c _ {1}, c _ {2}, \cdot c _ {n})
$$

$$
y = \left(c _ {1}, c _ {2}, \dots , \langle \text {e n d} \rangle\right)
$$

**Student Utterance**

I'm confused about how the RNN is able to predict the next character when special tokens are included. Does it treat these tokens differently from the other characters?

**Tutor Response**

How do you think the inclusion of the special tokens, such as "start" and "end", helps the RNN understand where the sequence begins and ends?

**Enter your scores in the CSV for row 7**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 8 — *confusion* &nbsp;·&nbsp; triplet loss

**Context C**

Triplet loss (Schroff et al 2015): $$ \mathcal{L}_{\text{triplet}}(\mathbf{x}, \mathbf{x}^+, \mathbf{x}^-) = \sum_{\mathbf{x} \in \mathcal{X}} \max \left(0, \underbrace{\|f(\mathbf{x}) - f(\mathbf{x}^+)\|_2^2}_{\text{margin}} - \underbrace{\|f(\mathbf{x}) - f(\mathbf{x}^-)\|_2^2}_{\text{margin}} + \epsilon\right) $$

**Student Utterance**

I'm confused about the role of 'margin' in the equation. Why is it mentioned twice, and how does it relate to the epsilon?

**Tutor Response**

How does comparing the distance between the anchor and positive example to the distance between the anchor and negative example help in understanding what the margin represents in this context?

**Enter your scores in the CSV for row 8**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 9 — *accurate* &nbsp;·&nbsp; Perceptron algorithm update rule

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

**Student Utterance**

I understand that the Perceptron algorithm updates the weights and bias only when there's a misclassification, meaning when y(i)(θᵀx(i) + θ₀) is less than or equal to zero. So, it doesn't update on every loop iteration, right?

**Tutor Response**

Given that the condition on line 5 triggers updates when the value is "less than or equal to zero," what do you think happens specifically when the value equals exactly zero — is that a correct classification or an incorrect one?

**Enter your scores in the CSV for row 9**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 10 — *accurate* &nbsp;·&nbsp; perceptron algorithm through the origin

**Context C**

We can make a simplified version of the perceptron algorithm if we restrict ourselves to separators through the origin:

PERCEPTRON-THROUGH-ORIGIN \((\tau, \mathcal{D}_n)\)

1. \(\theta = \left[ \begin{array}{llll}0 & 0 & \dots & 0 \end{array} \right]^{\mathrm{T}}\)
2. for \(t = 1\) to \(\tau\)
3. for \(i = 1\) to \(n\)
4. if \(y^{(i)}\left(\theta^{\mathrm{T}}x^{(i)}\right) \leqslant 0\)
5. \(\theta = \theta + y^{(i)}x^{(i)}\)
6. return \(\theta\)

We list it here because this is the version of the algorithm we'll study in more detail.

**Student Utterance**

I see that the perceptron through the origin only updates the weight vector when the product of the label and the dot product is non-positive. So, it only changes when there's a misclassification, right?

**Tutor Response**

What does it mean for the product y^(i)(θ^T x^(i)) to equal exactly zero — is that a misclassification, a correct classification, or something else?

**Enter your scores in the CSV for row 10**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 11 — *accurate* &nbsp;·&nbsp; representation of sparse data in tuples

**Context C**

Y is very sparse (most entries are empty). So, we will think of our training data-set as a set of tuples \(\{(a,i,r)\}\), where \(a\) is the index assigned to a particular user, \(i\) is the index assigned to a particular movie, and \(r\) is user \(a\)'s rating of movie \(i\). We will use \(D = \{(a,i):Y_{ai} \text{ is non-empty}\}\) as the set of indices for which we have a rating.

**Student Utterance**

So, if I understand correctly, our dataset only includes tuples for the user-movie pairs where a rating is actually given, and we ignore all the pairs without ratings?

**Tutor Response**

Given that \(D\) represents the set of all user-movie pairs with known ratings, how does focusing on \(D\) help us manage the sparsity of \(Y\)?

**Enter your scores in the CSV for row 11**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 12 — *accurate* &nbsp;·&nbsp; random linear classifier selection

**Context C**

RANDOM-LINEAR-CLASSIFIER$(\mathcal{D}_n, k, d)$

1. for $j = 1$ to $k$
2. randomly sample $(\theta^{(j)},\theta_0^{(j)})$ from $(\mathbb{R}^d,\mathbb{R})$
3. $j^{*} = \arg \min_{j\in \{1,\dots ,k\}}\mathcal{E}_{n}(\theta^{(j)},\theta_{0}^{(j)})$
4. return $(\theta^{(j^{*})},\theta_{0}^{(j^{*})})$

**Student Utterance**

So, the algorithm tries out several random classifiers and picks the one that performs best on our data, right?

**Tutor Response**

That's a good summary. Given that the algorithm iterates through each classifier $j$ from 1 to $k$, what is being computed in step 3, $j^{*} = \arg \min_{j\in \{1,\dots ,k\}}\mathcal{E}_{n}(\theta^{(j)},\theta_{0}^{(j)})$?

**Enter your scores in the CSV for row 12**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 13 — *erroneous* &nbsp;·&nbsp; cross-entropy for softmax classifier

**Context C**

Cross-entropy for softmax "classifier"

$$
\min _ {f} \mathbb {E} _ {(\mathbf {x}, \mathbf {x} ^ {+}) ^ {\cdot}} p _ {p o s}, \{\mathbf {x} _ {i} ^ {-} \} _ {i = 1} ^ {N} p _ {d a t a} \left[ - \log \frac {e ^ {f (\mathbf {x}) ^ {\cdot} f (\mathbf {x} ^ {+}) / \sim}}{e ^ {f (\mathbf {x}) ^ {\cdot} f (\mathbf {x} ^ {+}) / \sim} + \sqrt {\frac {N}{i = 1}} e ^ {f (\mathbf {x}) ^ {\cdot} f (\mathbf {x} _ {i} ^ {-}) / \sim}} \right] \begin{array}{l} \text {pull positive} \\ \text {pair together} \\ \text {push negative} \\ \text {pairs apart} \end{array}
$$

**Student Utterance**

It seems like the formula is telling us to divide by some constant '/~', which I thought was a standard operation to normalize the scores. Is that correct?

**Tutor Response**

Looking at the formula, what do you notice about where the '/~' symbol appears — does it show up only in the denominator as a normalizer, or does it appear in both the numerator and the denominator, and what might that suggest about its role?

**Enter your scores in the CSV for row 13**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 14 — *erroneous* &nbsp;·&nbsp; temporal difference learning

**Context C**

Note that the update can be rewritten as

$$
Q [ s, a ] = Q [ s, a ] - \alpha \left(Q [ s, a ] - (r + \gamma \max  _ {a ^ {\prime}} Q [ s ^ {\prime}, a ^ {\prime} ])\right),
$$

which looks something like a gradient update! This is often called temporal difference learning method, because we make an update based on the difference between the current estimated value of taking action a in state s, which is Q[s, a], and the "one-step" sampled value of taking a in s, which is r + γ max_a · Q[s', a'].

**Student Utterance**

So, temporal difference learning is just like gradient descent since it updates the Q-values using a similar formula, right?

**Tutor Response**

What specifically is being subtracted from Q[s, a] in this update formula, and how does that difference relate to what "temporal" means in "temporal difference learning"?

**Enter your scores in the CSV for row 14**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 15 — *erroneous* &nbsp;·&nbsp; quality measurement of reinforcement-learning algorithms

**Context C**

A *reinforcement-learning* (rl) *algorithm* is a kind of a policy that depends on the whole history of states, actions, and rewards and selects the next action to take. There are several different ways to measure the quality of an rl algorithm, including:

- Ignoring the $r_{t}$ values that it gets *while* learning, but consider how many interactions with the environment are required for it to learn a policy $ pi: mathcal{S} rightarrow mathcal{A}$ that is nearly optimal.
- Maximizing the expected discounted sum of total rewards while it is learning.

**Student Utterance**

I think the main way to measure a reinforcement-learning algorithm's quality is by how fast it can learn a nearly optimal policy, and the rewards it gets during learning don't really matter.

**Tutor Response**

The context describes two ways to measure the quality of an RL algorithm. Does your statement align with both of those ways?

**Enter your scores in the CSV for row 15**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 16 — *erroneous* &nbsp;·&nbsp; stochastic gradient descent for matrix factorization

**Context C**

Finally, we can approach this problem using stochastic gradient descent. It's easier to think about if we reorganize the objective function to be $$ J (U, V) = \frac {1}{2} \sum_ {(a, i) \in D} \left(\left(U ^ {(a)} \cdot V ^ {(i)} + b _ {U} ^ {(a)} + b _ {V} ^ {(i)} - Y _ {a i}\right) ^ {2} + \lambda_ {U} ^ {(a)} \left\| U ^ {(a)} \right\| ^ {2} + \lambda_ {V} ^ {(i)} \left\| V ^ {(i)} \right\| ^ {2}\right) $$

**Student Utterance**

So, using stochastic gradient descent, we're just trying to minimize the prediction error in J(U, V), right? The regularization terms don't really affect the process.

**Tutor Response**

How does the presence of the regularization terms, $$ \lambda_ {U} ^ {(a)} \left\| U ^ {(a)} \right\| ^ {2} + \lambda_ {V} ^ {(i)} \left\| V ^ {(i)} \right\| ^ {2}$$, influence the overall value of J(U, V) that we are trying to minimize?

**Enter your scores in the CSV for row 16**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 17 — *comprehension* &nbsp;·&nbsp; distance metric properties

**Context C**

Input values $x$ can be from any domain $\mathcal{X}$ ($\mathbb{R}^d$, documents, tree-structured objects, etc.). We just need a distance metric, $d: \mathcal{X} \times \mathcal{X} \to \mathbb{R}^+$, which satisfies the following, for all $x, x', x'' \in \mathcal{X}$:

$$
\begin{array}{l}
d(x, x) = 0 \\
d(x, x') = d(x', x) \\
d(x, x'') \leqslant d(x, x') + d(x', x'')
\end{array}
$$

**Student Utterance**

Ah, I see — the distance metric properties mean that the distance between any point and itself is always zero, and the distance from one point to another is the same in reverse.

**Tutor Response**

What does the third property tell you about the relationship between the direct distance from one point to another and the distance traveled through an intermediate point?

**Enter your scores in the CSV for row 17**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 18 — *comprehension* &nbsp;·&nbsp; Batch normalization with learnable parameters

**Context C**

However, if we let these be our $\widetilde{Z}^1$ values, we really are forcing something too strong on our data—our goal was to normalize across the data batch, but not necessarily force the output values to have exactly mean 0 and standard deviation 1. So, we will give the layer the "opportunity" to shift and scale the outputs by adding new weights to the layer. These weights are $G^1$ and $B^1$, each of which is an $n^1 \times 1$ vector. Using the weights, we define the final output to be $$ \widetilde{Z}_{ij}^1 = G_i^1 \overline{Z}_{ij}^1 + B_i^1. $$

**Student Utterance**

Ah, I see — the batch normalization layer uses weights G^1 and B^1 to adjust the outputs so they aren't strictly mean 0 and standard deviation 1, but instead allow for some flexibility in scaling and shifting.

**Tutor Response**

Given that G^1 and B^1 are learned weights, what do you think would happen to the outputs if G^1 were set to 1 and B^1 were set to 0 for every element?

**Enter your scores in the CSV for row 18**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 19 — *comprehension* &nbsp;·&nbsp; exploration vs. exploitation trade-off

**Context C**

Imagine that you have tried each action 10 times, and now you have an estimate $\hat{p}_1$ for the expected value of $R(a_1)$. Which arm should you pick next? You could

exploit your knowledge, and choose the arm with the highest value of $\hat{p}_1$ on all future trials; or

explore further, by trying some or all actions more times, hoping to get better estimates of the $p_1$ values.

**Student Utterance**

Ah, I see — the exploration vs. exploitation trade-off is about deciding whether to keep picking the arm with the highest estimated value or to try other arms to improve our estimates.

**Tutor Response**

Given that we want to maximize our rewards in the long run, what might be a downside to *only* exploiting the arm with the highest estimated value?

**Enter your scores in the CSV for row 19**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 20 — *comprehension* &nbsp;·&nbsp; backward propagation of gradients in sequences

**Context C**

Let's take a careful look at the backward propagation of the gradient along the sequence:

$$
\delta^ {s _ {t - 1}} = \frac {\partial s _ {t}}{\partial s _ {t - 1}} \cdot \left[ \frac {\partial \operatorname {L o s s} _ {\mathrm {e l t}} \left(p _ {t} , y _ {t}\right)}{\partial s _ {t}} + \delta^ {s _ {t}} \right].
$$

Consider a case where only the output at the end of the sequence is incorrect, but it depends critically, via the weights, on the input at time 1. In this case, we will multiply the loss at step \(n\) by

$$
\frac {\partial s _ {2}}{\partial s _ {1}} \cdot \frac {\partial s _ {3}}{\partial s _ {2}} \dots \frac {\partial s _ {n}}{\partial s _ {n - 1}}.
$$

**Student Utterance**

Ah, I see — the backward propagation of gradients involves multiplying the loss at the final step by all the partial derivatives of each step's state with respect to the previous step's state. This way, we can trace how the error at the end affects the earlier states.

**Tutor Response**

Given that we're multiplying all those partial derivatives together, what might happen if some of those values are either very large or very small?

**Enter your scores in the CSV for row 20**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 21 — *confusion* &nbsp;·&nbsp; recurrent neural networks as non-linear LTI systems

**Context C**

We will study recurrent neural networks which are a lot like a non-linear version of an LTI system, with transition and output functions

$$
f(s, x) = f_1(W^{sx}x + W^{xs}s + W_0^{xs})
$$

$$
g(s) = f_2(W^0s + W_0^0)
$$

defined by weight matrices

$$
W^{sx} : m \times \ell
$$

$$
W^{xs} : m \times m
$$

$$
W_0^{xs} : m \times 1
$$

$$
W^0 : n \times m
$$

$$
W_0^0 : n \times 1
$$

and activation functions $f_1$ and $f_2$. We will see that it's actually possible to learn weight values for a recurrent neural network using gradient descent.

**Student Utterance**

I'm confused about how exactly the weight matrices like W^{sx} and W^{xs} interact with the activation functions f_1 and f_2. How do these components work together in the context of a recurrent neural network?

**Tutor Response**

Looking at the transition function f(s, x) = f_1(W^{sx}x + W^{xs}s + W_0^{xs}), what do you notice about what gets passed as the *input* to the activation function f_1, and how does that input combine information from both the current input x and the previous state s?

**Enter your scores in the CSV for row 21**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 22 — *confusion* &nbsp;·&nbsp; chain rule in backpropagation

**Context C**

$$
\frac {\partial \mathcal {L}}{\partial \mathbf {x} _ {1}} = \frac {\partial \mathcal {L}}{\partial \mathbf {x} _ {2}} \frac {\partial \mathbf {x} _ {2}}{\partial \mathbf {x} _ {1}} = \frac {\partial \mathcal {L}}{\partial \mathbf {x} _ {2}} \frac {\partial \tanh  (\mathbf {x} _ {1})}{\partial \mathbf {x} _ {1}} = \frac {\partial \mathcal {L}}{\partial \mathbf {x} _ {2}} (1 - \tanh  ^ {2} (\mathbf {x} _ {1}))
$$

**Student Utterance**

I'm confused about why we multiply by (1 - tanh^2(x1)) when applying the chain rule. How does that relate to the derivative of tanh(x1)?

**Tutor Response**

What does the chain rule tell us we need to find when computing ∂x₂/∂x₁, and what is x₂ defined as in terms of x₁ in this expression?

**Enter your scores in the CSV for row 22**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 23 — *confusion* &nbsp;·&nbsp; regularization and overfitting

**Context C**

This trade-off is illustrated in the figure below. Hypothesis  $h_1$  has 0 training loss, but is very complicated. Hypothesis  $h_2$  mis-classifies two points, but is very simple. In absence of other beliefs about the solution, it is often better to prefer that the solution be "simpler," and so we might prefer  $h_2$  over  $h_1$ , expecting it to perform better on future examples drawn from this same distribution. Another nice way of thinking about regularization is that we would like to prevent our hypothesis from being too dependent on the particular training data that we were given: we would like for it to be the case that if the training data were changed slightly, the hypothesis would not change by much. To establish some vocabulary, we say that  $h_1$  is overfit to the training data.

**Student Utterance**

I'm confused about why we think h2 will perform better on future examples even though it misclassifies some points. Doesn't zero training loss mean h1 is better?

**Tutor Response**

Given that $h_1$ is very sensitive to the training data, as the text describes, what might happen if future data differs even slightly from the training data?

**Enter your scores in the CSV for row 23**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---

## Row 24 — *confusion* &nbsp;·&nbsp; weight decay in neural networks

**Context C**

Another common strategy is to simply penalize the norm of all the weights, as we did in ridge regression. This method is known as weight decay, because when we take the gradient of the objective

$\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$

we end up with an update of the form

$W_{t}$ $=W_{t-1}-\eta\left(\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)+\lambda W_{t-1}\right)$
$=W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)\enspace.$

This rule has the form of first “decaying” $W_{t-1}$ by a factor of $(1-\lambda\eta)$ and then taking a gradient step.

**Student Utterance**

I'm confused about why we need to decay the weights by (1-λη) before taking the gradient step. What's the purpose of that?

**Tutor Response**

How does the equation $W_{t} =W_{t-1}(1-\lambda\eta)-\eta\left(\nabla_{W}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W_{t-1})\right)$ relate to the gradient of the objective function $\mathrm{J}(W)=\sum_{i=1}^{n}\mathrm{Loss}(\mathrm{NN}(x^{(i)}),y^{(i)};W)+\lambda\|W\|^{2}$?

**Enter your scores in the CSV for row 24**

| Dimension | YOUR Score *(0–3)* |
|-----------|-------------------|
| Perception | |
| Orchestration | |
| Elicitation | |
| **Total** | |

---
