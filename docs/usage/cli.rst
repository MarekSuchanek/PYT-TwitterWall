CLI
===


**PYT TwitterWall CLI** can be used simply. Options will allow you to:

-  set the search query
-  set the count of initial tweets to show up (default is 5)
-  *NOTE*: This number means requested number of tweets before internal
   filtering (i.e. authors, #followers, #retweets, is retweet itself, …)
-  set the interval between twitter calls for new tweets (default is 10
   seconds)
-  set language of tweets to show up
-  allow/block tweets from users by giving user nicknames
-  set tweets to show only if they have min/max number of retweets
-  set tweets to show only if their author has min/max number for
   followers
-  hide retweets from output
-  disable colors and other styling in output (also no
   hashtag/mention/hyperref highlighting)

Moreover you can use:

-  ``--help`` to see all the options, syntax and information
-  ``--version`` to check the version of app

Command examples
----------------

Show help how to use **twitterwall**:

::

    twitterwall cli --help

Show only czech tweets (no retweets) with hashtag **#python**:

::

    twitterwall cli -q "#python" --no-retweets --lang "cs"

Show only czech tweets (no retweets) with text **swag**, check every 1
second, load 20 tweets at start and don’t use any CLI output styling at all:

::

    twitterwall cli -q "swag" -i 1 -n 20 --no-swag

Filter loaded tweets with word **python** by allowing only authors **hroncok**
and **EnCuKou** (`MI-PYT`_ teachers):

-  *NOTE*: It will probably show only new tweets by these authors and no
   tweets will be shown at the start, because are not in last 5 tweets containing
   word “python”.

::

    twitterwall cli -q "python" -a "hroncok" -a "EnCuKou"
    twitterwall cli -q "python" -a "hroncok" -a "encukou"

Filter loaded tweets with word **python** by blocking authors **hroncok**
and **EnCuKou** (`MI-PYT`_ teachers), so it will hide all tweets by them:

::

    twitterwall cli -q "python" -b "hroncok" -b "EnCuKou"
    twitterwall cli -q "python" -b "hroncok" -b "encukou"

Filter loaded tweets with word **python** by allowing only tweets with
number of retweets between 10 and 100 and from authors that have at
least 300 followers but also less than 3000:

::

    twitterwall cli -q "python" --retweets-min 10 --retweets-max 100 \
                    --followers-min 300 --followers-max 3000

Output sample
-------------

::

    05/10/2016 15:02:35 (https://twitter.com/pythontrending/statuses/783683809762050048)
    Python Trending [pythontrending]: MI-PYT - Materiály k předmětu MI-PYT na FIT ČVUT https://t.co/ZYdDaPT58n

-  *NOTE*: Time is always in UTC timezone (as given from Twitter API,
   just reformatted)!

.. _MI-PYT: https://github.com/cvut/MI-PYT