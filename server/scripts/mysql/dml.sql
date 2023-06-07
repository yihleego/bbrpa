insert into task(id, name, remark, deleted, created_time, updated_time)
values (id, 'get_icons', 'test', 0, now(), now());

insert task_record(task_id, data, result, message, status, deleted, created_time, updated_time)
values (1, '{"keyword":"草莓"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"葡萄"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"苹果"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"西瓜"}', null, null, 0, 0, now(), now());
