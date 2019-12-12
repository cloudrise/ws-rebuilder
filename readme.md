# WorkSpace Rebuilder
Since Amazon doesn't allow to rebuild all WorkSpaces using "One Click", here is a little tool doing it for you. It retrieve all WorkSpaces IDs and rebuild them using new image.
# Requirments
[Python 2.x or 3.x](https://www.python.org/downloads/)

[boto3](https://boto3.readthedocs.io/en/latest/)

# Installation
```sh
$ pip install boto3
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
# IAM Policy
Policy with minimum required permissions can be found in `ws-rebuilder-policy.json` file.

