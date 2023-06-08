create database rpa;
use rpa;

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


create table task_record
(
    id           bigint auto_increment primary key,
    task_id      bigint             not null,
    params       json               null comment '参数内容',
    result       json               null comment '任务执行结果报文',
    message      text               null comment '任务执行结果信息',
    status       smallint default 0 not null comment '任务状态 0:创建 1:运行中 2:失败 100:成功',
    deleted      bigint   default 0 not null comment '删除标识 0:未删除 {id}:已删除',
    created_time timestamp          null,
    updated_time timestamp          null
);
create index idx_task_record_task_id on task_record (task_id);