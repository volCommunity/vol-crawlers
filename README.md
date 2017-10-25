[![Build status](https://travis-ci.org/volCommunity/vol-crawlers.svg?branch=master)](https://travis-ci.org/volCommunity/vol-crawlers)
[![Coverage Status](https://coveralls.io/repos/github/volCommunity/vol-crawlers/badge.svg?branch=master)](https://coveralls.io/github/volCommunity/vol-crawlers?branch=master)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![IRC Channel](https://img.shields.io/badge/chat-on%20freenode-brightgreen.svg)](https://kiwiirc.com/client/irc.freenode.net/#vol.community)

# Vol::crawlers
Welcome! This project is in very early and experimental stage, and help in the following areas would be greatly appreciated!
 
This repository contains the crawlers used to find volunteering gigs.
 
How you could help:
* **Non technical:** Add support for new countries by raising an issue to support your country, and include sites that you would like to be included
* **Technical:** Help writing new or extending current crawlers 

## Development
Crawlers are written in Python3, use the Scrapy framework and run from Scrapinghub. They consume the REST API of https://github.com/volCommunity/vol-django
to update jobs.

Make your life easier by installing the flake8 pre-commit hook, if flake8 fails, so will the Travis build.

```shell
flake8 --install-hook git            # Install the hook
git config --bool flake8.strict true # Prevent commit creation
```

### Installation
We use the amazing <a href=https://github.com/kennethreitz/pipenv>Pipenv</a> to manage <a href=http://docs.python-guide.org/en/latest/dev/virtualenvs/>virtualenvs:</a>

Install Pipenv to manage virtualenvs, if you do not have it installed:
```
pip install pipenv
```

When Pipenv is available we spawn a shell and install the projects dependencies in our Virtualenv:
```shell
pipenv shell && pipenv install
```

### Running
#### Locally
You need to start vol-django locally -see https://github.com/volCommunity/vol-django or run against a deployed instance.

Once that is set up, run the scrawler of your choice, you'll need to specify the REST token (get or create at http://localhost:8000/adminauthtoken/token ) and REST URL, which you could
do like so. In this case we spin up the "dogoodjobs.co.nz" crawler:

```shell
scrapy crawl dogoodjobs.co.nz -a rest_token=a7d86fb582d3f61e377d43e4a76996d66e5fecba -a rest_url=http://localhost:8000
```

#### Scrapinghub
Spiders will be deployed to scrapinghub by Travis, after a merge to master.

The project lives at https://app.scrapinghub.com/p/247498 raise an issue if you would like access.

Spiders can be controlled via the CLI, after you have gotten access you'l be able to use Shub to control them. See
the doco for more information on this: https://app.scrapinghub.com/p/247498
