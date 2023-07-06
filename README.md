# pyside6_generic_v23.02
PySide6 기반 파이썬 GUI 앱 개발을 빠르게 시작할 수 있는 프레임워크 입니다.

![example](https://github.com/active0831/pyside6_generic_v23.01/assets/91447903/3e7ba597-0182-411f-b351-7d442a9397af)

- 업데이트 기록: 
 - components.basic 에 LineEditComponent 추가 ( 2023.7.5 )
 - components.image 에 ImageComponent, ImageListComponent 추가 ( 2023.7.6 )

# 파일 구성
편집할 파일
 - main_window.py (파일명 무관)

프레임워크 파일
 - lib.state.py
 - lib.task.py

# Mainwindow
 - 먼저 전체 프로그램에서 공유할 state 를 등록하고, 메인윈도우의 레이아웃 상 각 위치에 별도로 작성한 위젯을 배치한다. 이때, setSideWidget 이라는 함수를 만들어 dockWidget 을 배치하는 코드를 한 줄로 줄이면 보다 가독성을 높일 수 있다. 마지막으로 창 크기 등 디자인 요소들을 설정한다.

# 위젯
- 위젯은 QWidget 또는 Qmenubar 등을 상속받아 작성한다. 먼저 레이아웃을 등록하고, 각 레이아웃에 Component 를 위와 같이 등록한다. React 에서 컴포넌트를 정의하고 불러와서 배치하는 것과 최대한 비슷하게 할 수 있도록 만들었다.
인자로는 컴포넌트의 id 와 배치할 layout 을 필수적으로 받으며, 컴포넌트에 따라 label, 바인딩할 데이터의 state id (model_id), 상호작용 했을 때 실행할 매쏘드 ( onClick ) 등을 받는다.

# 컴포넌트
- layout 을 인자로 필수적으로 받기 때문에, layout 에 컴포넌트(레이아웃 또는 위젯 형식)를 추가함으로써 컴포넌트를 위젯에 등록할 수 있다.
또한, 부여받은 state 값이 변할 때 실행할 update method 를 bind 해 주고, 컨트롤 요소를 작동하였을 때 실행할 onClick 등 매쏘드를 해당 컨트롤 요소에 connect 해 주어야 한다.

# 데이터 바인딩 처리
- State 는 프로그램 어느 곳에서나 접근하여 활용할 수 있도록 singleton 으로 만들었다. use 로 state 를 선언하고, bind 로 선언된 state 에 update method 를 등록하고, set 으로 state 값을 변경하면 등록된 update method 들이 알아서 실행된다. 또한 value 로 state 값을 가져올 수 잇다.

# 비동기 작업 처리
활용은 싱글톤인 Tasks 오브젝트를 불러와서 set 하면 된다. 인자로 들어가는 것들은 다음과 같다.
- task_id : 동일한 id 의 작업이 존재할 경우, 기존의 작업을 중단하고 새로 실행한다.
- task_object : 실제로 실행할 작업을 AbstractTask 를 상속받아 직접 작성한 클래스에 정의한다. 이 때self.update_value 및 self.return_value 를 할당하는 부분이 반드시 있어야 작업 결과를 받아볼 수 있다.
- func_update, func_return 은 작업 도중 또는 작업 후에 결과를 받아 실행할 콜백 함수를 입력한다.



