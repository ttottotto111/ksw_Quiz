# 초기 설정
> ## quiz 폴더  
### .env파일 수정
- ./quiz/.env 수정필요
- django key 및 db정보는 별도 파일로 관리
```
SECRET_KEY='django_key'
DB_NAME='db_name'
DB_USER='db_user'
DB_PASSWORD='db_password'
DB_HOST='host'
DB_PORT='port'
```

### db 연동
```bash
python manage.py makemigrations
python manage.py migrate
```

# API
    #### 기본url에 swagger 등록, 전체 api확인 가능.
    #### 아래 api 설명 추가 참고
## 1. account
사용자 계정 관리 app
### 일반사용자 계정 생성
- url

    ```
    account/signup-user/
    ```
- 요청 예시
    ```JSON
    {
        "username": "name",
        "password": "password"
    }
    ```
### 관리자 계정 생성
- url
    ```
    account/signup-admin/
    ```
- 요청 예시
    ```JSON
    {
        "username": "name",
        "password": "password"
    }
    ```

## 2. quiz_manager
quiz 관리(조회, 생성, 수정, 삭제) 앱
### - 생성 (POST)
- url
    ```
    quiz/
    ```
- 요청 예시
    ```JSON
    {
        "title": "퀴즈 제목",
        "questions_count": 10,
        "questions": [
            {
                "title": "문제1",
                "answer": ["선택지1", "선택지2", "선택지3"],
                "correct_answer": "선택지1"
            },
            {
                "title": "문제2",
                "answer": ["선택지1", "선택지2", "선택지3", "선택지4"],
                "correct_answer": "선택지4"
            }
        ]
    }
    ```

### - 조회 (GET)  
- url
    ```
    quiz/
    ```
- 응답 예시
    ```JSON
    {
        "id" : 0
        "title": "퀴즈 제목",
        "questions_count": 10,
        "questions": [
            {
                "id" : 0,
                "title": "문제1",
                "answer": ["선택지1", "선택지2", "선택지3"],
                "correct_answer": "선택지1"
            },
            {
                "id" : 1,
                "title": "문제2",
                "answer": ["선택지1", "선택지2", "선택지3", "선택지4"],
                "correct_answer": "선택지4"
            }
        ]
    }
    ```

### - 수정 (PUT/PATCH)
- url
    ```
    quiz/{quiz id}/
    ```
- 요청 예시
    ```JSON
    {
        "title": "퀴즈 제목",
        "questions_count": 10,
        "questions": [
            {
                "title": "문제1",
                "answer": ["선택지1", "선택지2", "선택지3"],
                "correct_answer": "선택지1"
            },
            {
                "title": "문제2",
                "answer": ["선택지1", "선택지2", "선택지3", "선택지4"],
                "correct_answer": "선택지4"
            }
        ]
    }
    ```

### 삭제 (DELETE)
- url
    ```
    quiz/{quiz id}/
    ```

## 3. quiz_board
퀴즈 게시판 관리 앱
### - 관리자용 게시판 설정 (PUT/PATCH)
1시간 간격으로 설정정보를 캐싱 진행  
관리자가 수정한 경우 캐싱정보 갱신
- url
    ```
    /board/setting/1/
    ```
- 요청 예시  
quiz_paging : 퀴즈 목록 페이징 개수. default = 10  
question_paging : 퀴즈 내 문제 페이징 개수. default = 10  
question_random : 퀴즈 내 문제 순서 랜덤 여부. default = False  
choice_random : 문제 선택지 랜덤 여부. default = False
    ```JSON
    {
        "quiz_paging": 10,
        "question_paging": 10,
        "question_random": false,
        "choice_random": false
    }
    ```


### - 퀴즈 목록 조회 (GET)
quiz_id : 질문 정보  
질문 정보의 경우 상세 조회에서만 출력될 수 있도록 설정
- url  
filter : 전체/응시한/응시하지않은 퀴즈 선택 조회 옵션 default는 전체조회 (응시한 : solved / 응시하지않은 notsolved / 전체 all)
    ```
    /board/?filter={filter}&page={page_num}
    ```
- 응답 예시
    ```JSON
    {
        "count": 12,
        "next": "/board/?page=2",
        "previous": null,
        "results": [
            {
                "id": 18,
                "title": "퀴즈 제목",
                "questions_count": 10,
                "quiz_id": []
            },
            {
                "id": 17,
                "title": "퀴즈 제목",
                "questions_count": 10,
                "quiz_id": []
            }
    }
    ```

### - 퀴즈 상세 정보 (GET)
- url
    ```
    /board/{quiz_id}/?page={page_num}
    ```
- 응답예시
    ```JSON
    {
        "count": 10,
        "next": "http://127.0.0.1:8000/board/12/?page=2",
        "previous": null,
        "results": {
            "quiz_id": [
                    {
                    "id": 18,
                    "title": "문제2",
                    "answer": [
                        "선택지2",
                        "선택지1",
                        "선택지3",
                        "선택지4"
                        ]
                    },
                    {
                    "id": 18,
                    "title": "문제2",
                    "answer": [
                        "선택지2",
                        "선택지1",
                        "선택지4",
                        "선택지3"
                    ]
                }
            ]
        }
    }
    ```

## 4. exam
퀴즈 응시 관리 앱
### 시험 생성 (POST)
관리자가 설정한 설정값 (질문 개수, 질문 랜덤, 선택지 랜덤)에 따라 퀴즈 문제 출제  
해당 시험 문제는 세션에 저장
- url
    ```
    /exam/{quiz_id}/exam-start/
    ```
- 응답 예시
    ```JSON
    {
        "message": "start quiz",
        "questions": [
            {
                "id": 17,
                "title": "문제1",
                "answer": [
                    "선택지2",
                    "선택지1",
                    "선택지3"
                ]
            },
            {
                "id": 18,
                "title": "문제2",
                "answer": [
                    "선택지1",
                    "선택지2",
                    "선택지3",
                    "선택지4"
                ]
            }
        ]
    }
    ```
### 시험 페이지 (GET)
시험 생성 api로 생성된 시험을 응시하는 페이지 api  
관리자가 설정한 질문 페이징에 따라 페이징 진행
- url
    ```
    /exam/{quiz_id}/exam-page/?page={page_num}
    ```
- 응답예시
    ```JSON
    {
        "page": 1,
        "total_pages": 2,
        "questions": [
            {
                "id": 17,
                "title": "문제1",
                "answer": [
                    "선택지2",
                    "선택지1",
                    "선택지3"
                ]
            },
            {
                "id": 18,
                "title": "문제2",
                "answer": [
                    "선택지1",
                    "선택지2",
                    "선택지3",
                    "선택지4"
                ]
            }
        ]
    }
    ```

### 시험 결과 제출 (POST)
시험 페이지에서 본 응답 데이터를 받아 스코어 계산 후 응시 이력 db에 저장
- url
    ```
    /exam/{quiz_id}/exam-submit/
    ```
- 요청 예시  
question_num : 문제 번호  
user_answer : 유저가 입력한 답변  

    ```JSON
    {
        "answers" : [
            {
                "question_num" : 1,
                "user_answer" : "선택지1"
            },
            {
                "question_num" : 2,
                "user_answer" : "선택지4"
            }
        ]
    }
    ```
- 응답 예시  
title : 퀴즈 제목  
question_count : 문제 전체 개수  
score : 맞힌 문제 개수  

    ```JSON
    {
            "message" : "submit success",
            "title" : "Quiz 1",
            "question_count" : 10,
            "score" : 5
    }
    ```