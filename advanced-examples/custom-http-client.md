# Custom HTTP Clients for the Reach Python Helper Library

If you are working with the Reach Python Helper Library, and you need to be able to modify the HTTP requests that the library makes to the Reach servers, you’re in the right place. The most common reason for altering the HTTP request is to connect and authenticate with an enterprise’s proxy server. We’ll provide sample code that you can use in your app to handle this and other use cases.

## Connect and authenticate with a proxy server

To connect to a proxy server that's between your app and Reach, you need a way to modify the HTTP requests that the Reach helper library makes on your behalf to the Reach REST API.

In Python, the Reach helper library uses the [requests](https://docs.python-requests.org/en/master/) library under the hood to make the HTTP requests, and this allows you to provide your own `http_client` for making API requests.

So the question becomes: how do we apply this to a typical Reach REST API request, such as?

```python
client = ReachClient(api_user, api_key)

message = client.messaging.messaging_items \
    .send(
        dest="+15558675310",
        body="Hey there!",
        src="+15017122661"
    )

```

To start, you should understand when and where a `http_client` is created and used.

The helper library creates a default `http_client` for you whenever you call the `Client` constructor with your Reach credentials. Here, you have the option of creating your own `http_client`, and passing to the constructor, instead of using the default implementation.

Here’s an example of sending an SMS message with a custom client:

```python
import os
from talkylabs.reach.rest import ReachClient
from custom_client import MyRequestClass

from dotenv import load_dotenv
load_dotenv()

# Custom HTTP Class
my_request_client = MyRequestClass()

client = ReachClient(os.getenv("REACH_TALKYLABS_API_USER"), os.getenv("REACH_TALKYLABS_API_KEY"),
                http_client=my_request_client)

message = client.messaging.messaging_items \
    .send(
        dest="+15558675310",
        body="Hey there!",
        src="+15017122661"
    )

print('Message: {}'.format(message))
```

## Create your custom ReachRestClient

When you take a closer look at the constructor for `HttpClient`, you see that the `http_client` parameter is actually of type `talkylabs.reach.http.HttpClient`.

`HttpClient` is an abstraction that allows plugging in any implementation of an HTTP client you want (or even creating a mocking layer for unit testing).

However, within the helper library, there is an implementation of `talkylabs.reach.http.HttpClient` called `ReachHttpClient`. This class wraps the `talkylabs.reach.http.HttpClient` and provides it to the Reach helper library to make the necessary HTTP requests.

## Call Reach through a proxy server

Now that we understand how all the components fit together, we can create our own `HttpClient` that can connect through a proxy server. To make this reusable, here’s a class that you can use to create this `HttpClient` whenever you need one.

```python
import os
from requests import Request, Session, hooks
from talkylabs.reach.http.http_client import ReachHttpClient
from talkylabs.reach.http.response import Response

class MyRequestClass(ReachHttpClient):
    def __init__(self):
        self.response = None

    def request(self, method, url, params=None, data=None, headers=None, auth=None, timeout=None,
                allow_redirects=False):
        # Here you can change the URL, headers and other request parameters
        kwargs = {
            'method': method.upper(),
            'url': url,
            'params': params,
            'data': data,
            'headers': headers,
            'auth': auth,
        }

        session = Session()
        request = Request(**kwargs)

        prepped_request = session.prepare_request(request)
        session.proxies.update({
            'http': os.getenv('HTTP_PROXY'),
            'https': os.getenv('HTTPS_PROXY')
        })
        response = session.send(
            prepped_request,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )

        return Response(int(response.status_code), response.text)
```

In this example, we are using some environment variables loaded at the program startup to retrieve various configuration settings:

Your Reach API user and key

A proxy address in the form of http://127.0.0.1:8888

These settings are located in an .env file, like so:

```env
REACH_TALKYLABS_API_USER=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
REACH_TALKYLABS_API_KEY= your_auth_token

HTTPS_PROXY=https://127.0.0.1:8888
HTTP_PROXY=http://127.0.0.1:8888
```

Here’s the full program that sends a text message and shows how it all can work together.

```python
import os
from talkylabs.reach.rest import ReachClient
from custom_client import MyRequestClass

from dotenv import load_dotenv
load_dotenv()

# Custom HTTP Class
my_request_client = MyRequestClass()

client = ReachClient(os.getenv("REACH_TALKYLABS_API_USER"), os.getenv("REACH_TALKYLABS_API_KEY"),
                http_client=my_request_client)

message = client.messaging.messaging_items \
    .send(
        dest="+15558675310",
        body="Hey there!",
        src="+15017122661"
    )

print('Message: {}'.format(message))
```

## What else can this technique be used for?

Now that you know how to inject your own `http_client` into the Reach API request pipeline, you could use this technique to add custom HTTP headers and authorization to the requests (perhaps as required by an upstream proxy server).

You could also implement your own `http_client` to mock the Reach API responses so your unit and integration tests can run quickly without needing to make a connection to Reach.

We can’t wait to see what you build!
