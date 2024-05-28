# AWS 리소스 동적 관리 프로젝트

4학년 2학기 Cloud Computing 수업에서 진행한 프로젝트입니다. AWS EC2 인스턴스로 HTCondor Cluster를 구축한 뒤, 파이썬 SDK인 boto3로 클러스터를 동적으로 관리하는 프로그램을 제작했습니다.

## 사용한 서비스

- AWS EC2
- AWS SNS
- AWS EventBridge
- AWS CloudTrail
- AWS Systems Manager Run Command
- Terraform
- Ansible

## 주요 기능

- Terraform과 Ansible을 이용한 초기 환경 구축

- EC2 인스턴스 생성, 시작, 중지, 재부팅, 종료

- 이벤트 기반 이메일 알림 서비스
    - 현재에는 인스턴스 시작, 중지, 생성, 종료에 대한 알림을 설정할 수 있습니다.

- HTCondor Cluster 상태 확인

> 자세한 설명은 [위키](https://github.com/Ohjiwoo-lab/cloud-project/wiki)를 참고해주세요!

## 설치 환경

- Ansible: 2.10.8
- Terraform: v1.6.5
- Python: 3.10.12
- Ubuntu: 22.04.4 LTS
- aws cli: 2.15.24

## Setting

1. AWS 설정

    ```
    aws configure
    ```
    - AWS 서비스를 사용하기 위한 액세스 키를 입력합니다.

2. 필요한 라이브러리 설치

    ```
    pip install -r requirements.txt
    ```
    - 가상환경을 따로 만드는 것을 추천드립니다.

3. Key Pair 생성

    ```
    cd setup/
    mkdir key/
    ssh-keygen -t rsa -b 4096 -C "" -f "key/ansible_keypair" -N ""
    ```

    - 프라이빗 키와 퍼블릭 키로 사용될 키 2개가 생성됩니다.

4. Terraform 실행

    ```
    terraform init
    terraform plan
    terraform apply
    ```

    - 프로그램 실행에 필요한 모든 리소스가 생성되고 환경 설정이 이루어집니다.

5. 프로그램 실행

    ```
    cd ../
    python3 awsTest.py
    ```

*만약 모든 리소스를 삭제하고 싶다면 setup 폴더에서 `terraform destroy` 명령어를 입력하면 됩니다.*