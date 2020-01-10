# WorkSpace Rebuilder
Since Amazon doesn't allow to rebuild all WorkSpaces using "One Click", here is a little tool doing it for you. It retrieve all WorkSpaces IDs and rebuild them using new image. You can also import user list from csv, get their Workspaces IDs and rebuild them. Script will ask you if you want to do that.
# Requirments
[Python 2.x or 3.x](https://www.python.org/downloads/)

[boto3](https://boto3.readthedocs.io/en/latest/)

[argparse](https://docs.python.org/3/library/argparse.html)

# Installation
```sh
$ pip install boto3
$ pip install argparse
```
# Usage
WorkSpace Rebuilder uses IAM role by default (if started from EC2 instance). If you want to start it from on-premise host then you should pass credentials. Also region should be given.
Using IAM role:
```sh
$ python ws-rebuilder.py region
```
Using credentials:
```sh
$ python ws-rebuilder.py region --accesskey="yourAccessKey" --secretkey="yourSecretKey"
```
Usage example:
```sh
$ python ws-rebuilder.py eu-west-1
$ python ws-rebuilder.py eu-west-1 --accesskey="ABCDEF" --secretkey="123456"
```
You can also inject credentials using export command and then simply execute script. If you do so then you can skip *accesskey* and *secretkey* arguments. Just remember to specify a region!
```sh
$ export AWS_ACCESS_KEY_ID="YOUR_AWS_KEY_ID"
$ export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
$ export AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN"

$ python ws-rebuilder.py region
```
# IAM Policy
Policy with minimum required permissions can be found in `ws-rebuilder-policy.json` file.

# Changelog
- v0.1.1 - 07.01.2020 - Added possibility to rebuild Workspaces using user list from CSV file.
- v0.1.0 - 12.12.2019 - Public Release.