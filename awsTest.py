import boto3

class Instance:
    def __init__(self, ec2, client):
        self.ec2 = ec2
        self.client = client

    # 인스턴스 정보 출력
    def display(self):
        try:
            response = self.client.describe_instances()
            if len(response['Reservations']) == 0:
                print('No instance')
            else:
                for instances in response['Reservations']:
                    for instance in instances['Instances']:
                        print(f"[id] {instance['InstanceId']}, ", end="")
                        print(f"[AMI] {instance['ImageId']}, ", end="")
                        print(f"[type] {instance['InstanceType']}, ", end="")
                        print(f"[state] {instance['State']['Name']}, ", end="")
                        print(f"[monitoring state] {instance['Monitoring']['State']}")

        except Exception as e:
            print('get instance error', e)

    # 특정 인스턴스 시작
    def start(self, id):
        flag = False
        for instance in self.ec2.instances.all():
            if instance.id == id:
                print(f"Starting .... {id}")
                instance.start()
                flag = True
                # instance.wait_until_running()
                break
        if flag:
            print(f"Successfully started instance {id}")
        else:
            print("Incorrect Id. Please try again.")

    # 특정 인스턴스 중지
    def stop(self, id):
        flag = False
        for instance in self.ec2.instances.all():
            if instance.id == id:
                instance.stop()
                flag = True
                # instance.wait_until_stopped()
                break

        if flag:
            print(f"Successfully stop instance {id}")
        else:
            print("Incorrect Id. Please try again.")

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
        instance = self.ec2.create_instances(**params, MinCount=1, MaxCount=1)[0]
        print(f"Successfully started EC2 instance {instance.id} based on AMI {ami_id}")

    # AMI 이미지 출력
    def ami_images(self):
        print("Listing images....")

        for image in self.ec2.images.filter(Filters=[{'Name': 'name', 'Values': ['aws-htcondor-slave']}]):
            print(f"[ImageId] {image.id}, [Name] {image.name}, [Owner] {image.owner_id}")

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
            id = input("Enter instance id: ")
            if id is not None:
                instance.start(id)

        # 리전 출력
        elif operation=='4':
            client.get_region()

        # 특정 인스턴스 종료
        elif operation=='5':
            id = input("Enter instance id: ")
            if id is not None:
                instance.stop(id)

        # 인스턴스 생성
        elif operation=='6':
            ami_id = input("Enter ami id: ")
            if ami_id is not None:
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