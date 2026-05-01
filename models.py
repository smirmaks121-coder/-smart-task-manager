from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, default="Дом")
    due_date = Column(Date, default=datetime.date.today) # Новое поле
    is_completed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
