import base64

import requests
from flask import Flask, request, Response, render_template
import json
from web.code import convert_img, convert_img_row

# 初始化flaskAPP
app = Flask(__name__)


# 返回JSON字符串
def return_json(data):
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')


# 音色转换
@app.route('/esr/img', methods=['POST'])
def convert_img1():
    face_enhance = request.form.get('face_enhance')
    data = request.form.get('data')
    # 保存图片文件
    path = "./web/static"
    img_name = "origin.jpg"
    data = data.replace("data:image/jpeg;base64,", "")
    with open("{}/{}".format(path, img_name), "wb") as f:
        f.write(base64.b64decode(data))
    convert_img(path, img_name, face_enhance == 'true')
    return return_json({
        'origin': '/static/origin.jpg',
        'convert': '/static/scale_res.jpg'
    })


# 音色转换
@app.route('/esr/img/row', methods=['POST'])
def convert_img2():
    face_enhance = request.form.get('face_enhance')
    print(type(face_enhance))
    data = request.form.get('data')
    if data and data != "":
        data = data.replace("data:image/jpeg;base64,", "")
        file_data = base64.b64decode(data)
    else:
        file_data = request.files['file'].read()

    res = convert_img_row(file_data, face_enhance == 'true')
    return Response(res, mimetype="image/jpeg")


@app.route('/esr/img/url', methods=['GET'])
def convert_img3():
    file_data = requests.get(request.args.get("u")).content
    res = convert_img_row(file_data, True)
    return Response(res, mimetype="image/jpeg")


# 主页显示HTML
@app.route('/', methods=['GET'])
def index():
    return render_template('content.html')
