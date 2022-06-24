# High Performance Computing with Python

Experiments with Python for HPC and collection of Python benchmarks.

## Line Profiler

[`line_profiler`](https://github.com/pyutils/line_profiler) is a module for doing line-by-line profiling of functions.

### Usage

```python
@profile
def foo():
    pass
```

```bash
kernprof -l SCRIPT
```
