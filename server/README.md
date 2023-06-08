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

任务由 2 张表组成，`task`和`task_script`：

- `task`：仅用于展示，记录当前版本号。
- `task_script`：一个任务可能存在多个版本的脚本，客户端执行前对比本地脚本版本和数据库的版本，如果不一致需要先更新脚本。

```sql
create table task
(
    id           bigint auto_increment primary key,
    name         varchar(64)      null comment '名称 仅用于展示',
    remark       varchar(64)      null comment '备注 仅用于展示',
    version      int    default 0 not null comment '版本号 0:表示无脚本',
    deleted      bigint default 0 not null comment '删除标识 0:未删除 {id}:已删除',
    created_time timestamp        null,
    updated_time timestamp        null
);
create index idx_task_name on task (name);

create table task_script
(
    id           bigint auto_increment primary key,
    task_id      bigint             not null,
    script       text               null comment '脚本代码 用于执行',
    params       json               null comment '参数结构 用于校验',
    version      int      default 0 not null comment '版本号 从1开始',
    status       smallint default 0 not null comment '状态 0:禁用 1:启用',
    deleted      bigint   default 0 not null comment '删除标识 0:未删除 {id}:已删除',
    created_time timestamp          null,
    updated_time timestamp          null
);
create index idx_task_script_task_id on task_script (task_id);
```

任务示例：

```sql
# 增加一条测试任务
insert into task(id, name, remark, version, deleted, created_time, updated_time)
values (1, '获取图标', '测试', 1, 0, now(), now());
# 新增一条测试任务脚本
insert into task_script(id, task_id, script, params, version, status, deleted, created_time, updated_time)
values (1, 1, '<脚本具体见下方>', '[{"key":"keyword","value":"","type":"String","required":true}]', 1, 1, 0, now(), now());
```

脚本示例：

```python
"""
客户端运行脚本时会自动注入以下本地变量：
driver: WebDriver 自动注入 Headless 浏览器
params: any 自动注入参数
result: any 如果有返回值需要赋值该本地变量
success: bool 如果失败需要赋值该本地变量为 False，默认为 True
"""

import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# 直接使用 params 本地变量，获取参数
keyword = params["keyword"]

# 直接使用 driver 本地变量，本示例是从 iconfont 获取关键字对应的图标
driver.get('https://www.iconfont.cn/')
time.sleep(0.5)

# 点击按钮
driver.find_element(by=By.CSS_SELECTOR, value='#J_search-box > div:nth-child(1)').click()
# 默认是图标，这里选择插图
driver.find_element(by=By.CSS_SELECTOR, value='div[data-type=illustration]').click()
# 输入关键字
driver.find_element(by=By.CSS_SELECTOR, value='input#J_search_input_index').send_keys(keyword + Keys.ENTER)
time.sleep(0.5)

# 从页面中找到图标名称和链接
icon_names = driver.find_elements(by=By.CSS_SELECTOR, value='.block-icon-list>li>.icon-name')
icon_images = driver.find_elements(by=By.CSS_SELECTOR, value='.block-icon-list>li>.icon-twrap>img')

# 返回 result
result = []
for i in range(len(icon_images)):
    result.append({
        "name": icon_names[i].get_property("title"),
        "image": icon_images[i].get_property("src"),
    })

# 返回 success
success = True
```

需要注意的是，Python 程序中，缩进非常重要的一部分，通常表示上下代码的所属关系，如果不规范程序就不能运行，甚至造成恶性Bug。

### 新建任务记录

示例中创建了 4 个任务记录：

```sql
insert task_record(task_id, params, result, message, status, deleted, created_time, updated_time)
values (1, '{"keyword":"草莓"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"葡萄"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"苹果"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"西瓜"}', null, null, 0, 0, now(), now());
```