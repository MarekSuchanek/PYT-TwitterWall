# Twitter Wall

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


Twitter Wall is simple [Python](https://www.python.org) powered app for 
displaying [Twitter](https://twitter.com) tweets in CLI. It has the ability 
to show number of queried tweets (i.e. selected by search string) at start 
and then check if new tweets are publish and display them as well. This 
project is created as task for subject MI-PYT, CTU in Prague 
([subject repository :octocat:](https://github.com/cvut/MI-PYT)). 

## Installation

You need **Python 3.4+** to run this app and then there are two options
(examples are for Linux systems, for Windows or OSX find appropriate 
equivalents):

### Python environment

:bulb: Check your `python3 --version` first, maybe you will need to use
`python3.5` instead or update finally!

#### System-wide environment:

```
../PYT-TwitterWall/ $ python3 -m pip -r requirements.txt
../PYT-TwitterWall/ $ python3 twitterwall.py
```

#### Virtual environment:

```
../PYT-TwitterWall/ $ python3 -m venv env
../PYT-TwitterWall/ $ . env/bin/activate
(env) ../PYT-TwitterWall/ $ python3 -m pip -r requirements.txt
(env) ../PYT-TwitterWall/ $ python3 twitterwall.py

(env) ../PYT-TwitterWall/ $ deactivate
../PYT-TwitterWall/ $ rm -r env
```

### Twitter API key

You need to set-up your Twitter app on [apps.twitter.com](https://apps.twitter.com/) 
and create configuration file containing API key & secret. Provided 
`config/auth.example.cfg` serves as example of this configuration file. 

:warning: :closed_lock_with_key: Never ever publish file with your Twitter 
API key & secret! 


## Usage

TwitterWall CLI can be used simply. First you need config file with your
API key & secret (default path is `config/auth.cfg`, can be set different
via `--config` option. Other options will allow you to:

* set the search query
* set the count of initial tweets to show up (default is 5)
  * _NOTE_: This number means requested number of tweets before internal filtering (i.e.
authors, #followers, #retweets, is retweet itself, ...)
* set the interval between twitter calls for new tweets (default is 10 seconds)
* set language of tweets to show up
* allow/block tweets from users by giving user nicknames
* set tweets to show only if they have min/max number of retweets
* set tweets to show only if their author has min/max number for followers
* hide retweets from output
* disable colors and other styling in output (also no hashtag/mention/hyperref highlighting)

Moreover you can use:

* `--help` to see all the options, syntax and information
* `--version` to check the version of app

### Examples

Show help how to use **TwitterWall**:

```
python twitterwall.py --help
```

Show only czech tweets (no retweets) with hashtag **#python**:

```
python twitterwall.py -q "#python" --no-retweets --lang "cs"
```

Show only czech tweets (no retweets) with text **swag**, 
check every 1 second, load 20 tweets at start and don't use any 
CLI output styling at all:

```
python twitterwall.py -q "swag" -i 1 -n 20 --no-swag
```

Filter loaded tweets with word **python** by allowing only authors **hroncok** 
and **EnCuKou** ([MI-PYT](https://github.com/cvut/MI-PYT) teachers):

* _NOTE_: It will probably show only new tweets by these authors and no tweets 
will be shown at the start, because are not in last 5 tweets containing word "python".

```
python twitterwall.py -q "python" -a "hroncok" -a "EnCuKou"
python twitterwall.py -q "python" -a "hroncok" -a "encukou"
```

Filter loaded tweets with word **python** by blocking authors **hroncok** 
and **EnCuKou** ([MI-PYT](https://github.com/cvut/MI-PYT) teachers), so it
will hide all tweets by them:

```
python twitterwall.py -q "python" -b "hroncok" -b "EnCuKou"
python twitterwall.py -q "python" -b "hroncok" -b "encukou"
```

Filter loaded tweets with word **python** by allowing only tweets with 
number of retweets between 10 and 100 and from authors that have at least
300 followers but also less than 3000:

```
python twitterwall.py -q "python" --retweets-min 10 --retweets-max 100 \
                      --followers-min 300 --followers-max 3000
```

### Output sample

```
05/10/2016 15:02:35 (https://twitter.com/pythontrending/statuses/783683809762050048)
Python Trending [pythontrending]: MI-PYT - Materiály k předmětu MI-PYT na FIT ČVUT https://t.co/ZYdDaPT58n
```

  * _NOTE_: Time is always in UTC timezone (as given from Twitter API, just reformatted)!

## Authors

*  Marek Suchánek [[suchama4@fit.cvut.cz](mailto:suchama4@fit.cvut.cz)]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) 
file for more details.

