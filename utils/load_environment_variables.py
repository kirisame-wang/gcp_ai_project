import os

from linebot import LineBotApi, WebhookHandler


try:
    bucket_name = os.environ['USER_INFO_GS_BUCKET_NAME']
    # db = firestore.Client.from_service_account_json(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    handler = WebhookHandler(channel_secret=os.environ["LINE_CHANNEL_SECRET"])
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
except KeyError:  # To use dotenv in localhost to get environment variables
    from dotenv import load_dotenv
    load_dotenv()
    bucket_name = os.environ['USER_INFO_GS_BUCKET_NAME']
    # db = firestore.Client.from_service_account_json(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    handler = WebhookHandler(channel_secret=os.environ["LINE_CHANNEL_SECRET"])
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])