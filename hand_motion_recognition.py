import tensorflow.keras
import numpy as np
import cv2

# 모델 위치
model_filename = 'C:\\Users\\user\\PycharmProjects\\pythonProject6\\keras_model_3.h5'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)

# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 620)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 620)


# 이미지 처리하기
def preprocessing(frame):
    # frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

    # 이미지 정규화
    # astype : 속성
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    # print(frame_reshaped)
    return frame_reshaped


# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    print(prediction)
    return prediction


while True:
    ret, frame = capture.read()

    if cv2.waitKey(100) > 0:
        break
    frame2 = cv2.flip(frame,1)
    preprocessed = preprocessing(frame2)
    prediction = predict(preprocessed)

    if prediction[0][0] == max(prediction[0]) :
        print('1')
        cv2.putText(frame2, '1', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))

    elif prediction[0][1] == max(prediction[0]):
        cv2.putText(frame2, '2', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        print('2')

    #elif prediction[0][2] == max(prediction[0]):
    #    cv2.putText(frame2, '3', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    #    print('3')

    elif prediction[0][2] == max(prediction[0]):
        cv2.putText(frame2, 'YES', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        print('YES')

    elif prediction[0][3] == max(prediction[0]):
        cv2.putText(frame2, 'Swipe Left', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        print('Swipe Left')

    elif prediction[0][4] == max(prediction[0]):
        cv2.putText(frame2, 'Swipe Right', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        print('Swipe Right')

    elif prediction[0][5] == max(prediction[0]):
        cv2.putText(frame2, 'X', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        print('X')

    elif prediction[0][6] == max(prediction[0]):
        cv2.putText(frame2, '3', (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        print('3')

    cv2.imshow("VideoFrame", frame2)