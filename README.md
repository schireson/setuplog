![CircleCI](https://img.shields.io/circleci/build/gh/schireson/setuplog/master) [![codecov](https://codecov.io/gh/schireson/setuplog/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/setuplog) [![Documentation Status](https://readthedocs.org/projects/setuplog/badge/?version=latest)](https://setuplog.readthedocs.io/en/latest/?badge=latest)

## The pitch

Logging setup is one of those annoying things that one finds themselves relearning
every time a new project is started.

`setuplog` attempts to centralize, and simplify the set of decisions one needs to make
when bootstrapping a project.

```python
# app.py
from setuplog import setup_logging

setup_logging(
    log_level='INFO',
    namespace='project_name',

    # opt into {}-style formatting!
    style='format',
)

# elsewhere
from setuplog import log

log.info('Info!')
```

## Installing

```bash
pip install "setuplog"
```
