from flask import Flask, render_template ,jsonify , request

from modules.ImageToText.imageText import readText
import threading , time , cv2 , requests , os , json

#   External Modules ...
from modules.DialogFlowConnect import botResponseReciever
from modules.FriendRecognition.face_recog import FaceRecog
from modules.Actual.CurrencyDetection.predict import *

face = FaceRecog()

app = Flask(__name__)

# Variables declaration...

buffer = "currency"
data_buffer = ""
special_buffer = ""
stop_threads = False
webcam_thread = None

def webcamCap(stop):
    global buffer
    global data_buffer
    global special_buffer
    cap = cv2.VideoCapture("http://192.168.43.216:4747/mjpegfeed")
    counter = 0
    while(True):
        ret , frame = cap.read()
        #   RGB -> Grey Conversion (Optional)
        try:
            frame = frame[50: , 50:]
        except:
            pass

        if buffer == "Face" and counter > 20:
            counter = 0
            name = face.render_frame(frame)
            if(name != "No faces"):
                name = name.split(" ")[0]
                data_buffer = name
                buffer = "Nothing"
        elif buffer == "currency":
            cv2.imwrite("./modules/Actual/CurrencyDetection/sample.jpg" , frame)
            print("predict")
            predictCurrency()
            #buffer = "Nothing"
        
        counter = counter + 1
        
        cv2.imshow('Live Camera Feed' , frame)
        
        if stop():
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def bot_event_handler(bot_response , intent_class):
    if intent_class == "launch":
        return requests.post('http://192.168.43.218:5000/start')
    elif intent_class == "Sleep":
        return requests.post('http://192.168.43.218:5000/stop')
    elif intent_class == "currency":
        return requests.post('http://192.168.43.218:5000/currency')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/botResponse' , methods = ['POST' , 'GET'])
def botResponse():
    botMessage = botResponseReciever(request.form["utext"])
    bot_event_handler(botMessage[0] , botMessage[1])    
    return  jsonify({'response': botMessage[0] , 'class' : botMessage[1]})

@app.route('/start' , methods = ['POST' , 'GET'])
def startRender():
    global stop_threads
    global buffer
    global data_buffer
    global webcam_thread
    if not stop_threads:
        webcam_thread = threading.Thread(target = webcamCap, args =(lambda : stop_threads, )) 
        webcam_thread.start()
        while(buffer == "Face"):
            continue
        print("comes out of face !{}".format(data_buffer))
        return jsonify({ 'flag' : False, 'message': "Your friend "+data_buffer +" is nearby"})
    print('[STATUS] Thread running...')
    return jsonify({'flag': True})

@app.route('/stop' , methods = ['POST' , 'GET'])
def stopRender():
    global stop_threads
    stop_threads = True
    time.sleep(0.3)
    stop_threads = False
    print('[STATUS] Thread stops...')
    return jsonify({'flag' : True})

@app.route('/currency' , methods = ['POST' , 'GET'])
def predictCurrency():
    global buffer
    buffer = "currency"
    return "Hello"


if __name__ == "__main__":
    app.run(debug = True , host= "0.0.0.0")