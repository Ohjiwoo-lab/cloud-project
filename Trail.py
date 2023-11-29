from botocore.exceptions import ClientError


class Trail:
    def __init__(self, client):
        self.client = client

    def select_mode(self):
        # 어떤 방식으로 확인할 지 결정
        print("                                                            ")
        print("             Select criteria to filter events.              ")
        print("                                                            ")
        print("  1. number of events                  2. event period      ")
        print("                                                            ")

        num = int(input("Enter an integer: "))
        if num == 1:
            self.event_log_by_count()

    def event_log_by_count(self):
        try:
            count = int(input("Enter the number of events you want to check: "))
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
                print(f"[source] {event['EventSource']}, ", end="")
                print(f"[time] {event['EventTime']}")

        except ClientError as err:
            print("Cannot display event record")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])
