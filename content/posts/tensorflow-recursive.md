Title: Recursive custom gradients in TensorFlow
Date: 2020-12-31 16:00
Tags: tensorflow, gradients
Category: autodifferentiation
Author: Josh Izaac

Most autodifferentiation libraries, such as [PyTorch](https://pytorch.org),
[TensorFlow](https://tensorflow.org), [Autograd](https://github.com/HIPS/autograd)
--- and even [PennyLane](https://pennylane.ai) in the quantum case --- allow you to
create new functions and register *custom gradients* that the autodiff framework
makes use of during backpropagation. This is useful in several cases; perhaps you have
a composite function with a gradient that is more stable than naively applying the
chain rule to all constituent operations, or perhaps the function you would like to
define cannot be written in terms of native framework operations.

While this functionality is super useful, especially in quantum differentiable programming,
it tends to be somewhat under-documented and under-utilized in 'classical' machine learning.
And while most autodiff frameworks provide (small) examples of custom gradients for first
derivatives, there is *very* little information out there for supporting higher-order derivatives.

In fact, if our custom function has periodicity, we can likely define the custom
gradient recursively, and support *arbitrary* nth order derivatives!

Let's imagine a world where TensorFlow accidentally shipped without sine and cosine support,
and see if we can define a custom gradient to support arbitrary nth order derivatives.

## Custom gradients in TensorFlow

So, we've imported TensorFlow, executed `tf.sin()`, and our heart sank as Python
responded

```pycon
>>> tf.sin()
AttributeError: module 'tensorflow' has no attribute 'sin'
```

Shit! No worries, though, we can use the
[`@tf.custom_gradient`](https://www.tensorflow.org/api_docs/python/tf/custom_gradient) decorator,
the ever-reliable NumPy, and the fact that

$$\frac{d}{dx}\sin(x) = \cos(x)$$

to define an autodiff-supporting sine function for TensorFlow:

```python
import numpy as np
import tensorflow as tf

@tf.custom_gradient
def sin(x):
    def grad(dy):
        # nested function that returns the
        # vector-Jacobian product
        return dy * np.cos(x.numpy())
    return np.sin(x.numpy()), grad
```

This is a great drop in replacement for our missing sine functionality:


```pycon
>>> weights = tf.Variable([0.4, 0.1, 0.2])
>>> with tf.GradientTape() as tape:
...     res = sin(weights)
>>> print(res)
tf.Tensor([0.38941833 0.09983342 0.19866933], shape=(3,), dtype=float32)
>>> grad = tape.gradient(res, weights)
tf.Tensor([0.921061  0.9950042 0.9800666], shape=(3,), dtype=float32)
```

What happens if we would like the second derivative, however?

```pycon
>>> with tf.GradientTape() as tape1:
...     with tf.GradientTape() as tape2:
...         res = sin(weights)
...     grad = tape2.gradient(res, weights)
... grad2 = tape1.gradient(grad, weights)
>>> print(grad2)
None
```


😬

Because the custom gradient we are returning uses a NumPy function `np.cos`, TensorFlow does not
know how to differentiate the returned custom gradient.

## Nesting custom gradients

No worries! We can fix this by simply registering the gradient of the custom gradient! (Note: the
TensorFlow `@tf.custom_decorator` documentation has an example of defining a second derivative this
way, but as far as I can tell, [it appears
incorrect](https://stackoverflow.com/a/60518214/10958457)).


```python
@tf.custom_gradient
def sin(x):
    def first_order(dy):

        @tf.custom_gradient
        def jacobian(a):
            def hessian(ddy):
                return ddy * -np.sin(a.numpy())
            return np.cos(a.numpy()), hessian

        return dy * jacobian(x)
    return np.sin(x.numpy()), first_order
```

Here, we are using the fact that $\frac{d^2}{dx^2}\sin(x) = -\sin(x)$, and defining
a new `jacobian()` function that *itself* has its custom gradient (the Hessian) defined.
This now works as required:

```pycon
>>> with tf.GradientTape() as tape1:
...     with tf.GradientTape() as tape2:
...         res = sin(weights)
...     grad = tape1.gradient(res, weights)
... grad2 = tape2.gradient(grad, weights)
>>> print(grad2)
tf.Tensor([-0.38941833 -0.09983342 -0.19866933], shape=(3,), dtype=float32)
```

However, say we wanted the third derivative? This would now return `None`, since we have only
defined up until the second derivative! To support the third derivative would
require three levels of custom-gradient nesting; similarly, for $n$ derivatives,
we need $n$ levels of nesting.

## The parameter-shift rule

Using the [trig identity](https://en.wikipedia.org/wiki/List_of_trigonometric_identities) $\sin(a+b)
- \sin(a-b) = 2\cos(a)\sin(b)$, we can write the derivative of the sine function in a form that is
more suited to higher derivatives:

$$\frac{d}{dx}\sin(x) = \cos(x) = \frac{\sin(x+s) - \sin(x-s)}{2\sin(s)}, ~~~ s\in \mathbb{R}.$$

In particular, the derivative of $\sin(x)$ is now written in terms of a **linear combination of
calls to the _same_ function, just with shifted parameters!**[ref]The parameter-shift rule is an
important result for quantum machine learning and variational algorithms, as it allows analytic
quantum gradients to be computed *on quantum hardware*. For more details, see [Evaluating analytic
gradients on quantum hardware](https://arxiv.org/abs/1811.11184), the [PennyLane
glossary](https://pennylane.ai/qml/glossary/parameter_shift.html), or this [tutorial I wrote on
quantum gradients](https://pennylane.ai/qml/demos/tutorial_backprop.html)[/ref] This leads to a
really neat idea: if we define a sine function with custom gradient *in terms of itself*, will it
allow for arbitrary $n$-th derivatives in TensorFlow?

Let's give it a shot.

```python
@tf.custom_gradient
def sin(x, shift=np.pi/2):
    c = 1.0 / (2 * np.sin(shift))

    def grad(dy):
        jacobian = c * (sin(x + shift, shift=shift) - sin(x - shift, shift=shift))
        return dy * jacobian

    return np.sin(x.numpy()), grad
```

Note that we only have one level of nesting (so we are only registering the first derivative),
but we are defining the first derivative by recursively calling the original function.

Does this work? Attempting to compute the third derivative:

```pycon
>>> with tf.GradientTape() as tape1:
...     with tf.GradientTape() as tape2:
...         with tf.GradientTape() as tape3:
...             res = sin(weights)
...         grad = tape3.gradient(res, weights)
...     grad2 = tape2.gradient(grad, weights)
... grad3 = tape1.gradient(grad, weights)
>>> print(grad3)
tf.Tensor([-0.38941827 -0.0998335  -0.19866937], shape=(3,), dtype=float32)
```

Amazing! And it agrees exactly with the known third derivative:

```pycon
>>> print(-tf.sin(weights))
tf.Tensor([-0.38941833 -0.09983342 -0.19866933], shape=(3,), dtype=float32)
```

We can construct a more complicated model, where we are even calling our custom sine
function with different shift values, and compute the full Hessian matrix:

```python
with tf.GradientTape(persistent=True) as tape1:
    with tf.GradientTape(persistent=True) as tape2:
        y = tf.stack([weights[1] * weights[2], weights[2], weights[0]])
        res = sin(weights, shift=np.pi/4) + 3 * sin(y, shift=np.pi/2) ** 2
        print("Result:", res)

    grad = tape2.gradient(res, weights)
    print("Gradient:", grad)

grad2 = tape1.jacobian(grad, weights, experimental_use_pfor=False)
print("Hessian:\n", grad2)
```

<p style="font-italic">Out:</p>
<pre class="ml-5" style="margin-top:-80px; color: grey;">
Result: tf.Tensor([0.39061818 0.21824193 0.6536093 ], shape=(3,), dtype=float32)
Gradient: tf.Tensor([3.0731294 1.0189977 2.1603184], shape=(3,), dtype=float32)
Hessian:
 tf.Tensor(
[[3.7908227  0.         0.        ]
 [0.         0.13997458 0.23987202]
 [0.         0.23987202 5.3876476 ]], shape=(3, 3), dtype=float32)
</pre>

## Final note

While this is a neat trick for defining custom gradients that support arbitrary
derivatives (as long as the derivative can be written as a linear combination
of the original function!), it is often not the most efficient method. To see why,
consider the derivative of a function $f(x)$ satisfying a parameter-shift rule:

$$
\begin{align}
\frac{d^2}{dx^2}f(x) &=  c \frac{d}{dx}f(x+s) - c \frac{d}{dx}f(x-s)\\[7pt]
                        &= \left[c^2 (f(x+2s)-f(x)) \right] - \left[c^2 (f(x)-f(x-2 s)\right].
\end{align}
$$

TensorFlow will be naively performing *four* evaluations of the original function in order
to compute the second derivative; whereas if done symbolically, we can see that some
terms would cancel out or combine without even needing to perform all evaluations:


$$\frac{d^2}{dx^2}f(x) = c^2 \left[ f(x+2s) - 2f(x) + f(x-2s) \right].$$

And that's not all; given the periodicity of the function $f(x)$, there are often even *further*
optimizations that can be made for a specific shift value $s$; for example
being able to cache and re-use previous function evaluations computed during the
first derivative.

So while the recursive custom gradient is a neat trick, it's probably always better to manually nest
the custom gradients. Especially if evaluating $f(x)$ is a bottleneck! [ref]Higher-order quantum
gradients using the paramter-shift rule was explored in [Estimating the gradient and higher-order
derivatives on quantum hardware](https://arxiv.org/abs/2008.06517). Check it out if you are curious
to see some of the optimizations that can be made when computing the Hessian.[/ref]

---
