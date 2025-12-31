### 도커를 이용한 ubuntu 설치
- docker 공식사이트에서 자신의 운영체재에 맞는 버전 설치(window :  ..... AMD64)
- powershell을 관리자 권한으로 열어서
- wsl --install
- 재부팅
- docker desktop 실행해서 docker가 실행상태
- powershell에서 docker info 정상 실행 확인
- docker run -it ubuntu bash  실행해서 컨터이너 안의 ubuntu에 접속한다


### 1. 디렉토리 이동 및 위치 확인
- `pwd`: 현재 위치한 디렉토리의 경로를 출력합니다.
- `ls`: 현재 디렉토리의 파일과 폴더 목록을 보여줍니다.
- `ls -al`: 숨겨진 파일을 포함하여 상세 정보를 출력합니다.
- `cd /`: 최상위(root) 디렉토리로 이동합니다.
- `cd ~`: 현재 사용자의 홈 디렉토리로 이동합니다.

### 2. 파일 및 디렉토리 관리
- `mkdir my_folder`: 'my_folder'라는 이름의 새 디렉토리를 만듭니다.
- `touch hello.txt`: 내용이 비어있는 'hello.txt' 파일을 생성합니다.
- `echo "Hello Linux" > hello.txt`: 파일에 텍스트를 입력합니다.
- `cat hello.txt`: 파일의 내용을 터미널에 출력합니다.
- `cp hello.txt copy.txt`: 파일을 복사합니다.
- `mv copy.txt my_folder/`: 파일을 폴더 안으로 이동시킵니다.
- `rm hello.txt`: 파일을 삭제합니다.
- `rm -rf my_folder`: 디렉토리와 그 안의 내용을 모두 강제로 삭제합니다.

### 3. 리눅스 디렉토리 구조(FHS)
```
윈도우와 달리 C D 드라이브 개념이 없고 모든 것인 루트(/)에서 시작하는 단일 구조
```
- /(Root) : 최상위
- /bin & /usr/bin : 기본적인 명령어들(ls, cp)이 위치한 곳
- /etc : 시스템 설정 파일들의 보관소(윈도우의 제어판 + 레지스트리 역활)
- /home : 일반사용자들의 개인 디렉토리
- /var : 로그파일, 데이터베이스 등 수시로 변화는 파일 저장소
- /tmp : 임시 파일 저장소, 재부팅시 자동삭제가 될수도 있는 파일들

### 4. 목록 보기
- cd /etc
- ls                      # 그냥 이름만 보기
- ls -l                   # 상세 정보 보기 (권한, 소유자, 크기, 날짜)
- ls -a                   # 숨겨진 파일(.으로 시작)까지 모두 보기
- ls -al                  # 숨겨진 파일을 포함해 상세 정보 보기
- ls -lh                  # 파일 크기를 사람이 읽기 편하게(K, M, G 단위) 표시
- ls -R                   # 하위 디렉토리 내용까지 펼쳐서 보기 (재귀적, 스크롤 주의!)
- ls -d */                # 파일은 제외하고 디렉토리만 골라서 보기

### 5. 디렉토리 생성
- cd ~
- mkdir project                   # 폴더 하나 생성
- mkdir -p project/backend/api    # 하위 폴더까지 한 번에 생성 (-p: parents)
- mkdir project/frontend project/db # 여러 폴더 동시에 생성
- ls -R project                   # 구조 확인

### 6. 파일생성
- cd project
- touch README.md                 # 빈 파일 생성
- touch index.html style.css      # 여러 파일 동시 생성
- touch .gitignore                # 숨김 파일 생성
- ls                              # .gitignore 안 보임
- ls -a                           # 이제 보임

### 7. 복사의 다양한 옵션
- cp README.md README_bak.md      # 파일 복사
- cp -r backend backend_backup    # 폴더 통째로 복사할 땐 -r (recursive) 필수!
- cp -v index.html index_v2.html  # 복사 과정을 자세히 출력 (-v: verbose)

### 8. 이동(mv)와 이름변경
- mv style.css frontend/
- mv index_v2.html old_index.html # 이름 변경 (같은 폴더 내 이동 = 이름 변경)

### 9. 삭제(rm) - 주의
- rm old_index.html               # 파일 삭제 (되살릴 수 없음!)
- rm -r backend_backup            # 폴더 삭제는 -r 필수
- rm -rf project/db               # 묻지도 따지지도 않고 강제 삭제 (-f: force, 매우 위험)
# *주의: rm -rf / 명령은 시스템 전체를 날릴 수 있습니다. 절대 금지!*

```
my_work라는 폴더를 만들고 그 안에 year_2024, year_2025 폴더를 만드세요.
year_2024 안에 report1.txt, report2.txt, image.jpg 파일을 만드세요.
와일드카드(*)를 사용하여 year_2024의 모든 .txt 파일을 year_2025로 복사하세요.
year_2024 폴더를 통째로 archive라는 이름으로 변경하세요.
archive 폴더 안에 있는 image.jpg를 삭제하세요.
```

### 10 도커 컨터이너 확인 및 실행
- docker run -it ubuntu bash  # 도커를 이용해서 ubuntu를 컨테이너에 넣고 실행하고 컨테이너에 진입
- docker ps -a  # 현재 실행 및 종료된 컨테이너 목록
- 만약에 중지되어 있으면 docker desktop으로 실행 또는 docker start [CONTAINER ID]
- 실행중인 컨테이너 안에 진입 : docker exec -it [CONTAINER ID] bash

### 11 에디터
- apt update && apt install nano -y   # 패키지 목록 갱신 후 nano 설치
- ls -R /etc > file_list.txt      # /etc 목록을 파일로 저장 (내용이 꽤 김)
- cat file_list.txt               # 순식간에 지나가서 앞부분을 못 봄
- head -n 5 file_list.txt         # 딱 첫 5줄만 보기
- tail -n 5 file_list.txt         # 딱 마지막 5줄만 보기

```
nano 에디터
```
- 입력 : "ServerIP = 127.0.0.1" 입력
- 복사/붙여넣기 : Alt+6( 복사 )  Ctrl+U (붙여넣기)
- 잘라내기 : Ctrl+k (한줄 삭제/ 잘라내기)
- 검색 : Ctrl+w  누르고 찾을 단어 입력
- 저장 및 종료 : Ctrl+o(Write out) -> Enter -> Ctrl+x(Exit)