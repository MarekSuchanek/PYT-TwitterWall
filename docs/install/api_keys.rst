Twitter API keys
================

You need to set-up your Twitter app on `apps.twitter.com`_ and create
configuration file containing API key & secret. For that you need Twitter
user account with filled phone number in the first place. Provided ``config/auth.example.cfg``
serves as example of this configuration file.

  **!!!** Never ever publish file with your Twitter API key & secret!

  We also recommend NOT to use personal Twitter account.

.. _apps.twitter.com: https://apps.twitter.com/

auth.cfg layout
---------------
::

    [twitter]
    key = YourTwitterAPIKeyComesHere
    secret = YourTwitterAPISecretComesHere

