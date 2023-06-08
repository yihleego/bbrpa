insert into task(id, name, remark, version, deleted, created_time, updated_time)
values (1, '获取图标', '测试', 1, 0, now(), now());

insert into task_script(id, task_id, script, params, version, status, deleted, created_time, updated_time)
values (1, 1, '
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

keyword = params["keyword"]

# open url
driver.get(''https://www.iconfont.cn/'')
time.sleep(0.5)

# toggle the button
driver.find_element(by=By.CSS_SELECTOR, value=''#J_search-box > div:nth-child(1)'').click()
# choose the illustration
driver.find_element(by=By.CSS_SELECTOR, value=''div[data-type=illustration]'').click()
# input the keyword
driver.find_element(by=By.CSS_SELECTOR, value=''input#J_search_input_index'').send_keys(keyword + Keys.ENTER)
time.sleep(0.5)

# find all images and names
icon_names = driver.find_elements(by=By.CSS_SELECTOR, value=''.block-icon-list>li>.icon-name'')
icon_images = driver.find_elements(by=By.CSS_SELECTOR, value=''.block-icon-list>li>.icon-twrap>img'')

result = []
for i in range(len(icon_images)):
    result.append({
        "name": icon_names[i].get_property("title"),
        "image": icon_images[i].get_property("src"),
    })

success = True',
'[{"key":"keyword","value":"","type":"String","required":true}]',
1, 1, 0, now(), now());

insert task_record(task_id, params, result, message, status, deleted, created_time, updated_time)
values (1, '{"keyword":"草莓"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"葡萄"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"苹果"}', null, null, 0, 0, now(), now()),
       (1, '{"keyword":"西瓜"}', null, null, 0, 0, now(), now());
