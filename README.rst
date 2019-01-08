Schireson Logger
================

#schiresonip #teamruby

Index
-----

-  `Why use logging`_
-  `How to configure local logging`_
-  `How to set up remote logging`_

### Why use logging \* Log to multiple destinations, such as to the
terminal (``stderr``, ``stdout``, etc.) or a file. \* Filter messages by
severity \* Send messages of different severities to different
destinations \* Provide extra context and metadata to logs

### How to configure local logging For logging in one script, set up
logging and get the logger, then start using it:

.. code:: python

   from schireson_logger import log, setup_logging

   setup_logging('INFO', log_file='script.log')
   log.info('Wow!')

To capture tracebacks and exception information, add the
``log_exceptions`` decorator to the function and pass it the logger:

.. code:: python

   from schireson_logger import log, log_exceptions

   @log_exceptions(log)
   def function():
       ...

This decorator will log any exception from this function, even within
nested function calls.

To configure logging for an entire service, entrypoints
(e.g. ``manage.py``) should first set up logging:

.. code:: python

   from schireson_logger import setup_logging

   setup_logging('INFO', log_file='service.log')

Then modules that want to log things can import the logger and start
logging:

.. code:: python

   from schireson_logger import log

   log.info('Wow!')

### How to set up remote logging For projects deployed on a remote EC2
instance (either in a Docker container or directly), logs can also be
sent to a logging service. To get logs from a Docker container, specify
the log driver and options:

.. code:: bash

   $ docker run \
       --log-driver=awslogs \
       --log-opt awslogs-region=REGION \
       --log-opt awslogs-group=SOME_GROUP \
       ...

If the project is deployed directly, a service such as CloudWatch can be
used to collect logs and metrics. Ask SRE if you don’t have AWS
permissions or need any help. The Amazon docs are here: `Quick Start:
CloudWatch Logs Agent`_

.. _Why use logging: #why-use-logging
.. _How to configure local logging: #local-logging
.. _How to set up remote logging: #remote-logging
.. _`Quick Start: CloudWatch Logs Agent`: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/QuickStartEC2Instance.html
