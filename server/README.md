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