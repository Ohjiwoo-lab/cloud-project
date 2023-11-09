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
        print(f"Starting .... {id}")

        for instance in self.ec2.instances.all():
            if instance.id == id:
                response = instance.start()
                print(response)
                instance.wait_until_running()
                break

        print(f"Successfully started instance {id}")

    # 특정 인스턴스 중지
    def stop(self, id):
        for instance in self.ec2.instances.all():
            if instance.id == id:
                response = instance.stop()
                print(response)
                instance.wait_until_stopped()
                break

        print(f"Successfully stop instance {id}")


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
        if operation=='1':
            instance.display()

        elif operation=='2':
            pass

        elif operation=='3':
            id = input("Enter instance id: ")
            if id is not None:
                instance.start(id)

        elif operation=='4':
            pass

        elif operation=='5':
            id = input("Enter instance id: ")
            if id is not None:
                instance.stop(id)

        elif operation=='6':
            pass

        elif operation=='7':
            pass

        elif operation=='8':
            pass

        elif operation=='99':
            break

        else:
            print("You entered an invalid integer. Please enter again.")