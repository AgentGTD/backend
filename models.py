from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer)  # ID of the parent goal or None

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer)     # ID of the goal this task belongs to
    description = Column(String)
    completed_at = Column(DateTime)  # Timestamp when task was completed
    is_completed = Column(Boolean)
