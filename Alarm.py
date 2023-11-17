from botocore.exceptions import ClientError


class Alarm:
    def __init__(self, client, resource):
        self.client = client
        self.resource = resource

    # 알람을 전송할 주제 나열
    def list(self):
        try:
            topics = self.client.list_topics()
            cnt = 0
            for topic in topics['Topics']:
                print(topic['TopicArn'].split(':')[-1])
                cnt+=1

            print(f"You have {cnt} alarms.")

        except ClientError as err:
            print("Cannot get alarm list")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 알람 생성
    def create_alarm(self):
        # 어떤 작업에 대해 알람을 생성할 지 결정
        print("                                                            ")
        print("            When do you want to send the alarm?             ")
        print("                                                            ")
        print("  1. start instance               2. stop instance          ")
        print("  3. create instance              4. terminate instance     ")
        print("                                                            ")

        name = ''
        operation = input("Enter an integer: ")
        if operation=='1':
            name = 'start_instance'
        elif operation=='2':
            name = 'stop_instance'
        elif operation=='3':
            name = 'create instance'
        elif operation=='4':
            name = 'terminate instance'
        else:
            print("You entered an invalid integer.")
            return

        try:
            # 이미 존재하는 알람인지 확인
            topics = self.client.list_topics()
            for topic in topics['Topics']:
                if topic['TopicArn'].split(':')[-1]==name:
                    print("Already exist alarm")
                    return

            # 알람 생성 및 구독 활성화 (구독은 이메일로)
            try:
                email = input("Enter your email: ")
                response = self.client.create_topic(Name=name)
                self.client.subscribe(
                    TopicArn=response['TopicArn'],
                    Protocol='email',
                    Endpoint=email,
                )

            except ClientError as err:
                print("Cannot create alarm")
                print(err.response["Error"]["Code"], end=" ")
                print(err.response["Error"]["Message"])

        except ClientError as err:
            print("Cannot get alarm list")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])