import boto3
from Instance import Instance
from Alarm import Alarm


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
        print("  9. terminate instance                                     ")
        print("                                 99. quit                   ")
        print("------------------------------------------------------------")

        operation = input("Enter an integer: ")

        ec2 = boto3.resource('ec2')
        client = boto3.client('ec2')

        instance = Instance(ec2, client)

        # 인스턴스 목록 출력
        if operation=='1':
            instance.display()

        # 가용영역 출력
        elif operation=='2':
            instance.get_availability_zone()

        # 특정 인스턴스 시작
        elif operation=='3':
            ids = list(input("Enter instance id: ").split())
            if len(ids) == 0:
                print("Please enter correct id")
            else:
                instance.start(ids)

        # 리전 출력
        elif operation=='4':
            instance.get_region()

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
            ids = list(input("Enter instance id: ").split())
            if len(ids) == 0:
                print("Please enter correct id")
            else:
                instance.reboot(ids)

        # AMI 이미지 목록 출력
        elif operation=='8':
            instance.ami_images()

        # 인스턴스 종료
        elif operation=='9':
            ids = list(input("Enter instance id: ").split())
            if len(ids) == 0:
                print("Please enter correct id")
            else:
                instance.terminate(ids)

        # 프로그램 종료
        elif operation=='99':
            break

        else:
            print("You entered an invalid integer. Please enter again.")