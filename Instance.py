from botocore.exceptions import ClientError
import boto3


class Instance:
    def __init__(self):
        self.ec2_resource = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')
        self.sns = boto3.client('sns')

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
                    master_id = instance['InstanceId']

            return master_id

        except ClientError as err:
            print("Unable to get master instance information.")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 인스턴스 정보 출력
    def display(self):
        try:
            response = self.ec2_client.describe_instances()
            if len(response['Reservations']) == 0:
                print('No instance')
            else:
                for instances in response['Reservations']:
                    for instance in instances['Instances']:
                        if instance['State']['Name']=='terminated':
                            continue
                        print(f"[name] {instance['Tags'][0]['Value']}, ", end="")
                        print(f"[id] {instance['InstanceId']}, ", end="")
                        print(f"[AMI] {instance['ImageId']}, ", end="")
                        print(f"[type] {instance['InstanceType']}, ", end="")
                        print(f"[state] {instance['State']['Name']}, ", end="")
                        print(f"[monitoring state] {instance['Monitoring']['State']}")

        except Exception as err:
            print("Cannot display instances any more")
            print(f"Exception: {err}")

    # 특정 인스턴스 시작
    def start(self, ids):
        print(f"Starting ....", end="")
        for id in ids:
            print(f" {id}", end="")
        print()

        try:
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': ids
                    }
                ]
            )

            # 응답이 없는 경우, 잘못된 인스턴스 아이디를 입력한 것
            if len(response['Reservations']) == 0:
                print("Please enter correct id")
            else:
                for instances in response['Reservations']:
                    for instance in instances['Instances']:
                        # 이미 인스턴스가 시작 중인 상태인 경우
                        if instance['State']['Name'] == 'running':
                            print(f"Instance {instance['InstanceId']} is already running.")
                        else:
                            self.ec2_resource.instances.filter(InstanceIds=[instance['InstanceId']]).start()
                            print(f"Successfully started instance {instance['InstanceId']}")

        # 예외 처리
        except ClientError as err:
            print(f"Cannot start instances", end="")
            for id in ids:
                print(f" {id}", end=" ")
            print()
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 특정 인스턴스 중지
    def stop(self, ids):
        try:
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': ids
                    }
                ]
            )

            # 응답이 없는 경우, 잘못된 인스턴스 아이디를 입력한 것
            if len(response['Reservations']) == 0:
                print("Please enter correct id")
            else:
                for instances in response['Reservations']:
                    for instance in instances['Instances']:
                        # 마스터 노드인 경우 중지 불가
                        if instance['InstanceId'] == self.get_master():
                            print("The master node cannot be stopped.")
                            return
                        # 이미 인스턴스가 중지 중인 상태인 경우
                        if instance['State']['Name'] == 'stopped':
                            print(f"Instance {instance['InstanceId']} is already stopped.")
                            return
                        else:
                            self.ec2_resource.instances.filter(InstanceIds=[instance['InstanceId']]).stop()
                            print(f"Successfully stop instance {instance['InstanceId']}")

        # 예외 처리
        except ClientError as err:
            print(f"Cannot stop instances", end="")
            for id in ids:
                print(f" {id}", end=" ")
            print()
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 인스턴스 생성
    def create(self, ami_id):
        securityGroup = []
        for vm in self.ec2_resource.security_groups.all():
            if vm.group_name == "allow_ssh":
                securityGroup.append(vm.id)
                break

        params = {
            "ImageId": ami_id,
            "InstanceType": "t2.micro",
            "KeyName": "ansible_keypair",
            "SecurityGroupIds": securityGroup,
            "TagSpecifications": [
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            'Key': 'Name',
                            'Value': 'slave'
                        },
                    ]
                }
            ]
        }

        try:
            instance = self.ec2_resource.create_instances(**params, MinCount=1, MaxCount=1)[0]
            print(f"Successfully started EC2 instance {instance.id} based on AMI {ami_id}")

        # 예외 처리
        except ClientError as err:
            print(f"Cannot create instance based on AMI {ami_id}")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # AMI 이미지 출력
    def ami_images(self):
        print("Listing images....")
        try:
            flag=True
            for image in self.ec2_resource.images.filter(Filters=[{'Name': 'name', 'Values': ['slave-image']}]):
                print(f"[ImageId] {image.id}, [Name] {image.name}, [Owner] {image.owner_id}")
                flag=False

            if flag:
                print('No images')

        except Exception as err:
            print("Cannot display ami images any more")
            print(f"Exception: {err}")

    # 가용 영역 출력하기
    def get_availability_zone(self):
        try:
            response = self.ec2_client.describe_availability_zones()
            cnt=0
            for zone in response['AvailabilityZones']:
                print(f"[id] {zone['ZoneId']}, ", end="")
                print(f"[region] {zone['RegionName']}, ", end="")
                print(f"[zone] {zone['ZoneName']}")
                cnt += 1

            print(f"You have access to {cnt} Availability Zones.")

        except ClientError as err:
            print(f"Cannot get available zones")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 리전 출력하기
    def get_region(self):
        try:
            response = self.ec2_client.describe_regions()
            cnt = 0
            for region in response['Regions']:
                print(f"[region] {region['RegionName']}, ", end="")
                print(f"[endpoint] {region['Endpoint']}")
                cnt +=1

            print(f"You have access to {cnt} Regions.")

        except ClientError as err:
            print(f"Cannot get available regions")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 인스턴스 재부팅하기
    def reboot(self, ids):
        print("Rebooting ....", end="")
        for id in ids:
            print(f" {id}", end=" ")
        print()

        try:
            self.ec2_client.reboot_instances(InstanceIds=ids)
            print(f"Successfully rebooted instance", end="")
            for id in ids:
                print(f" {id}", end=" ")
            print()

        except ClientError as err:
            print(f"Cannot reboot instance")
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])

    # 인스턴스 종료(삭제)하기
    def terminate(self, ids):
        print("Terminating ...", end="")
        for id in ids:
            print(f" {id}", end=" ")
        print()

        try:
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': ids
                    }
                ]
            )

            # 응답이 없는 경우, 잘못된 인스턴스 아이디를 입력한 것
            if len(response['Reservations']) == 0:
                print("Please enter correct id")
            else:
                for instances in response['Reservations']:
                    for instance in instances['Instances']:
                        # 마스터 노드인 경우 종료 불가
                        if instance['InstanceId'] == self.get_master():
                            print("The master node cannot be terminated.")
                            return
                        # 이미 인스턴스가 종료 중인 상태인 경우
                        elif instance['State']['Name'] == 'terminated':
                            print(f"Instance {instance['InstanceId']} is already terminated.")
                            return
                        else:
                            self.ec2_resource.instances.filter(InstanceIds=[instance['InstanceId']]).terminate()
                            print(f"Successfully terminate instance {instance['InstanceId']}")

        # 예외 처리
        except ClientError as err:
            print(f"Cannot terminate instances", end="")
            for id in ids:
                print(f" {id}", end=" ")
            print()
            print(err.response["Error"]["Code"], end=" ")
            print(err.response["Error"]["Message"])