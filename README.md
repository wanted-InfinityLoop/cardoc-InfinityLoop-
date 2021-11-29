# 🎊 Wanted X Wecode PreOnBoarding Backend Course | 무한루프 팀 개인 과제

원티드 4주차 기업 과제 : Cardoc Assignment Project
✅ 카닥 기업 개인 과제입니다.

- [카닥 사이트](https://www.cardoc.co.kr/)
- [카닥 채용공고 링크](https://www.wanted.co.kr/company/6)

<br>
<br>

# 🔖 목차

- 과제 내용
- 기술 환경 및 tools
- 모델링 ERD
- API 명세서
- 기능 구현 추가설명
- 설치 및 실행 방법
<br>
<br>

# 📖 과제 내용

### **[필수 포함 사항]**

- README 작성
  - 프로젝트 빌드, 자세한 실행 방법 명시
  - 구현 방법과 이유에 대한 간략한 설명
  - 서버 구조 및 디자인 패턴에 대한 개략적인 설명 
  - 완료된 시스템이 배포된 서버의 주소
  - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- `Swagger`나 `Postman`을 이용하여 API 테스트 가능하도록 구현

### **[개발 요구 사항]**

- 데이터베이스로 RDB 사용
- 데이터베이스 관련 처리 ORM 사용
- 과제에서 제시한 반환 코드 사용

### **[기능 개발]**

✔️ **REST API 기능**

- 사용자 생성 API
- 사용자가 소유한 타이어 정보를 저장하는 API
- 사용자가 소유한 타이어 정보 조회 API  

<br>
<br>

# ➡️ Build(AWS EC2)

API URL : http://{}

<br>
<br>

# ⚒️ 기술 환경 및 tools

- Back-End: `Python 3.9.7`, `Django 3.2.9`
- Deploy: AWS `EC2`, `SQLlite 3.36.0`
- ETC: `Git`, `Github`, `Postman`

<br>
<br>

# 📋 모델링 ERD

![카닥db](https://user-images.githubusercontent.com/77820352/143791798-2ef7a0d4-2766-40cd-982a-444e11a8c092.png)

<br>
<br>

# 🌲 디렉토리 구조

```
.
├── config
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── models.py
│   ├── tests.py
│   ├── validator.py
│   └── views.py
└── users
│    ├── admin.py
│    ├── apps.py
│    ├── models.py
│    ├── tests.py
│    ├── urls.py
│    └── views.py
├── cars
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── CONVENTION.md
├── PULL_REQUEST_TEMPLATE.md
├── README.md
├── db.sqlite3
├── manage.py
├── my_settings.py
├── requirements.txt

```

<br>
<br>

# 🔖 API 명세서

[Postman API Document 보러가기](https://documenter.getpostman.com/view/18212819/UVJckGcb)

<br>

### 👉 사용자 생성 API

[회원가입]

1. 유저의 아이디와 비밀번호를 요청 본문에 담아 전달한다.
1. 이미 등록된 아이디는 아닌지, 비밀번호는 특수문자, 숫자, 문자 포함 8자 이상인지 검증한다.
1. 비밀번호는 암호화되어 저장된다.

- Method: POST

```
http://{}/users/signup
```

<br>

- parameter : request_body

```
{
    "id" : "dreamcar",
    "password" : "AsSdfd@3f"
}
```

<br>

- response

```
{
    "message": "SUCCUESS"
}
```

<br>

[로그인]

1. 유저의 아이디와 비밀번호를 통해서 유저를 검증 한다.
2. 로그인 성공 시, user_id 정보를 담은 access_token을 반환한다.

- Method: POST

```
http://{}/users/login
```

<br>

- parameter : request_body

```
{
    "id" : "dreamcar",
    "password" : "AsSdfd@3f"
}
```

<br>

- response

```
{
    "message": "SUCCESS",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImRyZWFtY2FyIiwiZXhwIjoxNjM4MTcyOTAzfQ.T8qLAegIKqD1chDPW8BcfoN4ukoUqfWMgBNY_TYWR0M"
}
```

<br>

### 👉 사용자가 소유한 타이어 정보를 저장하는 API

1. 유저 아이디와 자동차 차종 아이디를 요청 본문에 담아 요청합니다.
1. 최대 5명까지 요청할 수 있고, 그 이상 요청시 에러를 반환한다.
1. 해당 아이디의 유저가 있는지 조회하고, 없으면 에러를 반환한다.
1. 유저가 있을 시, 해당 자동차 차종 아이디로 외부 API를 호출한다. 
1. 자동차 정보와 트림이 없으면 생성하고, 있으면 해당 객체를 가져온다.
1. 가져온 타이어 정보를 폭, 편평비, 휠 사이즈로 나누어 저장한다.
1. 키값이 없으면 에러를 반환한다.

<br>

- Method: POST

```
http://{}/cars/tire-info
```

<br>

- parameter : request_body

```
[
  {
    "id": "candycandy",
    "trimId": 5000
  },
  {
    "id": "mylovewolkswagen",
    "trimId": 9000
  },
  {
    "id": "bmwwow",
    "trimId": 11000
  },
  {
    "id": "dreamcar",
    "trimId": 15000
  }
]
```

<br>

- response

```
{
    "message": "SUCCESS"
}
```

<br>

### 👉 사용자가 소유한 타이어 정보 조회 API

1. 인증된 사용자만 타이어 정보 조회 API 호출이 가능하다.
1. 헤더로 전달한 토큰으로 유저가 있는지 조회한다.
1. 토큰이 없거나, 유효한 토큰이 아니거나, Bearer 토큰이 아니면 에러를 반환한다.
1. 유저 아이디로 트림 객체를 가져오고, 참조하는 타이어 정보를 가져온다.
1. 트림 객체가 없을 시 에러를 반환한다.
1. 키값이 없으면 에러를 반환한다.

<br>

- Method: GET

```
http://{}/cars/tire-info
```

<br>

- header : Bearer token

- response

```
{
     "tire_info": [
        {
            "name": "타이어 전",
            "width": 245,
            "aspect_ratio": 45,
            "wheel_size": 19
        },
        {
            "name": "타이어 후",
            "width": 275,
            "aspect_ratio": 40,
            "wheel_size": 19
        }
    ]
}
```

<br>
<br>

# 🔖 설치 및 실행 방법

### 로컬 및 테스트용

1. 해당 프로젝트를 clone하고, 프로젝트로 들어간다.

```
https://github.com/wanted-InfinityLoop/cardoc-InfinityLoop-jy.git
```

2. 가상환경으로 miniconda를 설치한다. [Go](https://docs.conda.io/en/latest/miniconda.html)

```
conda create -n cardoc python=3.9
conda actvate cardoc
```

3. 가상환경 생성 후, requirements.txt를 설치한다.

```
pip install -r requirements.txt

Django==3.2.9
django-cors-headers==3.10.0
gunicorn==20.1.0
bcrypt==3.2.0
PyJWT==2.3.0
requests==2.26.0

```

4. migrate 후 로컬 서버 가동

```
python manage.py migrate
python manage.py runserver
```
