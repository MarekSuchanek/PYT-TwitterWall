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
`auth.example.cfg` serves as example of this configuration file. 

:warning: :closed_lock_with_key: Never ever publish file with your Twitter 
API key & secret! 


## Usage

Will be introduced soon! :turtle:

## Author

*  Marek Suchánek [[suchama4@fit.cvut.cz](mailto:suchama4@fit.cvut.cz)]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) 
file for more details.

