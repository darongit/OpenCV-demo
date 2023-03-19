import contextlib, os, glob, string, random
from threading import Thread
from datetime import datetime
import cv2
import numpy as np

def savePhoto(photo, dir_name = 'cameraresults'):
    with contextlib.suppress(FileExistsError):
        os.mkdir(dir_name)
    photos = glob.glob(f'{dir_name}\\*.png')
    count_photos=0
    for phot in photos:
        if ''.join([letter.lower() for letter in phot.rsplit('.', 1)[0].split('\\')[-1].strip().lower() if letter in string.ascii_letters]) == 'photo':
            count_photos+=1
    now = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = os.path.join(os.getcwd(), f'{dir_name}\\{now}_photo{count_photos}.png')
    try:
        cv2.imwrite(filename, photo)
    except Exception as e:
        print(filename)
        print(photo)
cap = cv2.VideoCapture(0)
rotate = 1
mirrors = 1
color_frame = 0
front_mirror = 1
while True:
    isTrue, frame = cap.read()
    if not isTrue:
        break
    frame = cv2.resize(frame, (0,0), fx=1.4, fy=1.4)
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    if rotate%2==0:
        small_frame = cv2.rotate(small_frame, cv2.ROTATE_180)
    if mirrors%2==0:
        for i in range(1, small_frame.shape[0]):
            small_frame[i] = small_frame[i][::-1]
            canny_frame[i] = canny_frame[i][::-1]
    gray_frame = cv2.cvtColor(cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    hsv_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)
    canny_frame = cv2.cvtColor(cv2.Canny(small_frame, 90, 75), cv2.COLOR_GRAY2BGR)
    if front_mirror%2==0:
        for i in range(1, small_frame.shape[0]):
            gray_frame[i] = gray_frame[i][::-1]
            hsv_frame[i] = hsv_frame[i][::-1]
    blank = np.zeros(frame.shape, dtype='uint8')
    blank[:small_frame.shape[0], :small_frame.shape[1]] = small_frame
    blank[:small_frame.shape[0], small_frame.shape[1]:] = hsv_frame
    blank[small_frame.shape[0]:, :small_frame.shape[1]] = canny_frame
    blank[small_frame.shape[0]:, small_frame.shape[1]:] = gray_frame
    if color_frame%2==0:
        color = (0, 0, 0)
    else:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    cv2.line(blank, (0, blank.shape[0]//2), (blank.shape[1], blank.shape[0]//2), color, 10)
    cv2.line(blank, (blank.shape[1]//2, 0), (blank.shape[1]//2, blank.shape[0]), color, 10)
    cv2.line(blank, (5, 0), (5, blank.shape[0]), color, 10)
    cv2.line(blank, (blank.shape[1]-5, 0), (blank.shape[1]-5, blank.shape[0]), color, 10)
    cv2.line(blank, (0,5), (blank.shape[1], 5), color, 10)
    cv2.line(blank, (0, blank.shape[0]-5), (blank.shape[1]-5, blank.shape[0]-5), color, 10)
    main_frame = np.zeros((blank.shape[0]+100, blank.shape[1], blank.shape[2]), dtype='uint8')
    main_frame[:blank.shape[0], :] = blank
    text= cv2.putText(main_frame, 'Press: "q" : quit, "s" : save photo, "r" : rotate, "t" : mirror reflection,', (25 ,main_frame.shape[0]-50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255,255,255), 1, cv2.LINE_AA)
    text= cv2.putText(main_frame, '"c" : frame style, "f" : frontline mirror', (25 ,main_frame.shape[0]-25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255,255,255), 1, cv2.LINE_AA)
    cv2.imshow('CV2', main_frame)
    wait = cv2.waitKey(1)
    if wait == ord('s'):
        Thread(target = savePhoto, args=(blank, 'myphotos')).start()
    elif wait == ord('r'):
        rotate+=1
    elif wait == ord('t'):
        mirrors+=1
    elif wait == ord('c'):
        color_frame+=1
    elif wait == ord('f'):
        front_mirror+=1
    elif wait == ord('q'):
        break
    if rotate == 20:
        rotate = 2
    if mirrors == 20:
        mirrors = 2
    if color_frame ==20:
        color_frame = 2

cv2.destroyAllWindows()
