CCTV를 통한 5인 집합 탐지 모델 
====
Simple Group Detector with python , Opencv


## 0. 들어가기에 앞서
----
이 모델은 과학기술 기반 치안현장 문제해결 '과학치안 아이디어 공모전' 에 접수하며 개발한 코드이며,

CV Library 에서 기본적으로 제공하는 물체 인식 알고리즘을 통하여 간단하고 빠른 사람 형태 인식 모델을 구현하였고

룸 술집, 룸노래방 , 빌라 등에 5인 이상 집합하는 경우를 방지하는 기대 효과를 제시하였습니다.


## 1. 사용 환경 및 라이브러리
----

* python == 3.6
* cvlib - 탐지 알고리즘 사용
* cv2 - 영상 , 사진 로드

## 2. 코드 분석
----
탐지 모델의 코드는 __Group_Check_App__ 이라는 클래스를 통해 구현하였습니다.

### 2.1 생성자

```
def __init__(self,PATH):
        if PATH == 'cam': # 캠으로 탐지
            self.cam = cv2.VideoCapture(0)
            self.isVideo = True
        elif (PATH.split('.')[-1] == 'mp4') or (PATH.split('.')[-1] == 'avi'): # 저장된 동영상으로 탐지
            self.cam = cv2.VideoCapture(PATH)
            self.isVideo = True
        else:
            self.frame = cv2.imread(PATH) # 이미지 파일로 탐지
            self.isVideo = False
        if self.isVideo and not self.cam.isOpened(): # 영상 로드 확인
            print('Load Failed! Check File Path') 
        else:  
            #윈도우 배치
            cv2.namedWindow('frame')
            cv2.namedWindow('after_frame')
            cv2.moveWindow('frame',100,200)
            cv2.moveWindow('after_frame',800,200)
            
            self.Detector(PATH) #탐지 메서드
```

PATH 라는 인자를 통해 객체를 생성하며, PATH 가 이미지라면 _self.isVideo = False_ , Path 가 동영상 , 웹캠 이라면 _self.isVideo = True_ 로 설정하게 하였습니다.

그 후, 윈도우를 배치하고 탐지 메서드 _self.Detector_ 를 실행하였습니다.

### 2.2 Detector 메서드 - 영상

```
def Detector(self,PATH):
        if self.isVideo: #동영상 탐지
            print('press q to quit')
            while self.cam.isOpened(): #동영상 프레임이 남은동안 반복
                persons = []
                status, frame = self.cam.read()
                cv2.imshow('frame',frame)
                rect,obj,conf = cv.detect_common_objects(frame,enable_gpu=True) # 영상 속 개체 탐지
                _ = [persons.append(rect[i]) for i in range(len(rect)) if obj[i] == 'person' and conf[i] >= 0.6] # 개체 중 '사람'이고 확률이 60% 이상인 개체만 추출
                
                for person in persons:
                    l,t,r,b = person #좌표 로드
                    if len(persons) >= 5: # person above 5
                        cv2.rectangle(frame,(l,t),(r,b),(0,0,255),3) #초록색 네모로 사람의 Bounding Box 그림
                    else: # person under 5    
                        cv2.rectangle(frame,(l,t),(r,b),(0,255,0),3) #빨간색 네모로 사람의 Bounding Box 그림

                cv2.putText(frame,'Person Counts : {}'.format(str(len(persons))),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0)) # 사람의 수 출력
                cv2.imshow('after_frame',frame)

                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    self.cam.release()
                    cv2.destroyAllWindows()
                    break
```

_self.isVideo_ 가 True일 때, cvlib의 _detect_common_object()_ 를 통하여 영상 프레임에서 개체를 탐지합니다. (_enable_gpu_ 옵션은 CPU 만 사용하는 컴퓨터에 경우 False로 변경합니다.)

그 후, 인식된 개체 중 object = 'person' 인 개체만 추출하는 명령어를 통하여 사람의 Bounding Box 만 persons 리스트에 저장합니다.
```
_ = [persons.append(rect[i]) for i in range(len(rect)) if obj[i] == 'person' and conf[i] >= 0.6]
```

그 다음에, persons 리스트의 사람 수만큼 프레임의 사람 영역에 사각형을 그리고, 5인 이상일 경우 붉은색 , 이하일 경우 연두색으로 색을 따로 지정합니다.

프레임의 왼쪽 상단에는 인식된 사람의 수를 출력하는 _cv2.puttext()_ 함수도 함께 사용하였습니다.


### 2.2 Detector 메서드 - 이미지

이미지의 경우 영상의 _while self.cam.isOpened():_ 구문만 빼면 거의 유사하지만 이미지가 너무 클 경우 창이 안 이쁘기 때문에

_cv2.resize()_ 함수를 통하여 이미지의 크기를 통일합니다.

그 후에 Bounding box 가 그려진 frame을 새로 저장합니다.


## 3. 테스트
```
print('\nInput File Path (input cam to use Webcam)')
PATH = input()
Group_Check_App(PATH)
```
입력된 문자열을 통해 클래스 객체를 생성하고, 탐지 결과를 반환합니다.

Dataset 폴더에 저장되어 있는 karaoke.jpg 를 불러 보았습니다.

![주석 2021-08-30 173015](https://user-images.githubusercontent.com/77887166/131310365-cfede508-3113-4a82-a34d-338e32155956.jpg)

노래방에 설치된 CCTV라고 가정했을 때, 사람의 수를 잘 찾아내는 것 같습니다!

![주석 2021-08-30 173232](https://user-images.githubusercontent.com/77887166/131310709-b1a0fc04-6eef-4fc4-96ab-ea615f6cb2db.jpg)

5인 이상 인식된 경우를 볼까요? 사람 뒤에 가려진 사람 한명이 인식이 안됬지만 대부분의 사람은 잘 찾아낸 것 같습니다.



## 4. 파이썬 Script 로 변환

이 부분은 생략 가능하지만, 쥬피터 노트북 (.ipynb) 형식을 파이썬 스크립트(.py) 로 변환하여 CMD창에서 바로 실행할 수 있는 프로그램으로 만들 수 있습니다.

CMD 창에서 쥬피터 노트북 파일 경로로 이동한 뒤, 아래의 명령어를 입력합시다.

```
jupyter nbconvert [쥬피터 노트북 파일명] --to script
```
![파이썬](https://user-images.githubusercontent.com/77887166/131311868-dcba98a3-46b1-4438-922c-9942f40bcad7.PNG)

파이썬 파일로 변환한 뒤에는 바로 실행할 수 있는 프로그램(.exe) 가 같은 폴더에 만들어집니다!


Copyright (C) 2021 Bae-SeungHo all rights reserved.
