'''
Author: DingWang wangding19@mails.ucas.ac.cn
Date: 2023-08-04 09:52:47
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-08-04 11:16:12
FilePath: \LLM Course by Ngwu\prompt-engineering-for-developers-main\prompt-engineering-for-developers-main\content\LangChain Chat with Your Data\LLM.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import time
import logging
import requests
from typing import Optional, List, Dict, Mapping, Any

import langchain
from langchain.llms.base import LLM
from langchain.cache import InMemoryCache

logging.basicConfig(level=logging.INFO)
# 启动llm的缓存
langchain.llm_cache = InMemoryCache()

class ChatGLM(LLM):
    
    # 模型服务url
    url = "http://10.26.128.38:8595/chat"

    @property
    def _llm_type(self) -> str:
        return "chatglm"

    def _construct_query(self, prompt: str) -> Dict:
        """构造请求体
        """
        query = {
            "human_input": prompt
        }
        return query

    @classmethod
    def _post(cls, url: str,
        query: Dict) -> Any:
        """POST请求
        """
        _headers = {"Content_Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url, 
                json=query, 
                headers=_headers, 
                timeout=60)
        return resp

    
    def _call(self, prompt: str, 
        stop: Optional[List[str]] = None) -> str:
        """_call
        """
        # construct query
        query = self._construct_query(prompt=prompt)

        # post
        resp = self._post(url=self.url,
            query=query)
        
        if resp.status_code == 200:
            resp_json = resp.json()
            predictions = resp_json["response"]
            return predictions
        else:
            return "请求模型" 
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.
        """
        _param_dict = {
            "url": self.url
        }
        return _param_dict

# if __name__ == "__main__":
#     llm = ChatGLM()
#     while True:
#         human_input = input("Human: ")

#         begin_time = time.time() * 1000
#         # 请求模型
#         response = llm(human_input, stop=["you"])
#         end_time = time.time() * 1000
#         used_time = round(end_time - begin_time, 3)
#         logging.info(f"chatGLM process time: {used_time}ms")

#         print(f"ChatGLM: {response}")