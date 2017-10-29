# Introduction

Thank you for considering contributing to vol.community! It's people like you that can help make this project more awesome
than we could imagine.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project.
In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

We are an open source project and we love to receive contributions from our community — you! There are many ways to contribute, examples are:

## Add new countries
Add support for new countries by raising an issue to support your country, and include sites that you would like to be included.

Writing spiders to parse these sites and upload them to [vol.community](vol.community).

## Improving documentation
Guides like the one you are reading a the moment are an important way for people to get on board. Once you start collaborating
and are all set it's easy to forget the challenges involved in getting up to speed with new knowledge domains and code bases. 

## Report Bugs
If you find a security vulnerability, do NOT open an issue. Email security@vol.community instead.

Report bugs at https://github.com/volCommunity/vol-crawlers/issues

* If you can, provide detailed steps to reproduce the bug.
* If you don't have steps to reproduce the bug, just note your observations in as much detail as you can.
Questions to start a discussion about the issue are welcome.

## Solve Bugs
Any issue with labels "help wanted" and "bug" are fair game. Before you start work on one, please state your intention in the issue
to prevent others from duplicating your work!

# Ground Rules
* Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
* Keep feature versions as small as possible, preferably one new feature per version.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See our [Code Of Conduct](href=https://github.com/volCommunity/vol-crawlers/blob/master/CODE_OF_CONDUCT.md>CODE_OF_CONDUCT.md)

# Your First Contribution
Not sure where to start contributing?

You can start looking at issues with label [help-wanted](https://github.com/volCommunity/vol-crawlers/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aopen%20label%3A%22help%20wanted%22%20).
As the project matures we'll have labels for beginner issues at [beginner-issue](https://github.com/volCommunity/vol-crawlers/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aopen%20label%3A%22beginner%20friendly%22) 
 which should only require a few lines of code, and a test or two.
Issues that would be a good first issue will be availble at [good-first-issue](https://github.com/volCommunity/vol-crawlers/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

# Your First Pull Request
Working on your first Pull Request? You can learn how from this *free* series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

# Suggesting a Feature
If you find yourself wishing for a feature that doesn't exist, you are probably not alone. There are bound to be others out there with similar needs.
Open an issue on our issues list on GitHub which describes the feature you would like to see, why you need it, and how it should work.

# Code comReview Process
After your Pull Request has been reached anyone is able to suggest changes. Only suggestions by core contributors have to be
followed but do give any contructive feedback some thought.

Your Pull Request should have gotten feedback withing a week. If we suggest making changes we may close the pull requests if there is no activity withing 2 weeks.

# Community
You can chat with the core team IRC on [irc.freenode.net/#vol.community](https://kiwiirc.com/client/irc.freenode.net/#vol.community). We try to have office hours on Fridays.

# Development Workflow
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
