Usage basics
============

First you need config file with your API key & secret. Default path is ``config/auth.cfg``,
can be set different via ``--config`` (or ``-c``) option:

::

   twitterwall --config <file> [web|cli] ...

For more about the config file, read section :doc:`../install/api_keys`.


Commands
--------
By selecting ``web`` or ``cli`` command you will pick desired interface
for tweets output:

- :doc:`cli`
- :doc:`web`


Common options
--------------

You can also use ``--help`` and ``--version`` at any level:

::

  $ twitterwall --help
  Usage: twitterwall [OPTIONS] COMMAND [ARGS]...

    Twitter Wall for loading and printing desired tweets

  Options:
    -c, --config FILENAME  App config file path.
    --version              Show the version and exit.
    --help                 Show this message and exit.

  Commands:
    cli  Twitter Wall running in CLI
    web  Twitter Wall running as web server

  $ twitterwall --version
  PYT TwitterWall, version 0.5
