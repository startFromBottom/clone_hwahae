# 버드뷰(화해) 서버 과제 구현


- url : programmer-server-challenge.2pmehxwmw3.ap-northeast-2.elasticbeanstalk.com 


- 로그인 기능 추가로, 로그인 후 api 열람이 가능합니다.

- 로그인 방법 (admin 계정) : user/login url에서 아래 json 


        {
            "username" : "ebadmin",
            "password" : "programmers"
        }

- 로그아웃 방법 : user/logout url 입력

- redoc/v1/, swagger/v1/ url에서 api에 관한 설명이 포함되어 있습니다.

## API 구성(과제 내용)


1. **상품 목록 조회하기 (/products)**

2. **상품 상세 정보 조회하기 (/product/:id)**

    -> 프로젝트 myapp.products 앱에 기능 구현되어 있습니다.

### 추가 구현 (화해 클론)

1. 회원 가입(이메일, 네이버, 구글, 페이스북)
    - production 환경에서 https 미설정으로 네이버, 구글, 페이스북 기능 불가

2. 로그인 기능(이메일, 네이버, 구글, 페이스북)
    - production 환경에서 https 미설정으로 네이버, 구글, 페이스북 기능 불가


