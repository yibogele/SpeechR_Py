# import jieba
# import json
import logging
import re
from collections import namedtuple
from pathlib import Path

from pypinyin import lazy_pinyin, load_phrases_dict


class ActionParser:
    logger = logging.getLogger(__name__)
    # date_pattern = re.compile(r'年月日号')
    date_pattern = re.compile(r'((\d+)年)?(\d+)月(\d+)([日号])?')

    def __init__(self, verbs_path):
        self.verbs_path = verbs_path
        self._action_verbs = []
        self._init_action_verbs(verbs_path)

        # log
        type(self).logger.info("ActionParser 动作列表: %s", self._action_verbs)

    def _init_action_verbs(self, verbs_path):
        # with open(verbs_path, 'rt', encoding='utf-8') as f:
        with Path(verbs_path).open('r', encoding='utf-8') as f:
            self._action_verbs = [line.strip() for line in f]
            self._action_verbs.sort(reverse=True)

    def get_action_param(self, action_string):
        ActionParam = namedtuple('ActionParam', 'action target')
        for action in self._action_verbs:
            if action_string.startswith(action):
                target = action_string[len(action):]
                pinyin = type(self).get_pinyin_result(action, target)
                action_param = ActionParam(action, pinyin)
                return action_param
        return ActionParam('', '')

    @classmethod
    def get_pinyin_result(cls, action, target):
        ActionParser.fix_pinyin()

        if action == '选择项目' or action == '显示':
            return ''.join(lazy_pinyin(target))
        #
        elif action == '选择日期':

            def year_repl(matchobj):
                if matchobj.group(1):
                    return f'{matchobj.group(2)}-{matchobj.group(3)}-{matchobj.group(4)}'
                else:
                    from datetime import datetime
                    return f'{datetime.today().year}-{matchobj.group(3)}-{matchobj.group(4)}'

            return cls.date_pattern.sub(year_repl, target)

        elif action == '选择':
            if target.startswith('人员'):
                return ''.join(lazy_pinyin(target[len('人员'):]))
            elif target.startswith('车牌号'):
                def process_carid(carid):
                    intab = '一二三四五六七八九零'
                    outtab = '1234567890'
                    transtab = str.maketrans(intab, outtab)
                    return carid.translate(transtab)

                return process_carid(target[len('车牌号'):])
            elif target.startswith('设施'):
                return target[len('设施'):]

        elif action == '勾选':
            if target == '公测':
                return '公厕'
 

        return target

    @classmethod
    def fix_pinyin(cls):
        load_phrases_dict({
            '大成': [['da'], ['cheng']],
            # '你好': [['hi'], ['ya']]
        })

    def __repr__(self):
        return f'{type(self).__name__}({self.verbs_path},{self.dict_path})'


__all__ = ['ActionParser']
