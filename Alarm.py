from botocore.exceptions import ClientError
import time
import boto3
import json


class Alarm:
    def __init__(self):
        self.client = boto3.client('sns')
        self.event = boto3.client('events')

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
            name = 'StartInstances'
        elif operation=='2':
            name = 'StopInstances'
        elif operation=='3':
            name = 'RunInstances'
        elif operation=='4':
            name = 'TerminateInstances'
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
                event_pattern = '{\n' \
                + '  "source": ["aws.ec2"],\n' \
                + '  "detail-type": ["AWS API Call via CloudTrail"],\n' \
                + '  "detail": {\n' \
                + '    "eventSource": ["ec2.amazonaws.com"],\n' \
                + '    "eventName": ["' + name + '"]\n' \
                + '  }\n' \
                + '}'

                # EventBridge 규칙 생성
                self.event.put_rule(
                    Name = name,
                    EventPattern=event_pattern,
                    State='ENABLED'
                )

                # EventBridge가 SNS에 메시지를 게시할 권한 부여 (리소스 기반 정책)
                attribute = self.client.get_topic_attributes(  # 기존 권한 가져오기
                    TopicArn=topic
                )

                json_policy = json.loads(attribute['Attributes']['Policy'])   # 문자열을 json으로 변환
                
                # 추가할 권한 정의
                policy = {
                    "Sid": "AWSEvents_" + name + "_id",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "events.amazonaws.com"
                    },
                    "Action": "sns:Publish",
                    "Resource": topic
                }
                json_policy['Statement'].append(policy)   # 권한 추가

                # 새로운 권한 생성 (json을 문자열로 바꾸기 위해 json.dumps 사용)
                new_policy = '{"Version":"' + json_policy['Version'] + '",' + '"Id":"' + json_policy['Id'] + '",' + '"Statement":' + json.dumps(json_policy['Statement']) + '}'

                # 속성 업데이트
                response = self.client.set_topic_attributes(
                    TopicArn = topic,
                    AttributeName = 'Policy',
                    AttributeValue = new_policy
                )

                # 대상(sns) 연결
                self.event.put_targets(
                    Rule=name,
                    Targets=[
                        {
                            "Id": name + "_SNS",
                            "Arn": topic,
                            "Input": json.dumps("귀하의 계정으로 " + name + " 작업이 이루어졌습니다. 본인이 수행한 활동이 아니라면 계정의 보안을 체크해보세요.", ensure_ascii = False)
                        }]
                )

                print("Successfully create alarm")
            else:
                self.client.delete_topic(TopicArn=topic)
                print("\nAlarm creation failed because the email was not confirmed.")

        except ClientError as err:
            print("Cannot create alarm")
            self.client.delete_topic(TopicArn=topic)
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 알람 삭제
    def delete(self):
        topics, endpoints = self.list()
        num = len(topics)

        if num==0:
            print("There are no alarms to delete.")
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
