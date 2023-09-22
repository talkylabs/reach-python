import os

from talkylabs.reach.rest import ReachClient

API_USER = os.environ.get("REACH_TALKYLABS_API_USER")
API_KEY = os.environ.get("REACH_TALKYLABS_API_KEY")


def example():
    """
    Some example usage of different Reach resources.
    """
    client = ReachClient(API_USER, API_KEY)

    # Get all messages
    all_messages = client.messaging.messaging_items.list()
    print("There are {} messages in your account.".format(len(all_messages)))

    # Get only last 10 messages...
    some_messages = client.messaging.messaging_items.list(limit=10)
    print("Here are the last 10 messages in your account:")
    for m in some_messages:
        print(m)

    # Get messages in smaller pages...
    all_messages = client.messaging.messaging_items.list(page_size=10)
    print("There are {} messages in your account.".format(len(all_messages)))

    print("Sending a message...")
    new_message = client.messaging.messaging_items.send(dest="XXXX", src="YYYY", body="Reach is the best!")


if __name__ == "__main__":
    example()
