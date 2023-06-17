'''
當用戶關注時，必須取用照片，並存放至指定bucket位置，而後生成User物件，存回db
當用戶取消關注時，
    從資料庫提取用戶數據，修改用戶的封鎖狀態後，存回資料庫
'''

# import os
from urllib.parse import parse_qs

# from daos import UserDAO
from services import AudioService, ImageService, UserService, VideoService, TextService

class LineBotController:

    # 將消息交給用戶服務處理
    @classmethod
    def follow_event(cls, event):
        # print(event)
        UserService.line_user_follow(event)


    @classmethod
    def unfollow_event(cls, event):
        UserService.line_user_unfollow(event)


    # TODO: 未來可能會判斷用戶快取狀態，現在暫時無
    @classmethod
    def handle_text_message(cls, event):
        TextService.line_user_reply_text(event)
        return "OK"


    @classmethod
    def handle_image_message(cls, event):
        ImageService.line_user_upload_image(event)
        return "OK"


    @classmethod
    def handle_video_message(cls, event):
        VideoService.line_user_upload_video(event)
        return "OK"


    @classmethod
    def handle_audio_message(cls, event):
        AudioService.line_user_upload_audio(event)
        return "OK"


    # 擷取event的data欄位，並依照function_name，丟入不同的方法
    @classmethod
    def handle_postback_event(cls, event):

        # query string 拆解 event.postback.data
        query_string_dict = parse_qs(event.postback.data)

        # 擷取功能
        detect_function_name = query_string_dict.get('function_name')[0]

        # Postbakc function 功能對應轉發

        return 'no'
