from Instance import Instance
from Alarm import Alarm
from Condor import Condor
from Trail import Trail


if __name__ == '__main__':
    instance = Instance()
    alarm = Alarm()
    condor = Condor()
    event = Trail()

    # 초기 구성하는 것 구현할 예정.
    '''
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': ['master']
            }
        ]
    )
    for master in response['Reservations']:
        for node in master['Instances']:
            if node['State']['Name'] != 'running':
                print("The master node is stopped. Starting a master node.")
                ec2.instances.filter(InstanceIds=[node['InstanceId']]).start()
    '''

    while True:
        print("                                                             ")
        print("                                                             ")
        print("-------------------------------------------------------------")
        print("           Amazon AWS Control Panel using SDK                ")
        print("-------------------------------------------------------------")
        print("  1. list instance               2. available zones          ")
        print("  3. start instance              4. available regions        ")
        print("  5. stop instance               6. create instance from ami ")
        print("  7. reboot instance             8. list images              ")
        print("  9. terminate instance          10. condor status           ")
        print("  11. list alarm                 12. create alarm            ")
        print("  13. delete alarm               14. modify email for alarm  ")
        print("  15. event history              16. connect to instance     ")
        print("                                 99. quit                    ")
        print("-------------------------------------------------------------")

        operation = input("Enter an integer: ")

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

        # condor status
        elif operation=='10':
            condor.status()

        # 설정된 알람 확인
        elif operation=='11':
            alarm.list()

        # 알람 생성
        elif operation=='12':
            alarm.create_alarm()

        # 알람 삭제
        elif operation=='13':
            alarm.delete()

        # 알림받을 이메일 수정
        elif operation=='14':
            alarm.modify()

        # 그동안 수행한 작업 확인하기
        elif operation=='15':
            event.event_log_by_count()

        # 마스터 노드 접속
        elif operation=='16':
            condor.console()

        # 프로그램 종료
        elif operation=='99':
            break

        else:
            print("You entered an invalid integer. Please enter again.")