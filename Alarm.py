from botocore.exceptions import ClientError


class Alarm:
    def __init__(self, sns):
        self.sns = sns

    # 알림을 전송할 주제 나열
    def list(self):
        try:
            topics = self.sns.list_topics()
            cnt = 0
            for topic in topics['Topics']:
                print(topic)
                cnt+=1

            print(f"You have {cnt} alarms.")

        except ClientError as err:
            print("Cannot get alarm list")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])