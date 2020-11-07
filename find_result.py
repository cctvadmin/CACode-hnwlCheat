import _lib
import time
import json

from data_util import DatabaseOperational


def removeAttribute(driver, elementobj, attributeName):
    '''
    封装删除页面属性的方法
    调用JS代码删除页面元素的指定的属性，arguments[0]~arguments[1]分别
    会用后面的element，attributeName参数进行替换
    '''
    driver.execute_script("arguments[0].removeAttribute(arguments[1])",
                          elementobj, attributeName)


def select_all_que():
    _database = DatabaseOperational()
    _data = _database.getAll('SELECT * FROM `hnwl_c2_cacode_20201107`')
    return _data


def quest(b, q):
    que = ''
    for i in q:
        que += str(i)
    try:
        b.get('https://zhidao.baidu.com/')
        time.sleep(0.4)
        search_form_new = _b.find_element_by_id('search-form-new')
        input = search_form_new.find_element_by_tag_name('input')
        input.click()

        input.send_keys(que.replace('\t', '').replace(
            '\r\n', '').replace('\n', ''))
        button = search_form_new.find_element_by_tag_name('button')
        button.click()
        time.sleep(0.4)
        dl = b.find_element_by_id(
            'wgt-list').find_elements_by_tag_name('dl')[0].find_element_by_tag_name('dt')
        link = dl.find_element_by_tag_name('a')
        removeAttribute(b, link, 'target')
        link.click()
        time.sleep(0.4)
        _text = b.find_elements_by_class_name(
            'content')[0].find_elements_by_tag_name('div')[0].text
    except Exception as e:
        _text = que + str(e)
    return _text


if __name__ == '__main__':
    _b = _lib.get_browser()
    ques = select_all_que()
    _result = {'result': []}
    for i, v in enumerate(ques):
        print(i)
        _re = quest(_b, [v['title'], v['selects']])
        _result['result'].append({
            'index': i,
            'content': _re
        })
        print(_re)
    op = open('./hnwl_c2_result_cacode_20201107.json', 'w+', encoding='utf-8')
    _result = json.dumps(_result, sort_keys=True, indent=4,
                         separators=(',', ':'), ensure_ascii=False)
    print(_result)
    op.write(_result)
    _b.close()
