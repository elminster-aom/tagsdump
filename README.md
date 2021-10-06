# Playground - transfer some GitHub metadata to Elastic cloud

## Basic description
This program takes a GitHub organization name (or user) and indexes the repository names along with all the repository's
respective tags.

#### Scenario
* These components may run in different systems
* One or more database tables could handle a reasonable amount of checks performed over a longer period of time

## How it works
The main program `tagsdump.py` has two execution modes:
1. Initial and first execution. Using parameter `--init` defines index (e.g.: *github-metadata*) on Elasticsearch and mapping for the data, e.g.:
```shell
$ tagsdump.py --init github-metadata
```
2. Next executions. Using the organization name (e.g.: *elminster-aom*) as source and the index (e.g.: *github-metadata*) as target, tags information will be stored in Elastic, e.g.:
```shell
$ tagsdump.py elminster-aom github_tags
```

## How to install
1. Clone or download a ZIP of this project, e.g.:
```shell
$ git clone git@github.com:elminster-aom/tagsdump.git
```
2. Ensure that you have the right version of Python (v3.9, see below)
3. Create and activate Python Virtual Environment and install required packages, e.g.:
```shell
$ python3 -m venv tagsdump \
&& source tagsdump/bin/activate \
&& python3 -m pip install --requirement tagsdump/requirements.txt
```
4. Move into the new environment:
```shell
$ cd tagsdump
```

## How to set up and run
1. Create (if doesn't exist already) a GitHub and Elastic account
2. All available settings are based on an environment variables file in the home of our application. For its creation you can use this template:
```shell
$ nano .env

# copy-paste this content:
ELASTIC_CLOUD_ID = my_elastic_cloud_id
ELASTIC_CLOUD_USER = "elastic"
ELASTIC_CLOUD_PSW = my_elastic_password
GITHUB_TOKEN = my_oath_token
LOG_LEVEL = WARNING

$ chmod 0600 .env
```

## Additional considerations
1. Only Unix-like systems are supported
2. The code has been tested with Python 3.9.4
3. For a detailed list of Python modules check out the [requirements.txt]
4. Concepts like tunning or replication are out of the scope of this exercise

## Areas of improvement
* Implement Elastic indexing using `elasticsearch.helpers.async_streaming_bulk()` for a better performance
* In addition of *tags*, include *release* metadata for adding `@timestamp` information to Elastic docs
* Review the possibility of using [Conditional requests](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#conditional-requests) for skipping tags already indexed
* Index is automatically created actually, maybe it would be worth to control this for taking profit of the index-mapping
