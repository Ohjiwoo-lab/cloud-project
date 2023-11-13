import boto3
from botocore.exceptions import ClientError


class Instance:
    def __init__(self, ec2, client):
        self.ec2 = ec2
        self.client = client
        self.response = self.client.describe_instances()

    # 인스턴스 정보 출력
    def display(self):
        try:
            if len(self.response['Reservations']) == 0:
                print('No instance')
            else:
                for instances in self.response['Reservations']:
                    for instance in instances['Instances']:
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
            self.ec2.instances.filter(InstanceIds=ids).start()
            print(f"Successfully started instance", end="")
            for id in ids:
                print(f" {id}", end="")
            print()

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
            self.ec2.instances.filter(InstanceIds=ids).stop()
            print(f"Successfully stop instance", end="")
            for id in ids:
                print(f" {id}", end="")
            print()

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
        for vm in self.ec2.security_groups.all():
            if vm.group_name == "launch-wizard-3":
                securityGroup.append(vm.id)
                break

        params = {
            "ImageId": ami_id,
            "InstanceType": "t2.micro",
            "KeyName": "slave-key",
            "SecurityGroupIds": securityGroup
        }

        try:
            instance = self.ec2.create_instances(**params, MinCount=1, MaxCount=1)[0]
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
            for image in self.ec2.images.filter(Filters=[{'Name': 'name', 'Values': ['aws-htcondor-slave']}]):
                print(f"[ImageId] {image.id}, [Name] {image.name}, [Owner] {image.owner_id}")
                flag=False

            if flag:
                print('No images')

        except Exception as err:
            print("Cannot display ami images any more")
            print(f"Exception: {err}")

class Client:
    def __init__(self, client):
        self.client = client

    # 가용 영역 출력하기
    def get_availability_zone(self):
        response = self.client.describe_availability_zones()
        cnt=0
        for zone in response['AvailabilityZones']:
            print(f"[id] {zone['ZoneId']}, ", end="")
            print(f"[region] {zone['RegionName']}, ", end="")
            print(f"[zone] {zone['ZoneName']}")
            cnt += 1

        print(f"You have access to {cnt} Availability Zones.")

    # 리전 출력하기
    def get_region(self):
        response = self.client.describe_regions()
        for region in response['Regions']:
            print(f"[region] {region['RegionName']}, ", end="")
            print(f"[endpoint] {region['Endpoint']}")

    # 인스턴스 재부팅하기
    def reboot(self, id):
        print(f"Rebooting .... {id}")
        self.client.reboot_instances(InstanceIds=[id])
        print(f"Successfully rebooted instance {id}")


if __name__ == '__main__':
    while True:
        print("                                                            ")
        print("                                                            ")
        print("------------------------------------------------------------")
        print("           Amazon AWS Control Panel using SDK               ")
        print("------------------------------------------------------------")
        print("  1. list instance                2. available zones        ")
        print("  3. start instance               4. available regions      ")
        print("  5. stop instance                6. create instance        ")
        print("  7. reboot instance              8. list images            ")
        print("                                 99. quit                   ")
        print("------------------------------------------------------------")

        operation = input("Enter an integer: ")

        ec2 = boto3.resource('ec2')
        ec2_client = boto3.client('ec2')

        instance = Instance(ec2, ec2_client)
        client = Client(ec2_client)

        # 인스턴스 목록 출력
        if operation=='1':
            instance.display()

        # 가용영역 출력
        elif operation=='2':
            client.get_availability_zone()

        # 특정 인스턴스 시작
        elif operation=='3':
            ids = list(input("Enter instance id: ").split())
            if len(ids) == 0:
                print("Please enter correct id")
            else:
                instance.start(ids)

        # 리전 출력
        elif operation=='4':
            client.get_region()

        # 특정 인스턴스 종료
        elif operation=='5':
            ids = list(input("Enter instance id: ").split())
            if len(ids) == 0:
                print("Please enter correct id")
            else:
                instance.stop(ids)

        # 인스턴스 생성
        elif operation=='6':
            ami_id = input("Enter ami id: ")
            if len(ami_id) == 0:
                print("Please enter correct ami id")
            else:
                instance.create(ami_id)

        # 인스턴스 재부팅
        elif operation=='7':
            id = input("Enter instance id: ")
            if id is not None:
                client.reboot(id)

        # AMI 이미지 목록 출력
        elif operation=='8':
            instance.ami_images()

        # 프로그램 종료
        elif operation=='99':
            break

        else:
            print("You entered an invalid integer. Please enter again.")