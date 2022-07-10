import pyautogui 
import cv2 as cv2
import numpy as np 
from pathvalidate import is_valid_filename
from plyer import notification

resolution = (1920, 1080) 
filename="fi:l*e/p\"a?t>h|.t<xt" 
end='start' 
used=[]
codec = cv2.VideoWriter_fourcc(*"XVID") 
while(end!='end'):
    while is_valid_filename(filename)!=True or filename in used:
        filename = input("Enter File Name to save recording:")+".avi"
        if is_valid_filename(filename)!=True:
            print("\nInvalid File Name. Try again")
        elif filename in used:
            print("\nFile Name already exists.Enter new file name")
    if is_valid_filename(filename) :
        print("Recording Started.\n")
        used.append(filename)
        notification.notify(
            title='Screen-Recorder',
            message='Recording started. Press Q to stop recording.',
            app_icon=None, 
            timeout=2, 
        )

        # vary FPS as per need or if any video speed related issues are observed.
        fps = 20.0

        out = cv2.VideoWriter(filename, codec, fps, resolution) 
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("Live", 480, 270) 
        
        while True: 
            img = pyautogui.screenshot() 
            frame = np.array(img) 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            out.write(frame) 
            cv2.imshow('Live', frame)   
            if cv2.waitKey(1) == ord('q'): 
                break
        out.release() 
        cv2.destroyAllWindows()
        end=input("Recording Stopped. Press enter to start new recording. Type 'end' to quit.\n").lower()
