# pyside6_boilerplate_v23.08
PySide6 기반 파이썬 GUI 앱 개발을 빠르게 시작할 수 있는 템플릿 입니다.

![example](https://github.com/active0831/pyside6_generic_v23.01/assets/91447903/3e7ba597-0182-411f-b351-7d442a9397af)

# 설치 
 - 설치 후 실행 : setup.bat
 - 코드(source) 수정 후 실행 : commit_run.bat
 - 실행만 : run.bat
 - 가상환경에 python 모듈 추가 설치 : pip_install.bat 편집 후 실행

# 파일 구성

## 편집할 파일

### 메인 파일
 - bin/main.py

### 모듈 작성
 - bin/modules/

### 컴포넌트, 함수 추가
 - bin/components/
 - bin/helper/

## 기본 라이브러리 ( 편집할 시, 본 템플릿 버전 업데이트 필요 )
 - bin/lib/core  (프레임워크 파일)
 - bin/lib/component ( 기본 컴포넌트 )
 - bin/lib/widget ( 기본 위젯 컴포넌트 )
 - bin/lib/helper ( 기본 헬퍼 함수 )
 - bin/lib/addon ( 선택적으로 활용 가능한 기능 )

# 업데이트 내역
  - v23.08 (2023.7.20.)      
      - 'auth' : 서버 로그인 및 REST API 활용 Addon
      - Task 'repeat' : 일정 시간 간격으로 반복 실행되는 비동기 작업 (기존 'set' 상위 호환)
      - 'settings.py' : 자동 로그인 여부 등 기본값 설정
      - 각 모듈과 애드온에서 Gui 요소를 따로 분리하여 편집
  - v23.07 (2023.7.18.)
      - 기본 라이브러리와 사용자 추가 라이브러리를 분리
  - v23.06 (2023.7.17.)      
      - State 및 위젯을 모듈별로 관리하도록 함
  - v23.05 (2023.7.15.)
      - MplPlotComponent, SliderComponent 추가.
      - State 들이 list 형태로 존재하도록 함.
      - Component 를 배치하면 'widget' 이 레이아웃에 연결되도록 함/
  - v23.04 ( 2023.7.8 )
    - 파이썬이 설치되지 않은 환경에서도 설치 및 실행 가능하도록 함. 
  - v23.03 ( 2023.7.7 )
    - setup.bat 을 통해 venv 및 자동 설치 및 실행할 수 있도록 함. 
  - v23.02 ( 2023.7.6 )
    - components.image 에 ImageComponent, ImageListComponent 추가 
  - v23.01 ( 2023.7.5 )
    - components.basic 에 LineEditComponent 추가 

