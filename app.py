from flask import *
from flask_cors import CORS
from PIL import Image
import MachineLearningModel
app = Flask(__name__)
CORS(app)

@app.route("/",methods=['POST','GET'])
def calculate():
    img = request.files['image']
    img = Image.open(img)
    resEye,resYarn = MachineLearningModel.find(img)
    returner ={}
    returner['result'] = int(resEye)*0.3+int(resYarn)*0.7 if(resEye!=-1) else resYarn
    return returner

app.run(host='0.0.0.0',debug=True)