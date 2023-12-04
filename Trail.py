from botocore.exceptions import ClientError


class Trail:
    def __init__(self, client):
        self.client = client

    def event_log_by_count(self):
        try:
            count = input("Enter the number of events : ")
            if len(count) == 0:
                print("You entered an incorrect number.")
                return

            count = int(count)
            if count <= 0:
                print("Please enter a value greater than 0.")
                return

            response = self.client.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'Username',
                        'AttributeValue': 'rak'
                    }
                ],
                MaxResults=count
            )
            for event in response['Events']:
                print(f"[name] {event['EventName']}, ", end="")
                print(f"[source] {event['EventSource'].split('.')[0]}, ", end="")
                print(f"[time] {event['EventTime']}")

        except ClientError as err:
            print("Cannot display event record")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])
