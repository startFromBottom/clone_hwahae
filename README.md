# 버드뷰(화해) 서버 과제 구현


- url : programmer-server-challenge.2pmehxwmw3.ap-northeast-2.elasticbeanstalk.com 


- 로그인 기능 추가로, 로그인 후 api 열람이 가능합니다.

- 로그인 방법 (admin 계정) : user/login url에서 아래 json 입력


        {
            "username" : "ebadmin",
            "password" : "programmers"
        }

- 로그아웃 방법 : user/logout url 입력

- redoc/v1/, swagger/v1/ url에서 api에 관한 설명이 포함되어 있습니다.

## API 구성(과제 내용) - 프로젝트 myapp.products 앱에 기능 구현되어 있습니다.


1. **상품 목록 조회하기 (/products)**

2. **상품 상세 정보 조회하기 (/product/:id)**

- 테스트 코드  
    test_models.py, test_queryparams_validators.py, test_serializers.py, test_views.py 

### 추가 구현 (화해 클론)


1. admin 기능(url : admin/)

2. 사용자 관련 기능(myapp.users 앱에 기능 구현되어 있습니다.)

    url : users/

    1) 회원 가입(이메일, 네이버, 구글, 페이스북)
        - production 환경에서 https 미설정으로 네이버, 구글, 페이스북 OAuth 불가

    2) 로그인 기능(이메일, 네이버, 구글, 페이스북)
        - production 환경에서 https 미설정으로 네이버, 구글, 페이스북 OAuth 불가

    3) 이메일로 회원 가입 시, 이메일 인증 기능

    4) 회원의 개인 정보 확인

    5) 내가 쓴 리뷰 목록 확인

    6) 내가 쓴 특정 리뷰 확인, 수정, 삭제

    5) 내가 스크랩한 리뷰 목록 확인

    6) 내가 스크랩한 특정 리뷰 확인, 수정, 삭제


3. 리뷰 관련 기능(myapp.reviews 앱에 기능 구현되어 있습니다.)

    url : reviews/

    1) 특정 제품의 모든 리뷰 확인

    2) 특정 제품에 대한 특정 리뷰 생성, 확인, 수정, 삭제

    3) 특정 리뷰의 사진 업로드, 확인, 수정, 삭제

    4) 특정 리뷰 스크랩

    5) 특정 리뷰에 좋아요 누르기


4. 리뷰에 대한 댓글 관련 기능(myapp.comments -> 미구현)



### 사용 서드파티 앱

1. rest_framework

2. debug_toolbar (디버깅)

3. sslserver (local환경에서 https 접속)

4. django_seed (가짜 데이터 생성)

5. storages (static 파일, 업로드 파일 관리)

6. drf_yasg (api 문서화)
    




