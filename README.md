# Twitter Wall

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) 
![Version](https://img.shields.io/badge/release-v0.2-orange.svg)


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
../PYT-TwitterWall/ $ python3 twitterwall ...
```

#### Virtual environment:

```
../PYT-TwitterWall/ $ python3 -m venv env
../PYT-TwitterWall/ $ . env/bin/activate
(env) ../PYT-TwitterWall/ $ python3 -m pip -r requirements.txt
(env) ../PYT-TwitterWall/ $ python3 twitterwall ...

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

First you need config file with your API key & secret. Default path is `config/auth.cfg`, 
can be set different via `--config` option:

```
python twitterwall --config <file> [web|cli] ...
```

### CLI

TwitterWall CLI can be used simply. Options will allow you to:

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

#### Examples

Show help how to use **TwitterWall**:

```
python twitterwall cli --help
```

Show only czech tweets (no retweets) with hashtag **#python**:

```
python twitterwall cli -q "#python" --no-retweets --lang "cs"
```

Show only czech tweets (no retweets) with text **swag**, 
check every 1 second, load 20 tweets at start and don't use any 
CLI output styling at all:

```
python twitterwall cli -q "swag" -i 1 -n 20 --no-swag
```

Filter loaded tweets with word **python** by allowing only authors **hroncok** 
and **EnCuKou** ([MI-PYT](https://github.com/cvut/MI-PYT) teachers):

* _NOTE_: It will probably show only new tweets by these authors and no tweets 
will be shown at the start, because are not in last 5 tweets containing word "python".

```
python twitterwall cli -q "python" -a "hroncok" -a "EnCuKou"
python twitterwall cli -q "python" -a "hroncok" -a "encukou"
```

Filter loaded tweets with word **python** by blocking authors **hroncok** 
and **EnCuKou** ([MI-PYT](https://github.com/cvut/MI-PYT) teachers), so it
will hide all tweets by them:

```
python twitterwall cli -q "python" -b "hroncok" -b "EnCuKou"
python twitterwall cli -q "python" -b "hroncok" -b "encukou"
```

Filter loaded tweets with word **python** by allowing only tweets with 
number of retweets between 10 and 100 and from authors that have at least
300 followers but also less than 3000:

```
python twitterwall cli -q "python" --retweets-min 10 --retweets-max 100 \
                       --followers-min 300 --followers-max 3000
```

#### Output sample

```
05/10/2016 15:02:35 (https://twitter.com/pythontrending/statuses/783683809762050048)
Python Trending [pythontrending]: MI-PYT - Materiály k předmětu MI-PYT na FIT ČVUT https://t.co/ZYdDaPT58n
```

  * _NOTE_: Time is always in UTC timezone (as given from Twitter API, just reformatted)!
  
### WEB

WEB interface is made by [Flask](http://flask.pocoo.org) & [Jinja](http://jinja.pocoo.org). 
It uses also [Twitter Bootstrap](http://getbootstrap.com), [jQuery](https://jquery.com)
and [Lightbox](http://lokeshdhakar.com/projects/lightbox2/) (local files only, no CDN).

Main ideas are same as for CLI interface. You just start web app with defined 
(or default) count of initial tweets displayed and/or interval of loading next
tweets via AJAX. You can also run in flask debugging mode. The query and language
is set by user of web interface (by URL). 

In the web interface user can moreover turn on/off AJAX loading, clear screen or 
just refresh the page. For each tweet there is button for hide/show details that
consists of entities: hashtags, mentions, links and photos. For nicer photos browsing
is used Lightbox.

_Example_: [mareksuchanek.pythonanywhere.com](http://mareksuchanek.pythonanywhere.com/)

#### Routes

  * `/` = landing
  * `/q/<query>[/<lang>]` = web interface for requested query in defined language
  * `/api/<lid>/<query[/<lang>]` = API used by AJAX for loading additional tweets

#### Web launch example

Here is also `--help` as for the `cli` command: 

```
python twitterwall web --help
```

Start web interface with loading 7 tweets at start and 10 seconds interval of AJAX requests (when turned on by user). 

  * _NOTE_: Minimal value of interval is defined as 3 seconds.
  
```
python twitterwall web --count 7 --interval 10
python twitterwall web -n 7 -i 10
```

Start web interface with default values (5 tweets and 5 seconds), but turn on debugging.

  * _NOTE_: Should not be used on production! :confounded:

```
python twitterwall web --debug
```

#### Screenshots

Basic Twitter Wall with **@hroncok** query:

![Basic tweets list with "@hroncok" query](http://marsu.9e.cz/github/twitterwall-basic.png)

Tweets with **#photoshoot** query with one tweet details shown (2 hashtags, 1 mention, 0 links and 1 picture):

![Tweets list with "#photoshoot" query with one tweet details shown ](http://marsu.9e.cz/github/twitterwall-details.png)

Enlarged photo of cat :smiley_cat: via [Lightbox](http://lokeshdhakar.com/projects/lightbox2/):

![Enlarged photo of cat via Lightbox](http://marsu.9e.cz/github/twitterwall-lightbox.png)

## Authors

*  Marek Suchánek [[suchama4@fit.cvut.cz](mailto:suchama4@fit.cvut.cz)]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) 
file for more details.

