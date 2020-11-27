from app import db
from .base import Base


class Student(Base):
    __tablename__='student'
    
    
    student_name    = db.Column(db.String(128),  nullable=False)
    student_marks    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
 
    



               