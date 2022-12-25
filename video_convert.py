import base64
import cv2
import requests
from tqdm import tqdm
import numpy as np

if __name__ == '__main__':
    cap = cv2.VideoCapture('op.mp4')
    frames_num = cap.get(7)
    fps = cap.get(5)
    width = cap.get(3)
    height = cap.get(4)
    print(frames_num, fps, width, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('res.mp4', fourcc, fps, (int(width)*4, int(height)*4))
    cnt = 0
    for i in tqdm(range(0, int(frames_num))):
        ret, frame = cap.read()
        data = cv2.imencode('.jpg', frame)[1].tobytes()
        res = requests.post("http://192.168.1.10:8209/esr/img/row", {
            "data": base64.encodebytes(data).decode(),
            "face_enhance": "false"
        })
        tmp = cv2.imdecode(np.frombuffer(res.content, np.uint8), cv2.IMREAD_UNCHANGED)
        cv2.imwrite("jpg/res_{}.jpg".format(i), tmp)
        out.write(tmp)
    cap.release()
    out.release()
