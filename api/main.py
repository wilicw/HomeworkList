import json
from flask import Flask, request, jsonify, render_template
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import configparser
config = configparser.ConfigParser()
config.read('.config')

app = Flask(__name__, static_folder = "../dist/static", template_folder = "../dist")
CORS(app)
app.config['MONGODB_SETTINGS'] = {
  'db': "homework",
  'host': "mongodb://{}:{}@{}:{}/homework?authSource={}".format(config['mongo']['user'], config['mongo']['password'], config['mongo']['host'], config['mongo']['port'], config['mongo']['db']),
}
db = MongoEngine()
db.init_app(app)

class tags(db.Document):
  _id = db.IntField()
  name = db.StringField()
  def to_json(self):
    return {"id": self._id,
            "name": self.name}

class subjects(db.Document):
  _id = db.IntField()
  name = db.StringField()
  def to_json(self):
    return {"id": self._id,
            "name": self.name}

class users(db.Document):
  _id = db.IntField()
  username = db.StringField()
  password = db.StringField()

class hw(db.Document):
  _id = db.IntField()
  text = db.StringField()
  subject = db.IntField()
  tag = db.IntField()
  time = db.IntField()
  user = db.IntField()
  def to_json(self):
    return {"id": self._id,
            "text": self.text,
            "tag": self.tag,
            "subject": self.subject,
            "time": self.time}

@app.route('/')
def catch_all():
    return render_template("index.html")

@app.route('/api/tags/', methods=['GET'])
def query_tags():
  items = tags.objects()
  if not items:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify([ tag.to_json() for tag in items ])

@app.route('/api/subjects/', methods=['GET'])
def query_subjects():
  items = subjects.objects()
  if not items:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify([ subject.to_json() for subject in items ])

@app.route('/api/', methods=['GET'])
def query_records():
  now = int(request.args.get('now'))
  lists = hw.objects(time__gte=now)
  if not lists:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify([ hw.to_json() for hw in lists ])

@app.route('/api/', methods=['PUT'])
def create_record():
  data = json.loads(request.data)
  admin = users.objects(
    username=str(data['username']),
    password=str(data['password'])
  ).first()
  if not admin:
    return jsonify({'error': 'who are u?'})
  next_id = [ i._id for i in hw.objects() ]
  next_id = next_id[-1]+1
  item = hw(
    _id=next_id,
    text=data['text'],
    tag=int(data['tag']),
    subject=int(data['subject']),
    time=int(data['time']),
    user=int(admin._id)
  )
  item.save()
  return jsonify(item.to_json())

@app.route('/api/', methods=['POST'])
def update_record():
  data = json.loads(request.data)
  admin = users.objects(
    username=str(data['username']),
    password=str(data['password'])
  ).first()
  if not admin:
    return jsonify({'error': 'who are u?'})
  item = hw.objects(_id=data['id']).update(
    text=data['text'],
    tag=int(data['tag']),
    subject=int(data['subject']),
    time=int(data['time'])
  )
  return jsonify({})

@app.route('/api/', methods=['DELETE'])
def delete_record():
  data = json.loads(request.data)
  admin = users.objects(
    username=str(data['username']),
    password=str(data['password'])
  ).first()
  if not admin:
    return jsonify({'error': 'who are u?'})
  item = hw.objects(_id=data['id'])
  if not item:
    return jsonify({'error': 'data not found'})
  else:
    item.delete()
  return jsonify({})

if __name__ == "__main__":
  app.run(host='0.0.0.0')