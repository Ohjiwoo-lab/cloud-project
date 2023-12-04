# AWS 자원 동적 관리 툴
- Cloud Computing 수업에서 진행하는 프로젝트를 위한 레파지토리입니다.
- 이는 파이썬 SDK로 AWS 가상머신을 동적으로 관리합니다.

## Feature

### Amazon EC2
- [인스턴스 정보 출력](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L10)
- [인스턴스 시작](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L29)
- [인스턴스 중지](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L68)
- [AMI 이미지로부터 인스턴스 생성](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L107)
- [AMI 이미지 정보 출력](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L132)
- [가용영역 출력](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L148)
- [리전 출력](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L166)
- [인스턴스 재부팅](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L183)
- [인스턴스 종료](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Instance.py#L202)

### Amazon SNS를 통한 이메일 알림
> 인스턴스 시작, 인스턴스 중지, 인스턴스 생성, 인스턴스 종료에 대해 알림을 설정할 수 있다.   
> 알림을 설정하면 해당 작업을 수행했을 때마다 이메일로 알림을 보내준다.

- [현재 설정된 알림 확인](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Alarm.py#L11)
- [알림 생성](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Alarm.py#L41)
- [이메일 전송](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Alarm.py#L101)
- [알림 삭제](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Alarm.py#L118)
- [알림을 받을 이메일 수정](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Alarm.py#L151)
- [이메일 검증](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Alarm.py#L226)

### Amazon System Manager Run Command
> 현재 HTCondor의 상태를 출력한다.   
> 마스터 노드에 condor_status를 실행한 결과를 가져온다.

- [condor_status](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Condor.py#L11)

### Amazon CloudTrail
> CloudTrail이 수집한 이벤트 기록을 확인한다.
> IAM에서 사용자 이름을 가져와서 해당 사용자가 수행한 기록만 원하는 개수만큼 출력한다.
- [이벤트 기록 확인](https://github.com/Ohjiwoo-lab/cloud-project/blob/main/Trail.py#L10)