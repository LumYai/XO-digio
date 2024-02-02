from flask import Flask, render_template, jsonify, request
import pymongo
from pymongo import MongoClient




app = Flask(__name__)


#Database
client = MongoClient(host='test_mongodb',
                        port=27017, 
                        username='root', 
                        password='pass',
                        authSource="admin")
db = client["test_db"]

@app.route('/')
def index():
    # Retrieve data from MongoDB (you can modify this part according to your needs)
    data = db.mycollection.find()
    return render_template('index.html', data=data)

#  ----------API เก็บข้อมูลลง Database--------------

# สร้าง Sequence Collection ถ้ายังไม่มี
if 'sequence' not in db.list_collection_names():
    db.create_collection('sequence')
    db.sequence.insert_one({'_id': 'play_round', 'sequence_value': 1})
#  เก็บประวัติการเล่นบน database

@app.route('/api/play_round', methods=['POST'])
def play_round():
    # รับข้อมูลที่ส่งมาจากแอพพลิเคชัน (รหัสวิชา)
    data = request.json

    id_r = db.sequence.find_one_and_update(
        {'_id': 'play_round'},
        {'$inc': {'sequence_value': 1}},
        return_document=True
    )['sequence_value']


    list_x = data.get('list_x')
    list_o = data.get('list_o')
    size = data.get('size')

    filter_condition = {'_id': id_r}

    # ตรวจสอบว่าข้อมูลถูกส่งมาหรือไม่
    if not list_x or not list_o :
        return jsonify({'message': 'ข้อมูลไม่ครบถ้วน'}), 400

    # กำหนดเงื่อนไขในการค้นหาเอกสารที่มี '_id' เท่ากับ '030'
    # filter_condition = {'_id': '030'}

    # กำหนดข้อมูลที่จะใช้ในการอัปเดตหรือสร้างเอกสารใหม่
    update_data = {
        '_id': id_r,  # ระบุ '_id' เพื่อหาเอกสารที่มีหรือสร้างใหม่
        'list_x': list_x,
        'list_o': list_o,
        'size': size
    }

    # ใช้คำสั่ง update_one เพื่ออัปเดตหรือสร้างเอกสารใน MongoDB
    db.play_round.update_one(filter_condition, {'$set': update_data}, upsert=True)

    return jsonify({'message': 'บันทึกข้อมูลสำเร็จ'}), 200


#  ส่งค่าผลการเล่นให้แสดงบนหน้า
@app.route('/api/play_round_display', methods=['GET'])
def display_play_round():
    # ดึงข้อมูลจาก MongoDB
    data = list(db.play_round.find({}))

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)