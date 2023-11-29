# test_chatbot.py
import requests

def send_message(user_id, message):
    url = 'http://127.0.0.1:8000/message'
    data = {'user_id': user_id, 'message': message}
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response Content:", response.content)
    return response.json()


def get_history(user_id):
    url = f'http://127.0.0.1:8000/history/{user_id}'
    response = requests.get(url)
    return response.json()

# 测试发送消息并获取回答
print(send_message("user123", "你好，机器人！"))
# 获取并打印聊天历史
print(get_history("user123"))

# 对另一个用户重复此过程
print(send_message("user456", "机器人，今天日期是多少？"))
print(get_history("user456"))
