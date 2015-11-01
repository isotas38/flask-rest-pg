from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/postgres'
api = Api(app)
db = SQLAlchemy(app)

teacher_fields = {
    'id': fields.Integer,
    'img_path': fields.String,
    'tag': fields.String,
}

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    img_path = db.Column(db.String(80), unique=True)
    tag = db.Column(db.String(120))

    def __init__(self, img_path, tag):
        self.img_path = img_path
        self.tag = tag

    def __repr__(self):
        return '<User %r>' % self.img_path

class TeacherResource(Resource):
    @marshal_with(teacher_fields)
    def get(self):
        teachers = Teacher.query.all()
        return teachers

    def post(self):
        teacher = Teacher(**request.get_json(force=True))
        db.session.add(teacher)
        db.session.commit()
        return "ok"

api.add_resource(TeacherResource, '/teachers')

if __name__ == '__main__':
     app.run(host='0.0.0.0')
