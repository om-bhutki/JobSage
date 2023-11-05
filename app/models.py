# contains the database schema and the ORM
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    job_Title = db.Column(db.String(100), nullable=False)
    comp_name = db.Column(db.String(50), nullable=False)
    Job_desc = db.Column(db.String(300), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    linkedin_company_url = db.Column(db.String(255))

    def to_json(self):
        return {
            'job_id': self.job_id,
            'job_Title': self.job_Title,
            'comp_name': self.comp_name,
            'Job_desc': self.Job_desc,
            'salary': self.salary,
            'city': self.city,
            'address': self.address,
            'linkedin_company_url': self.linkedin_company_url
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def to_json(self):
        return {
            'username': self.username,
            'password': self.password
        }
