from botocore.exceptions import ClientError
from threading import Event
import time


class Alarm:
    def __init__(self, client):
        self.client = client

    # 알람을 전송할 주제 나열
    def list(self):
        try:
            topics = self.client.list_topics()
            arn_list, email_list = [], []
            cnt = 0
            for i, topic in enumerate(topics['Topics']):
                tmp_email = []
                print(f"{i+1}. [name] {topic['TopicArn'].split(':')[-1]}", end=" ")

                endpoints=self.client.list_subscriptions_by_topic(TopicArn=topic['TopicArn'])
                print(f"[email] ", end="")
                for endpoint in endpoints['Subscriptions']:
                    if endpoint['SubscriptionArn'] != 'PendingConfirmation':
                        print(f"{endpoint['Endpoint']} ", end="")
                        tmp_email.append([endpoint['SubscriptionArn'], endpoint['Endpoint']])
                print()

                email_list.append(tmp_email)
                arn_list.append(topic['TopicArn'])
                cnt+=1

            print(f"You have {cnt} alarms.")
            return arn_list, email_list

        except ClientError as err:
            print("Cannot get alarm list")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 알람 생성
    def create_alarm(self):
        # 어떤 작업에 대해 알람을 생성할 지 결정
        topic = ''

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
            name = 'create_instance'
        elif operation=='4':
            name = 'terminate_instance'
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
            email = input("Enter your email: ")

            response = self.client.create_topic(Name=name)
            topic = response['TopicArn']
            self.client.subscribe(
                TopicArn=topic,
                Protocol='email',
                Endpoint=email,
            )
            print("A confirmation email has been sent. Please complete verification in time.")

            flag = self.verify_email(topic)

            if flag:
                print("Successfully create alarm")
            else:
                self.client.delete_topic(TopicArn=topic)
                print("\nAlarm creation failed because the email was not confirmed.")

        except ClientError as err:
            print("Cannot create alarm")
            self.client.delete_topic(TopicArn=topic)
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 특정 작업 시 알람 전송
    def send(self, action):
        try:
            topics = self.client.list_topics()
            for topic in topics['Topics']:
                if topic['TopicArn'].split(':')[-1] == action:
                    self.client.publish(
                        TopicArn=topic['TopicArn'],
                        Message=f"당신의 AWS 계정으로 {action} 작업이 이루어졌습니다. 본인의 활동이 맞는지 확인해보세요."
                    )
                    break

        except ClientError as err:
            print("Cannot send the email")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 알람 삭제
    def delete(self):
        topics, endpoints = self.list()
        num = len(topics)

        if num==0:
            print("There are no alarms to modify.")
            return

        try:
            operation = int(input("\nWhich alarm do you want to delete? "))

            try:
                if operation > num or operation <= 0:
                    print("You entered an invalid integer...")
                    return

                # 토픽 삭제
                self.client.delete_topic(TopicArn=topics[operation - 1])
                # 해당 토픽을 구독하는 이메일 삭제
                for endpoint in endpoints[operation - 1]:
                    self.client.unsubscribe(SubscriptionArn=endpoint[0])

                print("Successfully delete alarm")

            except ClientError as err:
                print("Cannot delete alarm")
                print(err.response["Error"]["Code"], end=" ")
                print(err.response["Error"]["Message"])

        except ValueError:
            print("You entered an invalid integer...")

    # 알람 이메일 수정
    def modify(self):
        topics, endpoints = self.list()
        num = len(topics)

        if num==0:
            print("There are no alarms to modify.")
            return

        try:
            operation = int(input("\nWhich alarm do you want to modify? "))

            try:
                if operation > num or operation <= 0:
                    print("You entered an invalid integer...")
                    return

                # 어떤 작업에 대해 이메일을 수정할 지
                print("                                                 ")
                print("         What task do you want to do?            ")
                print("                                                 ")
                print("    1. delete email           2. add email       ")
                print("                                                 ")

                task = input("Enter an integer: ")
                # 이메일 삭제하는 경우
                if task=='1':
                    flag=True
                    email = input("Which email would you like to delete? ")
                    for endpoint in endpoints[operation - 1]:
                        if endpoint[1] == email:
                            flag = False
                            self.client.unsubscribe(SubscriptionArn=endpoint[0])
                            print(f"Successfully delete email {email}")

                    if flag:
                        print("You entered wrong email...")

                # 이메일 추가하는 경우
                elif task=='2':
                    email = input("Enter your email: ")
                    flag = True
                    for endpoint in endpoints[operation - 1]:
                        if endpoint[1] == email:
                            flag = False
                            print("This email already exists.")
                            break

                    if flag:
                        print("A confirmation email has been sent. Please complete verification in time.")
                        self.client.subscribe(
                            TopicArn=topics[operation - 1],
                            Protocol='email',
                            Endpoint=email,
                        )

                        validation = self.verify_email(topics[operation - 1])
                        if validation:
                            print(f"Successfully add email {email} to alarm {topics[operation-1].split(':')[-1]}")
                        else:
                            print("\nYour email has not been confirmed.")

                # 잘못된 번호를 입력한 경우
                else:
                    print("You entered an invalid integer...")
                    return

            except ClientError as err:
                print("Cannot modify alarm")
                print(err.response["Error"]["Code"], end=" ")
                print(err.response["Error"]["Message"])

        except ValueError:
            print("You entered an invalid integer...")

    # 이메일 검증
    def verify_email(self, topicArn):
        cnt, flag, result = 20, True, False
        for i in range(cnt, -1, -1):
            print(f"{i}...", end="", flush=True)

            endpoints = self.client.list_subscriptions_by_topic(TopicArn=topicArn)
            for endpoint in endpoints['Subscriptions']:
                if endpoint['SubscriptionArn'] == 'PendingConfirmation':
                    flag = False
                    break

            if flag:
                print(" Confirmed.")
                result = True
                break
            else:
                flag = True

            time.sleep(1)

        return result
