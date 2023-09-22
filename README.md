# reach-python

## Documentation

The documentation for the Reach@Talkylabs API can be found [here][apidocs].

The Python library documentation can be found [here][libdocs].

## Versions

`reach-python` uses a modified version of [Semantic Versioning](https://semver.org) for all changes. [See this document](VERSIONS.md) for details.

### Supported Python Versions

This library supports the following Python implementations:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

## Installation

Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a
package manager for Python.

```shell
pip3 install reach-talkylabs
```

If pip install fails on Windows, check the path length of the directory. If it is greater 260 characters then enable [Long Paths](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation) or choose other shorter location.

Don't have pip installed? Try installing it, by running this from the command
line:

```shell
curl https://bootstrap.pypa.io/get-pip.py | python
```

Or, you can [download the source code
(ZIP)](https://github.com/talkylabs/reach-python/zipball/main 'reach-python
source code') for `reach-python`, and then run:

```shell
python3 setup.py install
```

> **Info**
> If the command line gives you an error message that says Permission Denied, try running the above commands with `sudo` (e.g., `sudo pip3 install reach-talkylabs`).

### Test your installation

Try sending yourself an SMS message. Save the following code sample to your computer with a text editor. Be sure to update the `src` phone number with one that you verified in the web application. The `dest` phone number will be your own mobile phone.

```python
from talkylabs.reach.rest import ReachClient

api_user = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
api_key  = "your_api_key"

client = ReachClient(api_user, api_key)

message = client.messaging.messaging_items.send(
    dest="+15558675309",
    src="+15017250604",
    body="Hello from Python!")

print(message)
```

Save the file as `send_sms.py`. In the terminal, `cd` to the directory containing the file you just saved then run:

```shell
python3 send_sms.py
```

After a brief delay, you will receive the text message on your phone.

> **Warning**
> It's okay to hardcode your credentials when testing locally, but you should use environment variables to keep them secret before committing any code or deploying to production.

## Use the helper library

### API Credentials

The client needs your Reach credentials. You can either pass these directly to the constructor (see the code below) or via environment variables.

Authenticating with Account SID and Auth Token:

```python
from talkylabs.reach.rest import ReachClient

api_user = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
api_key  = "your_api_key"
client = ReachClient(api_user, api_key)
```

Alternatively, a `Client` constructor without these parameters will
look for `REACH_TALKYLABS_API_USER` and `REACH_TALKYLABS_API_KEY` variables inside the
current environment.

We suggest storing your credentials as environment variables. Why? You'll never
have to worry about committing your credentials and accidentally posting them
somewhere public.

```python
from talkylabs.reach.rest import ReachClient
client = ReachClient()
```



### Iterate through records

The library automatically handles paging for you. Collections, such as `calls` and `messages`, have `list` and `stream` methods that page under the hood. With both `list` and `stream`, you can specify the number of records you want to receive (`limit`) and the maximum size you want each page fetch to be (`page_size`). The library will then handle the task for you.

`list` eagerly fetches all records and returns them as a list, whereas `stream` returns an iterator and lazily retrieves pages of records as you iterate over the collection. You can also page manually using the `page` method.

#### Use the `list` method

```python
from talkylabs.reach.rest import ReachClient

api_user = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
api_key = "your_api_key"
client = ReachClient(api_user, api_key)

for sms in client.messaging.messaging_items.list():
  print(sms.dest)
```

### Asynchronous API Requests

By default, the Client will make synchronous requests to the API. To allow for asynchronous, non-blocking requests, we've included an optional asynchronous HTTP client. When used with the Client and the accompanying `*_async` methods, requests made to the API will be performed asynchronously.

```python
from talkylabs.reach.http.async_http_client import AsyncReachHttpClient
from talkylabs.reach.rest import ReachClient

async def main():
    api_user = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    api_key  = "your_api_key"
    http_client = AsyncReachHttpReachClient()
    client = ReachClient(api_user, api_key, http_client=http_client)

    message = await client.messaging.messaging_items.send_async(dest="+12316851234", src="+15555555555", body="Hello there!")

asyncio.run(main())
```

### Enable Debug Logging

Log the API request and response data to the console:

```python
import logging

client = ReachClient(api_user, api_key)
logging.basicConfig()
client.http_client.logger.setLevel(logging.INFO)
```

Log the API request and response data to a file:

```python
import logging

client = ReachClient(api_user, api_key)
logging.basicConfig(filename='./log.txt')
client.http_client.logger.setLevel(logging.INFO)
```

### Handling Exceptions

`reach-python` exports an exception class to help you handle exceptions that are specific to Reach methods. To use it, import `ReachRestException` and catch exceptions as follows:

```python
from talkylabs.reach.rest import ReachClient
from talkylabs.reach.base.exceptions import ReachRestException

api_user = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
api_key  = "your_api_key"
client = ReachClient(api_user, api_key)

try:
  message = client.messaging.messaging_items.send(dest="+12316851234", src="+15555555555", body="Hello there!")
except ReachRestException as e:
  print(e)
```


### Other advanced examples

- [Learn how to create your own custom HTTP client](./advanced-examples/custom-http-client.md)

### Docker Image

The `Dockerfile` present in this repository and its respective `talkylabs/reach-python` Docker image are currently used by us for testing purposes only.

### Getting help

If you've found a bug in the library or would like new features added, go ahead and open issues or pull requests against this repo!

[apidocs]: https://www.reach.talkylabs.com/docs/api
[libdocs]: https://talkylabs.github.io/reach-python
