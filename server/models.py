# -*- coding=utf-8
from sqlalchemy import String, Column, Integer, JSON, TIMESTAMP, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    remark = Column(String(64))
    version = Column(Integer)
    deleted = Column(Integer)
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class TaskScript(Base):
    __tablename__ = "task_script"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer)
    script = Column(Text)
    params = Column(JSON)
    version = Column(Integer)
    status = Column(Integer)
    deleted = Column(Integer)
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class TaskRecord(Base):
    __tablename__ = "task_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer)
    params = Column(JSON)
    result = Column(JSON)
    message = Column(Text)
    status = Column(Integer)
    deleted = Column(Integer)
    created_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)


class TaskScriptStatus:
    DISABLED = 0
    ENABLED = 1


class TaskRecordStatus:
    CREATED = 0
    RUNNING = 1
    FAILED = 2
    COMPLETED = 100
