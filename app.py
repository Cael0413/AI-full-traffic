from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from chatbot import chat_with_gpt
from sheets import add_to_sheet

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Error:", e)
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text
    print(f"來自 {user_id} 的訊息：{msg}")

    reply = chat_with_gpt(msg)
    add_to_sheet(user_id, msg, tag="我要諮詢")
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

@app.route("/")
def index():
    return "LINE Bot with AI + Sheets is running!"
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 預設5000
    app.run(host="0.0.0.0", port=port)

