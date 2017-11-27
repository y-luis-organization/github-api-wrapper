[![Build Status](https://travis-ci.org/y-luis-organization/github-api-wrapper.svg?branch=master)](https://travis-ci.org/y-luis-organization/github-api-wrapper)

# GitHub API wrapper

Prerequisites:
-------------
Django

requests

Endpoints
-------------
    GET organizations/

Number of organizations that are at this time in github (according to https://stackoverflow.com/a/47503662/3286487).

    GET organizations/organization_name

Number of repositories and the biggest repository for a given organization name

Both endpoints returns a JSON response.

Tested with:
-------------
Django 1.11

requests 2.10