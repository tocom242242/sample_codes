# find_person_and_cat/main.py

import cv2
from darkflow.net.build import TFNet

# darkflowの設定
options = {"model": "./cfg/yolo.cfg",
           "load": "./weights/yolo.weights",
           "threshold": 0.1}

# darkflowの生成
tfnet = TFNet(options)

# カメラの起動
cap = cv2.VideoCapture(0)

class_names = ["cat", "person"]


def clip_img(img, result, img_path):
    """
        画像を切り抜く
    """
    x = result['topleft']['x']
    y = result['topleft']['y']
    brx = result['bottomright']['x']
    bry = result['bottomright']['y']
    h = abs(y-bry)
    w = abs(x-brx)

    clipped = img[y:y+h, x:x+w]
    cv2.imwrite(img_path, clipped)

    return clipped


def main():
    while(True):
        ret, img = cap.read()
        results = tfnet.return_predict(img)

        # 元画像の保存
        img_path = './img.jpg'
        # img_path = './{}.jpg'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        cv2.imshow("img", img)
        cv2.imwrite(img_path, img)
        for result in results:
            label = result['label']
            confidence = result['confidence']

            # 猫や人が含まれていて、確信度は0.6以上であれば切り抜く
            if label in class_names and confidence > 0.6:
                clipped_img_path = './img_clipped.jpg'
                # clipped_img_path = './{}_clipped.jpg'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
                # 画像をクリップする
                clip_img(img, result, clipped_img_path)
                print("cliped")

        # qを押したら終了する
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
