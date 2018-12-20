# Schireson Logger
\#schiresonip #teamruby

## Index
* [Why use logging](#why-use-logging)
* [How to configure local logging](#local-logging)
* [How to set up remote logging](#remote-logging)

<a name='why-use-logging'></a>
### Why use logging
* Log to multiple destinations, such as to the terminal (`stderr`, `stdout`, etc.) or a file.
* Filter messages by severity
* Send messages of different severities to different destinations
* Provide extra context and metadata to logs

<a name='local-logging'></a>
### How to configure local logging
For logging in one script, set up logging and get the logger, then start using it:
```python
import logging
from schireson_logger.logger import setup_logging

setup_logging('INFO', log_file='script.log', logger_name='script_logger')
log = logging.getLogger('service_logger')
log.info('Wow!')
```

To capture tracebacks and exception information, add the `log_exceptions` decorator to the function and pass it the logger:
```python
import logging
from schireson_logger.decorator import log_exceptions

log = logging.getLogger('service_logger')
@log_exceptions(log)
def function():
    ...
```
This decorator will log any exception from this function, even within nested function calls.

To configure logging for an entire service, entrypoints (e.g. `manage.py`) should first set up logging:
```python
from schireson_logger.logger import setup_logging

setup_logging('INFO', log_file='service.log', logger_name='service_logger')
```

Then modules that want to log things can get the logger based on the given name and start logging:
```python
import logging

log = logging.getLogger('service_logger')
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
