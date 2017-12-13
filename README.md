# ops-buildkite-reporter

This is a Stat reporting tool that talks to BuildKite API V2/GraphQL and generates
reports in csv format for management to have a picture of the BK usage within
MYOB


## Get Started

- set `export BK_TOKEN=<the BuildKite API token>`

   > token: your personal BK API token with all read related permissions

- set `export BK_DRYRUN=False`

   > feel free to set `BK_DRYRUN=True` if you want to save time or computationally
expensive API hits, or decide it is not necessary to fetch up-to-date data from
the API.

- simply run `./team_pipeline_build_stat.py` to get CSV reports in local
directory

## TODO

- More unit tests
- CI pipeline
- AWS integrations:
  * get the BK_TOKEN from AWS-SSM
  * Be able to run this program in AWS-Lambda
  * AWS-CloudWatch can trigger the above AWS-Lambda weekly
  * output the CSV report to a AWS-S3 version-enabled bucket
  * setup SES (Simple Email Service) to send the CSV report to the Management
  once CSV report is ready
- CD pipeline to deploy the above mentioned stack

## For Developers

- To make it more compatible with AWS-Lambda, in term of dependency management.
Please run
  - `cd <the project's root folder>`
  - `pip install <your new dependency> -t <./vendor>`

  > If you want to add dependencies to the project AND you use `OSX` as
operating system. Please consider add a cfg file temporarily, as suggested
[here](https://stackoverflow.com/questions/24257803/distutilsoptionerror-must-supply-either-home-or-prefix-exec-prefix-not-both).
Otherwise you will have an strange error due to a known issue with PIP.
`distutils.errors.DistutilsOptionError: must supply either home or prefix/exec-prefix -- not both`

  - After installing new dependencies, don't forget to remove the workaround file
  `rm $HOME/.pydistutils.cfg`
  - Remove unnecessary `whl` files to make your package slim
  `rm ./vendor/*.whl`
