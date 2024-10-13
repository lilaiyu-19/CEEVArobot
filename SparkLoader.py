from sparkai.depreciated.service.spark_ws import answer

import SparkApi
import time

appid = "3be93f01"
api_secret = "YWM3NjE2YjJkZWY4MjY4NDhkZDdiNTY4"
api_key = "358446a7028bec707aca7b77e6e92f04"

domain_4 = "4.0Ultra"
domain_3 = "generalv3.5"  # Max版本
domain_2 = "generalv3"       # Pro版本
#domain = "general"         # Lite版本

Spark_url_4 = "wss://spark-api.xf-yun.com/v4.0/chat"  # ultra服务地址
Spark_url_3 = "wss://spark-api.xf-yun.com/v3.5/chat"  # Max服务地址
Spark_url_2 = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址

def getText(role, content, now_text):
    json_con = {"role": role, "content": content}
    now_text.append(json_con)
    return now_text


def get_length(get_length_text):
    length = 0
    for content in get_length_text:
        temp = content["content"]
        temp_len = len(temp)
        length += temp_len
    return length


def check_len(check_len_text):
    while get_length(check_len_text) > 1000:
        del check_len_text[1]
    return check_len_text


class SparkLoader:
    # 初始化上下文内容
    text = [
        {"role": "system",
         "content": "你现在是一位高考志愿填报咨询师，"
                    "你了解中国各大院校各省各专业最近几年的招生分数；接下来请用咨询师的口吻为用户解答相关问题,尽量简短不超过500字。"},
    ]
    domain = ''
    Spark_url = ""

    def __init__(self, model):
        if model == 'Spark Pro':
            self.domain = domain_2
            self.Spark_url = Spark_url_2
        elif model == 'Spark Max':
            self.domain = domain_3
            self.Spark_url = Spark_url_3
        else:
            self.domain = domain_4
            self.Spark_url = Spark_url_4

    def Question(self, input_text):
        question = check_len(getText("user", input_text, self.text))
        SparkApi.main(appid, api_key, api_secret, self.Spark_url, self.domain, question)
        getText("assistant", SparkApi.answer, self.text)
        answer_now = SparkApi.answer
        SparkApi.answer = ""
        return answer_now
