# pyside6_boilerplate_v23.06
PySide6 기반 파이썬 GUI 앱 개발을 빠르게 시작할 수 있는 템플릿 입니다.

![example](https://github.com/active0831/pyside6_generic_v23.01/assets/91447903/3e7ba597-0182-411f-b351-7d442a9397af)

# 설치 
 - 설치 및 실행 : setup.bat
 - 설치 후 실행만 : run.bat
 - 가상환경에 python 모듈 추가 설치 : pip_install.bat 편집 후 실행

# 파일 구성

## 편집할 파일

### 메인 파일
 - bin/main.py

### 추가 모듈
 - bin/modules/

### 추가 컴포넌트
 - bin/components/

## 프레임워크 파일 (필요 시 편집)
 - bin/lib/state.py
 - bin/lib/task.py
 - bin/lib/widget.py

## 예제 파일
 - examples/
 - 의존 라이브러리는 개별적으로 설치가 필요할 수 있음

# 업데이트 내역
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

