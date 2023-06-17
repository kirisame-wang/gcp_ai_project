'''

用戶上傳照片時，將照片從Line取回，放入CloudStorage

瀏覽用戶目前擁有多少張照片（未）

'''

# from flask import Request
import os
# import urllib.request

from google.cloud import storage
# from linebot import LineBotApi
from linebot.models import TextSendMessage


# from daos import UserDAO
# from models import User
from utils import line_bot_api


class AudioService:
    # line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    '''
    用戶上傳照片
    將照片取回
    將照片存入CloudStorage內
    '''

    @classmethod
    def line_user_upload_audio(cls, event):
        # 取出照片
        image_blob = line_bot_api.get_message_content(event.message.id)
        temp_file_path = f"""{event.message.id}.mp3"""

        #
        with open(temp_file_path, 'wb') as fd:
            for chunk in image_blob.iter_content():
                fd.write(chunk)

        # 上傳至bucket
        storage_client = storage.Client()
        bucket_name = os.environ['USER_INFO_GS_BUCKET_NAME']
        destination_blob_name = f'{event.source.user_id}/audio/{event.message.id}.mp3'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(temp_file_path)

        # 移除本地檔案
        os.remove(temp_file_path)

        # 回覆消息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(f"""音訊已上傳，請期待未來的AI服務！""")
        )
