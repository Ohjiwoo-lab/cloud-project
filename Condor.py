from botocore.exceptions import ClientError
import time
import boto3


class Condor:
    def __init__(self):
        self.client = boto3.client('ssm')
        self.ec2_client = boto3.client('ec2')

    # 마스터 노드 아이디 리턴
    def get_master(self):
        try:
            # 마스터 노드를 필터링
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': ['master']
                    },
                    {
                        'Name': 'instance-state-name',
                        'Values': ['running']
                    }
                ]
            )

            master_id = ''
            for instances in response['Reservations']:
                for instance in instances['Instances']:
                    if instance['State']['Name'] != 'running':
                        print("The master node must be running.")
                        return
                    master_id = instance['InstanceId']

            return master_id

        except ClientError as err:
            print("Unable to get master instance information.")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # HTCondor의 상태를 보는 함수
    def status(self):
        try:
            master_id = self.get_master()

            # 마스터 노드에 명령 실행
            command = self.client.send_command(
                Targets=[
                    {
                        'Key': 'InstanceIds',
                        'Values': [
                            master_id
                        ]
                    }
                ],
                DocumentName="AWS-RunShellScript",
                Comment="condor status",
                Parameters={
                    'commands': [
                        'condor_status'
                    ]
                }
            )

            # 명령이 실행될 동안 sleep
            print("Running...")
            time.sleep(1)

            # 결과 출력
            result = self.client.get_command_invocation(
                CommandId=command['Command']['CommandId'],
                InstanceId=master_id
            )
            print(result['StandardOutputContent'])

        except ClientError as err:
            print("The command cannot be sent to the master node.")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 콘솔처럼 실행할 수 있게 하는 기능
    def console(self):
        try:
            # 접속하고 싶은 인스턴스 id를 입력
            instance_id = input("Enter the instance ID you want to connect to: ")

            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': [instance_id]
                    }
                ]
            )

            # 잘못된 아이디를 입력한 경우
            if len(response['Reservations']) == 0:
                print("You entered an incorrect ID.")
                return

            for instances in response['Reservations']:
                for instance in instances['Instances']:
                    if instance['State']['Name'] != 'running':
                        print("The instance is not running.")
                        return

            print("Connect to the console.")
            while True:
                operation = input("$ ")
                if operation == "exit":
                    break

                command = self.client.send_command(
                    Targets=[
                        {
                            'Key': 'InstanceIds',
                            'Values': [
                                instance_id
                            ]
                        }
                    ],
                    DocumentName="AWS-RunShellScript",
                    Parameters={
                        'commands': [
                            operation
                        ]
                    }
                )

                time.sleep(1)

                # 결과 출력
                result = self.client.get_command_invocation(
                    CommandId=command['Command']['CommandId'],
                    InstanceId=instance_id
                )

                if result['Status'] == 'Success':
                    print(result['StandardOutputContent'])
                else:
                    print(result['StandardErrorContent'])

        except ClientError as err:
            print("The command cannot be sent to the node.")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])
