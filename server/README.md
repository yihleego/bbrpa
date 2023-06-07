# RPA Server

## 安装

### Python

请确保 Python 版本 3.8 及以上

### 依赖

```
Flask==2.2.3
waitress==2.1.2
SQLAlchemy==2.0.9
PyMySQL==1.0.3
redis==4.5.5
PyYAML==6.0
```

```shell
pip install -r requirements.txt
```

### MySQL

执行以下脚本：

- [ddl.sql](scripts/mysql/ddl.sql)
- [dml.sql](scripts/mysql/dml.sql)

修改配置文件：

[config-dev.yml](config-dev.yml)

```yaml
database:
  url: mysql+pymysql://username:password@localhost:3306/rpa
```

### Redis

修改配置文件：

[config-dev.yml](config-dev.yml)

```yaml
redis:
  host: localhost
  port: 6379
  password: password
```

## 运行

```shell
python main.py --env=dev
```

## 任务

### 新建任务

```sql
insert into task(id, name, remark, deleted, created_time, updated_time)
values (id, 'get_icons', 'test', 0, now(), now());
```

`name`对应`client/app.py`中的方法名，后续考虑设计一个`task_script`表，通过脚本解释器执行任务，而不是硬编码。

### 为用户新建任务记录

```sql
insert task_record(task_id, data, result, message, status, deleted, created_time, updated_time)
values (1, '{"keyword":"草莓"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"葡萄"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"苹果"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"西瓜"}', null, null, 0, 0, now(), now());
```