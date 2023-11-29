from botocore.exceptions import ClientError
import time


class Condor:
    def __init__(self, client, ec2):
        self.client = client
        self.ec2_client = ec2

    # HTCondor의 상태를 보는 함수
    def status(self):
        try:
            # 마스터 노드를 필터링
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'tag:Name',
                        'Values': ['master']
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