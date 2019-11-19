import re

from pypinyin import pinyin, lazy_pinyin, load_phrases_dict

if __name__ == '__main__':
    print(f'{pinyin("中心")}')
    print(f'{lazy_pinyin("樊昌学")}')
    print(f'{lazy_pinyin("音乐")}')
    print(f'{lazy_pinyin("啊奥哦额")}')
    load_phrases_dict({
        '蹒跚': [['pen'], ['shan']],
        '你好': [['hi'], ['ya']]
    })
    print(f'{lazy_pinyin("你好蹒跚好")}')

    listdate = re.split(r'[年月日号]', '2019年4月18')
    if listdate[-1] == '':
        listdate.pop()
    print('-'.join(listdate))

    date_pattern = re.compile(r'((\d+)年)?(\d+)月(\d+)([日号])?')


    def year_repl(matchobj):
        if matchobj.group(1):
            return f'{matchobj.group(2)}-{matchobj.group(3)}-{matchobj.group(4)}'
        else:
            from datetime import datetime
            return f'{datetime.today().year}-{matchobj.group(3)}-{matchobj.group(4)}'


    print(date_pattern.sub(year_repl, '4月18'))
    print(date_pattern.sub(year_repl, '4月18'))
    print(date_pattern.sub(year_repl, '2018年4月18号'))


    def process_carid(carid):
        intab = '一二三四五六七八九零'
        outtab = '1234567890'
        transtab = str.maketrans(intab, outtab)
        return carid.translate(transtab)


    print(f'{process_carid("r七八九零")}')
