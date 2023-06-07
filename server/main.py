# -*- coding=utf-8
import datetime
import logging
import os
import sys

import redis
import waitress
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import Task, TaskRecord, TaskRecordStatus

app = Flask(__name__)
engine = create_engine(config.database.url)
Session = sessionmaker(bind=engine)
rd = redis.Redis(host=config.redis.host, port=config.redis.port, password=config.redis.password, db=0)


@app.post("/tasks/records")
def create_task_record():
    body = request.json
    task_id = body["task_id"]
    data = body["data"]

    session = Session()
    try:
        r = TaskRecord()
        r.task_id = task_id
        r.data = data
        r.status = TaskRecordStatus.CREATED
        r.created_time = datetime.datetime.now()
        session.add(r)
        session.commit()
        return {
            "id": r.id,
        }
    finally:
        session.close()


@app.patch("/tasks/records")
def update_task_record():
    body = request.json
    id = body["id"]
    success = body["success"]
    result = body.get("result")  # nullable
    message = body.get("message")  # nullable

    session = Session()
    try:
        r = session.query(TaskRecord) \
            .filter(TaskRecord.id == id) \
            .first()
        if r is None:
            return "No record", 404  # not found

        r.result = result
        r.message = message
        if success:
            r.status = TaskRecordStatus.COMPLETED
        else:
            r.status = TaskRecordStatus.FAILED

        session.commit()

        # clean task record status
        rd.delete(f'rpa_task:{str(r.id)}')

        return {
            "id": r.id,
            "status": r.status,
        }
    finally:
        session.close()


@app.get("/tasks/records")
def get_executable_tasks():
    session = Session()
    try:
        # find a specified number of CREATED tasks
        records = session.query(TaskRecord) \
            .filter(TaskRecord.deleted == 0) \
            .filter(TaskRecord.status == TaskRecordStatus.CREATED) \
            .order_by(TaskRecord.created_time.asc()) \
            .limit(2).all()
        if len(records) == 0:
            return []

        # guarantee that the tasks can only be processed by one single client
        for r in records:
            if rd.setnx(f'rpa_task:{str(r.id)}', TaskRecordStatus.RUNNING):
                rd.pexpire(f'rpa_task:{str(r.id)}', 10 * 60 * 1000)
                r.status = TaskRecordStatus.RUNNING

        session.commit()

        tasks = session.query(Task) \
            .filter(Task.id.in_([r.task_id for r in records])) \
            .all()

        task_map = {t.id: t.name for t in tasks}

        return [{
            "id": r.id,
            "task_id": r.task_id,
            "task_name": task_map.get(r.task_id),
            "data": r.data,
        } for r in records if r.status == TaskRecordStatus.RUNNING]
    finally:
        session.close()


@app.after_request
def after_request(res):
    req = request
    logging.info("[%s] ---> %s %s %s %s", req.endpoint, req.method, req.full_path, req.remote_addr, req.data if len(req.data) > 0 else "")
    if req.endpoint in ["list_motions", "list_retargets"]:
        logging.info("[%s] <--- %s (%d-byte body)", req.endpoint, res.status, res.content_length)
    else:
        logging.info("[%s] <--- %s (%d-byte body) %s", req.endpoint, res.status, res.content_length, res.data if len(res.data) > 0 else "")
    # CORS
    h = res.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "*"
    h["Access-Control-Allow-Methods"] = "*"
    return res


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    logging.exception(e)
    return str(e), 500


def init():
    formatter = logging.Formatter(config.logging.format)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(config.logging.level)
    logger.addHandler(stream_handler)
    if config.logging.filename:
        os.makedirs(os.path.dirname(config.logging.filename), exist_ok=True)
        file_handler = logging.FileHandler(config.logging.filename, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


if __name__ == "__main__":
    init()
    waitress.serve(app, host="0.0.0.0", port=11111)
