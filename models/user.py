'''
基於Line給的用戶屬性，定義用戶類別
並提供 to_dict,  from_dict方法，使能在object與dict間快速轉換
提供 __repr__ 快速打印參數
'''
from __future__ import annotations


class User(object):

    # 物件基礎建構式
    def __init__(self, line_user_id, line_user_pic_url, line_user_nickname,
                 line_user_status, line_user_system_language, line_bot_state=None,
                 testing1=None, testing2=None, testing3=None, testing4=None,
                 testing5=None, testing6=None, testing7=None, testing8=None,
                 testing9=None, testing10=None, blocked=False) -> None:
        self.line_user_id = line_user_id
        self.line_user_pic_url = line_user_pic_url
        self.line_user_nickname = line_user_nickname
        self.line_user_status = line_user_status
        self.line_user_system_language = line_user_system_language
        self.line_bot_state = line_bot_state
        self.testing1 = testing1
        self.testing2 = testing2
        self.testing3 = testing3
        self.testing4 = testing4
        self.testing5 = testing5
        self.testing6 = testing6
        self.testing7 = testing7
        self.testing8 = testing8
        self.testing9 = testing9
        self.testing10 = testing10
        self.blocked = blocked


    def __repr__(self) -> str:
        return (f'''User(
            line_user_id={self.line_user_id},
            line_user_pic_url={self.line_user_pic_url},
            line_user_nickname={self.line_user_nickname},
            line_user_status={self.line_user_status},
            line_user_system_language={self.line_user_system_language},
            line_bot_state={self.line_bot_state},
            blocked={self.blocked}
            )''')


    # source的欄位係以 資料庫欄位做為預設命名
    @staticmethod
    def from_dict(source: dict) -> User:
        user = User(
            line_user_id=source.get(u'line_user_id'),
            line_user_pic_url=source.get(u'line_user_pic_url'),
            line_user_nickname=source.get(u'line_user_nickname'),
            line_user_status=source.get(u'line_user_status'),
            line_user_system_language=source.get(u'line_user_system_language'),
            line_bot_state=source.get("line_bot_state"),
            testing1=source.get(u'testing1'),
            testing2=source.get(u'testing2'),
            testing3=source.get(u'testing3'),
            testing4=source.get(u'testing4'),
            testing5=source.get(u'testing5'),
            testing6=source.get(u'testing6'),
            testing7=source.get(u'testing7'),
            testing8=source.get(u'testing8'),
            testing9=source.get(u'testing9'),
            testing10=source.get(u'testing10'),
            blocked=source.get(u'blocked'))
        return user

    def to_dict(self) -> dict:
        user_dict = {
            "line_user_id": self.line_user_id,
            "line_user_pic_url": self.line_user_pic_url,
            "line_user_nickname": self.line_user_nickname,
            "line_user_status": self.line_user_status,
            "line_user_system_language": self.line_user_system_language,
            "line_bot_state": self.line_bot_state,
            "testing1": self.testing1,
            "testing2": self.testing2,
            "testing3": self.testing3,
            "testing4": self.testing4,
            "testing5": self.testing5,
            "testing6": self.testing6,
            "testing7": self.testing7,
            "testing8": self.testing8,
            "testing9": self.testing9,
            "testing10": self.testing10,
            "blocked": self.blocked}
        return user_dict
