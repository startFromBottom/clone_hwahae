from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status

"""
Review 관련 api

1. 특정 제품에 대한 리뷰

생성(POST) - 권한 : 로그인한 사람은 모두

읽기(GET) - 권한 : 로그인한 사람은 모두
-> 모두 읽으려할 때, 그 제품에 대한 리뷰를 작성하지 않으면 최대 1개밖에 못봄
리뷰를 1개라도 작성해야 모든 리뷰를 볼 수 있음

업데이트(PUT) - 권한 : 리뷰 작성자

삭제(DELETE) - 권한 : 리뷰 작성자


"""
