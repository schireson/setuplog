# Schireson Logger

<a name='why-use-logging'></a>
### Why use logging
* Log to multiple destinations, such as to the terminal (`stderr`, `stdout`, etc.) or a file.
* Filter messages by severity
* Send messages of different severities to different destinations
* Provide extra context and metadata to logs

<a name='local-logging'></a>
### How to configure local logging
For logging in one script, configure logging, then start logging directly using `log`:
```python
from schireson_logger import log, setup_logging

setup_logging('INFO', log_file='script.log')
log.info('Wow!')
```

To capture tracebacks and exception information, add the `log_exceptions` decorator to the function and pass it the logger:
```python
from schireson_logger import log, log_exceptions

@log_exceptions(log)
def function():
    ...
```
This decorator will log any exception from this function, even within nested function calls.

To configure logging for an entire service, entrypoints (e.g. `manage.py`) should first set up logging and add the `log_exceptions` decorator to the entrypoint function:
```python
from schireson_logger import setup_logging

setup_logging('INFO')
```


Then modules that want to log things can import the logger and start logging:
```python
from schireson_logger import log

log.info('Wow!')
```

<a name='remote-logging'></a>
### How to set up remote logging
 For projects deployed on a remote EC2 instance (either in a Docker container or directly), logs can also be sent to a logging service.
To get logs from a Docker container, specify the log driver and options:
```bash
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=REGION \
    --log-opt awslogs-group=SOME_GROUP \
    ...
```

If the project is deployed directly, a service such as CloudWatch can be used to collect logs and metrics. 
Ask SRE if you don't have AWS permissions or need any help.
The Amazon docs are here: [Quick Start: CloudWatch Logs Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/QuickStartEC2Instance.html)
