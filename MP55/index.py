from flask import Flask, render_template, Response, request, redirect
import cv2
import pyautogui
import time
from cvzone.HandTrackingModule import HandDetector

app = Flask(__name__, template_folder='template')

detector = HandDetector(maxHands=1, detectionCon=0.8)
cam = cv2.VideoCapture(0)

output = ""  # Initialize the output variable to store the count string

def gen():
    global output
    fingerup = None  # Initialize fingerup variable
    prev_index_pos = None  # Initialize previous index finger position
    while True:
        success, frame = cam.read()
        if not success:
            print("Failed to capture frame from camera. Check camera connection.")
            continue
        hands, frame = detector.findHands(frame)  # Set draw to True to draw the hand landmarks
        text_to_display = "Try Again" 
        
        if hands:
            hand = hands[0]
            lmList = hand["lmList"]  # List of 21 Landmark points
            bbox = hand["bbox"]  # Bounding box info x,y,w,h
            centerPoint = hand["center"]  # Center of the hand cx,cy
            handType = hand["type"]  # Handtype Left or Right
            fingerup = detector.fingersUp(hand)
            
            # Your conditions for fingerup...
            if fingerup == [0, 0, 0, 0, 0]:
                text_to_display = "10"
            elif fingerup == [0, 1, 0, 0, 0]:
                text_to_display = "1"
            elif fingerup == [0, 1, 1, 0, 0]:
                text_to_display = "2"
            elif fingerup == [0, 1, 1, 1, 0]:
                text_to_display = "3"
            elif fingerup == [0, 1, 1, 1, 1]:
                text_to_display = "4"
            elif fingerup == [1, 1, 1, 1, 1]:
                text_to_display = "5"
            elif fingerup == [1, 0, 0, 0, 0]:
                text_to_display = "6"
            elif fingerup == [1, 1, 0, 0, 0]:
                text_to_display = "7"
            elif fingerup == [1, 1, 1, 0, 0]:
                text_to_display = "8"
            elif fingerup == [1, 1, 1, 1, 0]:
                text_to_display = "9"
            else:
                text_to_display = "Try Again"  # Display message when no gesture is detected
                
            if lmList:  # Check if hand landmarks are detected
                index_pos = lmList[8]  # Index finger tip position
                thumb_pos = lmList[4]  # Thumb tip position
                
                # Calculate the movement of the index finger
                if prev_index_pos is not None:
                    dx = index_pos[0] - prev_index_pos[0]
                    dy = index_pos[1] - prev_index_pos[1]
                    pyautogui.move(dx, dy)  # Move the cursor
                    
                prev_index_pos = index_pos
                
                if fingerup == [0, 1, 1, 0, 1]:  
                    pyautogui.scroll(100)  # Scroll up
                elif fingerup == [0, 1, 0, 0, 1]:  
                    pyautogui.scroll(-100)  # Scroll down
                
                elif fingerup == [0, 0, 1, 1, 1]:
                    pyautogui.click()  # Perform a click

                elif fingerup == [0, 0, 0 ,0 ,1]:
                    pyautogui.move(100,0)

                elif fingerup == [1, 0, 0 ,0 ,1]:
                    pyautogui.move(-100,0)

                elif fingerup == [1, 1, 0 ,0 ,1]:
                    pyautogui.move(0,100)

        output = text_to_display  # Update the output with the latest count or message
        
        # Encode the frame and yield it for streaming
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html", output=output)

@app.route('/video')
def video():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    global output
    # Capture the current output value
    captured_output = output
    return captured_output  # Return just the output data

@app.route('/reset', methods=['POST'])
def reset():
    global output
    # Clear the output variable
    output = ""
    return output  # Return the cleared output data

@app.route('/redirect', methods=['POST'])
def redirect_to_playlist():
    output_value = request.form['output_value']
    if output_value == "1":
        return redirect('/playlist1.html')
    elif output_value == "2":
        return redirect('/playlist2.html')
    elif output_value == "3":
        return redirect('/playlist3.html')
    elif output_value == "4":
        return redirect('/playlist4.html')
    elif output_value == "5":
        return redirect('/playlist5.html')
    elif output_value == "6":
        return redirect('/playlist6.html')
    elif output_value == "7":
        return redirect('/playlist7.html')
    elif output_value == "8":
        return redirect('/playlist8.html')
    elif output_value == "9":
        return redirect('/playlist9.html')
    elif output_value == "10":
        return redirect('/playlist10.html')
    else:
        return "Please Capture a Valid Gesture to Discover Music"
    
@app.route('/playlist1.html')
def playlist1():
    return render_template('playlist1.html')

@app.route('/playlist2.html')
def playlist2():
    return render_template('playlist2.html')

@app.route('/playlist3.html')
def playlist3():
    return render_template('playlist3.html')

@app.route('/playlist4.html')
def playlist4():
    return render_template('playlist4.html')

@app.route('/playlist5.html')
def playlist5():
    return render_template('playlist5.html')

@app.route('/playlist6.html')
def playlist6():
    return render_template('playlist6.html')

@app.route('/playlist7.html')
def playlist7():
    return render_template('playlist7.html')

@app.route('/playlist8.html')
def playlist8():
    return render_template('playlist8.html')

@app.route('/playlist9.html')
def playlist9():
    return render_template('playlist9.html')

@app.route('/playlist10.html')
def playlist10():
    return render_template('playlist10.html')

if __name__ == "__main__":
    app.run()
