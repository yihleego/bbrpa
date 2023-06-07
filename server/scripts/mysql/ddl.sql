create database rpa;
use rpa;

create table task
(
    id           bigint auto_increment primary key,
    name         varchar(64)       null,
    remark       varchar(64)       null,
    deleted      tinyint default 0 not null,
    created_time timestamp         null,
    updated_time timestamp         null
);
create index idx_task_name on task (name);

create table task_record
(
    id           bigint auto_increment primary key,
    task_id      bigint             not null,
    data         text               null,
    result       text               null,
    message      text               null,
    status       smallint default 0 not null,
    deleted      tinyint  default 0 not null,
    created_time timestamp          null,
    updated_time timestamp          null
);
create index idx_task_record_task_id on task_record (task_id);