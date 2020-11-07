import _lib
import time
import json

if __name__ == '__main__':
    _b = _lib.get_browser()
    _b.get("https://hnwledu.ls365.net/University/User/Student/ExaminationQuery.aspx?m=wdks")
    login_name = _b.find_element_by_id('LoginName')
    login_pwd = _b.find_element_by_id('LoginPwd')
    login_name.click()
    login_name.send_keys("440882200108015498")
    login_pwd.click()
    login_pwd.send_keys("666666")
    login_btn = _b.find_element_by_id('loginbtn')
    login_btn.click()

    time.sleep(3)

    _b.find_element_by_link_text('我的考试').click()
    time.sleep(3)

    _start_score = _b.find_elements_by_link_text('开始考试')
    _start_score[0].click()
    time.sleep(3)
    exam_question = _b.find_elements_by_class_name('exam_question')
    _questions = {'question': []}
    for index, i in enumerate(exam_question):
        exam_question_title = i.find_element_by_class_name(
            'exam_question_title')
        title = str(exam_question_title.text).replace(
            '\r\n', '\t').replace('\n', '\t')
        selects = i.find_element_by_class_name(
            'question_select').find_elements_by_tag_name('li')
        selects_que = []
        for j in selects:
            selects_que.append(str(j.text).replace(
                '\r\n', '\t').replace('\n', '\t'))
        _questions['question'].append({
            'index': index,
            'title': title,
            'selects': selects_que
        })
    _result = json.dumps(_questions, sort_keys=True, indent=4,
                         separators=(',', ':'), ensure_ascii=False)
    op = open('./hnwl_c2_cacode_20201107.json', 'w+', encoding='utf-8')
    op.write(_questions)
    op.close()
    print(_result)
