# AWS 리소스 동적 관리 프로젝트 개요

4학년 2학기 Cloud Computing 수업에서 진행한 프로젝트입니다. AWS EC2 인스턴스로 HTCondor Cluster를 구축한 뒤, 파이썬 SDK인 boto3로 클러스터를 동적으로 관리하는 프로그램을 제작했습니다.

**사용한 AWS 서비스**

- AWS EC2
- AWS SNS
- AWS EventBridge
- AWS CloudTrail
- AWS Systems Manager Run Command

**주요 기능**

- EC2 인스턴스 생성, 시작, 중지, 재부팅, 종료

- 이벤트 기반 이메일 알림 서비스
    - 현재에는 인스턴스 시작, 중지, 생성, 종료에 대한 알림을 설정할 수 있습니다.

- HTCondor Cluster 상태 확인

> 자세한 설명은 [위키](https://github.com/Ohjiwoo-lab/cloud-project/wiki)를 참고해주세요!