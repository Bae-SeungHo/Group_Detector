#!/usr/bin/env python
# coding: utf-8

# ![science](http://kiap.or.kr/inc/user/resource/image/sub/img_calendar01_0625.png)

# * ## 라이브러리 로드

# In[43]:


import numpy as np
import cvlib as cv
import matplotlib.pyplot as plt
import cv2


# * ##  5인 이상 그룹 탐지 클래스

# In[49]:


class Group_Check_App:
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
    
    def Detector(self,PATH):
        if self.isVideo: #동영상 탐지
            print('press q to quit')
            while self.cam.isOpened(): #동영상 프레임이 남은동안 반복
                persons = []
                status, frame = self.cam.read()
                cv2.imshow('frame',frame)
                rect,obj,conf = cv.detect_common_objects(frame) # 영상 속 개체 탐지
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
                
        else: # 이미지 탐지
            persons = []
            self.frame = cv2.resize(self.frame,(640,480),interpolation=cv2.INTER_AREA)
            cv2.imshow('frame',self.frame)
            rect,obj,conf = cv.detect_common_objects(self.frame)
            _ = [persons.append(rect[i]) for i in range(len(rect)) if obj[i] == 'person' and conf[i] >= 0.6]

            for person in persons:
                    l,t,r,b = person #좌표 로드
                    if len(persons) >= 5: # person above 5
                        cv2.rectangle(self.frame,(l,t),(r,b),(0,0,255),3) #초록색 네모로 사람의 Bounding Box 그림
                    else: # person under 5    
                        cv2.rectangle(self.frame,(l,t),(r,b),(0,255,0),3) #빨간색 네모로 사람의 Bounding Box 그림
                        
            cv2.putText(self.frame,'Person Counts : {}'.format(str(len(persons))),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
            cv2.imshow('after_frame',self.frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
            cv2.imwrite('%s_result.jpg' % (PATH.split('.')[:-1][0]),self.frame)   


# * ##  활용

# In[50]:


print('\nInput File Path (input cam to use Webcam)')
PATH = input()
Group_Check_App(PATH)

