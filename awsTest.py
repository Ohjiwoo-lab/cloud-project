import boto3

# 인스턴스 정보 출력
class Instance:
    def __init__(self, ec2):
        self.ec2 = ec2

    def display(self):
        for instance in self.ec2.instances.all():
            print(f"[id] {instance.id}, ", end="")
            print(f"[type] {instance.instance_type}, ", end="")
            print(f"[key] {instance.key_name}, ", end="")
            print(f"[public ip] {instance.public_ip_address}, ", end="")
            print(f"[state] {instance.state['Name']}")


if __name__ == '__main__':
    ec2 = boto3.resource('ec2')
    instance = Instance(ec2)
    instance.display()