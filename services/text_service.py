import numpy as np
import os
import random

from google.cloud import storage
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage, ImageSendMessage, QuickReply, QuickReplyButton, MessageAction

from daos import UserDAO
from utils import bucket_name, line_bot_api, detect_json_array_to_new_message_array

class TextService:


    @classmethod
    def line_user_reply_text(cls, event):
        cls.user = UserDAO.get_user(event.source.user_id)
        cls.line_bot_state = cls.user.line_bot_state

        if event.message.text == "預約會談":
            cls.line_bot_state = ""
            cls.reply_to_ask_meeting(event)

        elif event.message.text == "心理測驗":
            cls.line_bot_state = ""
            cls.send_testing(event)

        elif event.message.text == "開啟蘇格拉底式對話":
            cls.line_bot_state = ""
            cls.send_socratics(event)

        elif event.message.text == "禪繞畫":
            cls.line_bot_state = ""
            cls.send_zentangles(event)

        elif event.message.text == "聯繫專人":
            cls.line_bot_state = ""
            cls.reply_to_ask_service(event)

        elif event.message.text == "更多功能":
            cls.line_bot_state = ""
            cls.send_options(event)

        elif cls.line_bot_state.startswith("t"):
            cls.send_testing(event)

        elif cls.line_bot_state.startswith("s"):
            cls.send_socratics(event)


    @classmethod
    def send_zentangles(cls, event):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix='statics/'))

        img = random.choice(blobs)
        try:
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(f"https://storage.googleapis.com/tibame-ai-0602-bucket/{img.name}",
                                 f"https://storage.googleapis.com/tibame-ai-0602-bucket/{img.name}"))
        except LineBotApiError as e:
            line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage("發生錯誤，請稍後再試"))
            print(e)
        cls.user.line_bot_state = ""
        UserDAO.save_user(cls.user)

    @classmethod
    def send_testing(cls, event):
        quick_reply_template = QuickReply(
            items=[QuickReplyButton(action=MessageAction(label="非常同意", text="非常同意")),
                   QuickReplyButton(action=MessageAction(label="同意", text="同意")),
                   QuickReplyButton(action=MessageAction(label="中立", text="中立")),
                   QuickReplyButton(action=MessageAction(label="不同意", text="不同意")),
                   QuickReplyButton(action=MessageAction(label="非常不同意", text="非常不同意"))])
        scores = {"非常同意": 5, "同意": 4, "中立": 3, "不同意": 2, "非常不同意": 1}
        facets_with_interpretations = {"(E) 外向性": "您在生活中是個喜歡社交生活的人，擁有強烈的好奇心與創造力。",
                                       "(A) 親和性": "您在生活中擁有良好的人際關係，您的特質讓朋友們經常願意信任並親近您。",
                                       "(C) 盡責性": "您在朋友眼中經常是值得信賴的，您十分擅長堅持以完成目標。",
                                       "(N) 神經質": "您在生活中對於負面情緒較為敏感，但也讓您容易發現弦外之音。",
                                       "(O) 開放性": "您在生活中面對新事物是較為開放的，探索並發展不同興趣是您的樂趣來源。"}

        if not cls.line_bot_state:
            line_bot_api.reply_message(
                event.reply_token,
                messages=[TextSendMessage("以下測驗共有十題，答案沒有對錯，你可選擇隨時退出。"),
                          TextSendMessage("（1）我認為自己是個拘謹的人。", quick_reply=quick_reply_template)])
            cls.user.line_bot_state = "t1"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t1":  # Testing state 1
            cls.user.testing1 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（2）我認為自己一般而言值得信任。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t2"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t2":  # Testing state 2
            cls.user.testing2 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（3）我認為自己喜歡懶散的生活步調。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t3"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t3":  # Testing state 3
            cls.user.testing3 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（4）我認為自己是放鬆的，很擅長面對壓力。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t4"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t4":  # Testing state 4
            cls.user.testing4 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（5）我認為自己比較缺乏藝術類的興趣。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t5"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t5":  # Testing state 5
            cls.user.testing5 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（6）我認為自己是個外向且喜歡社交的人。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t6"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t6":  # Testing state 6
            cls.user.testing6 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（7）我認為自己習慣從別人身上尋找產生錯誤的原因。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t7"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t7":  # Testing state 7
            cls.user.testing7 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（8）我認為自己做事總是十分全面。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t8"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t8":  # Testing state 8
            cls.user.testing8 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（9）我認為自己是個容易緊張的人。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t9"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t9":  # Testing state 9
            cls.user.testing9 = scores[event.message.text]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("（10）我認為自己擁有活躍的想像力。", quick_reply=quick_reply_template))
            cls.user.line_bot_state = "t10"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "t10":  # Testing state 10
            cls.user.testing10 = scores[event.message.text]
            e_score = -1 * cls.user.testing1 + cls.user.testing5
            a_score = cls.user.testing2 - cls.user.testing7
            c_score = -1 * cls.user.testing3 + cls.user.testing8
            n_score = -1 * cls.user.testing4 + cls.user.testing9
            o_score = -1 * cls.user.testing5 + cls.user.testing10

            max_score_ind = np.argmax([e_score, a_score, c_score, n_score, o_score])
            max_score_facet = list(facets_with_interpretations.keys())[max_score_ind]

            line_bot_api.reply_message(
                event.reply_token,
                messages=[TextSendMessage(f"測驗結果顯示您得分最高的項目為{max_score_facet}，解釋如下："),
                          TextSendMessage(f"{list(facets_with_interpretations.values())[max_score_ind]}")])
            cls.user.line_bot_state = ""
            UserDAO.save_user(cls.user)

    @classmethod
    def send_socratics(cls, event):
        if not cls.line_bot_state:
            line_bot_api.reply_message(event.reply_token,
                                           messages=[TextSendMessage("你看起來有些困擾，要不要試著跟我說說看呢？"),
                                                     TextSendMessage("（回覆內容請在同一則訊息中送出）")])
            cls.user.line_bot_state = "s1"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "s1":  # Socratic state I
            line_bot_api.reply_message(
                event.reply_token,
                messages=[TextSendMessage("你面臨的狀況聽起來真不容易"),
                          TextSendMessage("如果是你的朋友遇到這樣的情況，你會提出哪些方法試著協助他呢？"),
                          TextSendMessage("（回覆內容請在同一則訊息中送出）")])
            cls.user.line_bot_state = "s2"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "s2":  # Socratic state II
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    "哇！聽來真不錯，我們可以嘗試用這個方法來幫助自己嗎？",
                    quick_reply=QuickReply(
                        items=[QuickReplyButton(
                            action=MessageAction(label="可以",
                                                 text="可以")),
                            QuickReplyButton(
                                action=MessageAction(label="不行",
                                                     text="不行")),
                            QuickReplyButton(
                                action=MessageAction(label="終止蘇格拉底式對話",
                                                     text="終止蘇格拉底式對話"))])))
            cls.user.line_bot_state = "s3"
            UserDAO.save_user(cls.user)

        elif cls.line_bot_state == "s3":  # Socratic state III
            if event.message.text == "可以":
                line_bot_api.reply_message(
                    event.reply_token,
                    messages=[TextSendMessage(
                        "太好了！很高興你從自己身上找到了力量$祝你有美好的一天。",
                        emojis=[{"index": 18,
                                 "productId": "5ac2213e040ab15980c9b447",
                                 "emojiId": "035"}]),
                        TextSendMessage("（蘇格拉底式對話已結束）")])
                cls.user.line_bot_state = ""
                UserDAO.save_user(cls.user)

            elif event.message.text == "不行":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage("試著再想想看，還有什麼其他做法或許可以幫助到這位朋友呢？"))
                cls.user.line_bot_state = "s2"
                UserDAO.save_user(cls.user)

            elif event.message.text == "終止蘇格拉底式對話":
                line_bot_api.reply_message(
                    event.reply_token,
                    messages=[TextSendMessage("或者我們可以藉由專業人士的協助和陪伴來尋找解方，請選擇聯繫專人或直接預約會談。"),
                              TextSendMessage(
                                  "（蘇格拉底式對話已結束）",
                                  quick_reply=QuickReply(
                                      items=[QuickReplyButton(
                                          action=MessageAction(label="聯繫專人",
                                                               text="聯繫專人")),
                                             QuickReplyButton(
                                          action=MessageAction(label="預約會談",
                                                               text="預約會談"))]))])
                cls.user.bot_state = ""
                UserDAO.save_user(cls.user)


    @classmethod
    def reply_to_ask_meeting(cls, event):
        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage("請填寫以下預約會談表單，完成後我們將盡快與您聯繫。"),
                      TextSendMessage("https://forms.gle/kkDTtw7n3HuztTuU7")])


    @classmethod
    def reply_to_ask_service(cls, event):
        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage("已收到您的要求，我們將盡快與您聯繫。"),
                      TextSendMessage("或者您也可以致電至我們的服務專線：0800-123-123")])


    @classmethod
    def send_options(cls, event):
        line_bot_api.reply_message(
            event.reply_token,
            messages=detect_json_array_to_new_message_array("line_message_json/MoreOptions.json"))
