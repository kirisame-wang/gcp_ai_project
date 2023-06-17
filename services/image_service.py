'''

用戶上傳照片時，將照片從Line取回，放入CloudStorage

瀏覽用戶目前擁有多少張照片（未）

'''
import os
# from flask import Request
import numpy as np
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model
# import time
# import urllib.request

from google.cloud import storage
from linebot import LineBotApi
from linebot.models import TextSendMessage

# from daos import UserDAO
# from models import User
from utils import bucket_name, line_bot_api


# Load the model for classifying task
model = load_model('converted_savedmodel/model.savedmodel')


class ImageService:
    '''
    用戶上傳照片
    將照片取回
    將照片存入CloudStorage內
    '''

    @classmethod
    def line_user_upload_image(cls, event):
        # Initiate the bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # Save and upload the image
        image_blob = line_bot_api.get_message_content(event.message.id)
        temp_file_path = f"""{event.message.id}.png"""

        with open(temp_file_path, 'wb') as fd:
            for chunk in image_blob.iter_content():
                fd.write(chunk)

        blob = bucket.blob(f'{event.source.user_id}/image/{event.message.id}.png')
        blob.upload_from_filename(temp_file_path)

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Set the predicted classes
        class_dict = {}
        with open('converted_savedmodel/labels.txt') as f:
            for line in f.readlines():
                key, val = line.split()
                class_dict[int(key)] = val

        # Preprocessing the input data
        image = Image.open(temp_file_path)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0 - 1)

        # Load the image into the array
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array[0:224, 0:224, 0:3]

        # run the inference
        prediction = model.predict(data)
        # max_probability_item_index = np.argmax(prediction[0])
        # res = class_dict.get(max_probability_item_index)

        # 將預測值拿去尋找line_message
        # 並依照該line_message，進行消息回覆
        # if prediction.max() > 0.6:
        #     result_message_array = detect_json_array_to_new_message_array(f"line_message_json/{res}.json")
        #     self.line_bot_api.reply_message(event.reply_token, result_message_array)
        # else:
        #     self.line_bot_api.reply_message(event.reply_token,
        #                                     TextSendMessage("圖片無法辨認，圖片已上傳，請期待未來的AI服務！"))

        # 移除本地檔案
        os.remove(temp_file_path)

        # Reply messages
        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage("分析完成，你的屬性如下"),
                      TextSendMessage(f"狗派：{prediction[0][0] * 100:.1f}%"),
                      TextSendMessage(f"貓派：{prediction[0][1] * 100:.1f}%")])
