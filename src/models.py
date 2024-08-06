from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#how to make models and how to do route to modify those models
teacher_subject = db.Table(
    "teacher_subject",
    db.Column("teacher_id", db.ForeignKey("teachers.id")),
    db.Column("subjects_id", db.ForeignKey("subjects.id")),
)
student_cohort = db.Table(
    "student_cohort",
    db.Column("student_id", db.ForeignKey("students.id")),
    db.Column("cohort_id", db.ForeignKey("cohorts.id")),
)

class Teachers(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    experience = db.Column(db.Integer, unique=False, nullable=False)
    subjects = db.relationship("Subjects", secondary= teacher_subject)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Teachers %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "experience": self.experience,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    #not cohort_id or name because then it would only be ONE possible cohort. Cohorts allows MULTIPLE relationships

class Subjects(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    teachers = db.relationship("Teachers", secondary= teacher_subject)

    def __repr__(self):
        return 'Subjects %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
            # do not serialize the password, its a security breach
        }

class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    grade = db.Column(db.Integer, unique=False, nullable=False)
    #favorite_subjects = db.relationship("Subjects", secondary= teacher_subject)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    cohorts = db.relationship("Cohorts", secondary= student_cohort)

    def __repr__(self):
        return '<Students %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "grade": self.grade,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Cohorts(db.Model):
    __tablename__ = "cohorts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable = False)
    teacher = db.relationship('Teachers', backref='cohorts')
    students = db.relationship("Students", secondary= student_cohort)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable = False)
    subject = db.relationship('Subjects', backref='cohorts')
    
#many to many relationship since both the teachers can teach many subjects and there can be many teachers who teach the same subjects

    def __repr__(self):
        return '<Cohorts %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "teacher": self.teacher.serialize(),
            "subject": self.subject.serialize(),
            "student": [student.serialize() for student in self.students]

            # do not serialize the password, its a security breach
        }