import boto3

class Instance:
    def __init__(self, ec2):
        self.ec2 = ec2

    # 인스턴스 정보 출력
    def display(self):
        if self.ec2 is None:
            print("No instance")
        else:
            for instance in self.ec2.instances.all():
                print(f"[id] {instance.id}, ", end="")
                print(f"[AMI] {instance.image_id}, ", end="")
                print(f"[type] {instance.instance_type}, ", end="")
                print(f"[key] {instance.key_name}, ", end="")
                print(f"[public ip] {instance.public_ip_address}, ", end="")
                print(f"[state] {instance.state['Name']}")

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

class Region:
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
        instance = Instance(ec2)

        client = boto3.client('ec2')
        region = Region(client)

        # 인스턴스 목록 출력
        if operation=='1':
            instance.display()

        # 가용영역 출력
        elif operation=='2':
            region.get_availability_zone()

        # 특정 인스턴스 시작
        elif operation=='3':
            id = input("Enter instance id: ")
            if id is not None:
                instance.start(id)

        # 리전 출력
        elif operation=='4':
            region.get_region()

        # 특정 인스턴스 종료
        elif operation=='5':
            id = input("Enter instance id: ")
            if id is not None:
                instance.stop(id)

        # 인스턴스 생성
        elif operation=='6':
            pass

        # 인스턴스 재부팅
        elif operation=='7':
            pass

        # AMI 이미지 목록 출력
        elif operation=='8':
            pass

        # 프로그램 종료
        elif operation=='99':
            break

        else:
            print("You entered an invalid integer. Please enter again.")