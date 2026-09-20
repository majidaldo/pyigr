# Why?

My (author) motivation is to be able to generally describe systems that respond to change.


Related (but not the same):
- reactive programming libraries:
Doesn't focus on a 'state'
- dynamical systems [pathsim](https://docs.pathsim.org/):
This library doesn't, at the face of it, look like it can do what pathsim does, 
but I think sim descriptions could be mapped somehow.

DAG exec:
- pipefunc
state with no deps. useful as is but you can farm out tasks as you wish.


# How?

Rules/functions are repeatedly applied to a 'state' (dict)
until there are no more changes.
w
## 1. Specify

Rules initializer:
```python
def __init__(self, state: state = {}, *, log: bool = False): ...
```
Function registration:
```python
def register(self, argmap: argmap = {}): ...
```

```python
import state_rules.main as rm

r = rm.Rules({'x':1}, log=True)
@r.register({
    # input
    'x': 'x' # created by default from func sig if not specified
    # output
    'return': 'x', # default is funcname.
    # for multiple outputs,
    # can be a dict that updates state: return: { }
     })
def f(x):
    return x+x # {'x': x+x, 'x+x':x+x } # will be inserted to state
```

## 2. Run

The run function signature:
```python
def run(self, maxiter=10, *, stopping: Callable[[state], bool] | None = None): ...
```

```python
r.run(5)
r.log
```
```python
[
Iteration(i=0, state={'x': 1})
Iteration(i=1, state={'x': 2})
Iteration(i=2, state={'x': 4})
Iteration(i=3, state={'x': 8})
Iteration(i=4, state={'x': 16})
Iteration(i=5, state={'x': 32})
]
```

# Tips

- The state is a (flat) dictionary but you can use a fancy dotted dict if you want more structure.
Then, use use a function to get at a key.
- Cache function calls (yourself) as functions will get repeatedly called with the same input.
- Use `stopping` critereon to early stop before `maxiter`.
