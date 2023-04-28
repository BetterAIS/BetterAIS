"""
MIT License

Copyright (c) 2023 Illia Chaban

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import datetime
import openai
import random
import json

from better_ais.config.openai import OpenAiSettings
from .base_client import AISClient
from openai.error import RateLimitError
from collections import defaultdict

class FakeAISClient(AISClient):
    """FakeAisClient is a fake implementation of Client for accademic information systems."""

    def __init__(self, openai_settings: OpenAiSettings):
        self.__openai_settings = openai_settings
        self.__homeworks_hashing: dict[str, list[str]] = defaultdict(list)
        self.__documents_hashing: dict[str, list[str]] = defaultdict(list)

    async def __create_completion(self, prompt: str, max_tokens: int = 5):
        prompt = """Act like StuDModocol,
 StuDModocol logged in to the academician information system of your university. Your university is called 'STU'. The website of your academician information system is 'https://is.stuba.sk'. 
StuDModocol write every answer using json and nothing else. This is an example of StuDModocol's answer: {"answer": "hello, world"}
StuDModocol can imagine about everything. For example, when it imagines about what is next subject, it says: {"answer": "TZIV"}. When it imagines about what is the current time, it says: {"answer": "9:00"}.
""" + prompt

        openai.api_key = self.__openai_settings.api_key
        try:
            response = await asyncio.to_thread(
                    openai.Completion.create, 
                    
                    engine=self.__openai_settings.model,
                    prompt=prompt,
                    temperature=0.8,
                    max_tokens=max_tokens
            )
            print(prompt)
            print(response)
        except RateLimitError:
            print("RateLimitError")
            return "Not enough tokens. This is a fake AIS."
        return response.choices[0].text # type: ignore

    async def __gen_email(self, username: str):
        prompt = f"""StuDModocol, Imagine, You'r username is "{username}". You got a new email. Imagine about possible content of:
- Who is the mail sender name? (answer alias: MailSenderName)
- Who is the mail username? (answer alias: MailSenderUserName)
- What is the subject of the mail? (answer alias: MailSubject)
- What is the body of the mail? (answer alias: MailBody)
"""
        try:
            gpt_chatbot_response = await self.__create_completion(prompt=prompt, max_tokens=100)
            data = json.loads(gpt_chatbot_response)
            sender = data.get("MailSenderName", "John Doe") + " <" + data.get("MailSenderUserName", "johnd") + "@stuba.sk>"
            subject = data.get("MailSubject", "Hello, world!")
            body = data.get("MailBody", "Hello, world!")
        except json.JSONDecodeError:
            sender = "John Doe <johnd@stuba.sk>"
            subject = "Hello, world!"
            body = "Hello, world!"
        
        return {
            'id': random.randint(0, 1000000),
            'sender': sender,
            'subject': subject,
            'body': body,
            'is_read': False,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
        }

    async def __gen_document(self, username: str):
        prompt = f"""StuDModocol, Imagine, You'r username is "{username}". You got a new document. Imagine about possible content of:
- Who is the author of the document? (answer alias: DocumentAuthor)
- What is the title of the document? (answer alias: DocumentTitle)
- What is the subject of the document? (answer alias: DocumentSubject)
- What is the description of the document? (answer alias: DocumentDescription)
- What is the link of the document? (answer alias: DocumentLink)
- What is the file path of the document? (answer alias: DocumentFilePath)
"""
        try:
            gpt_chatbot_response = await self.__create_completion(prompt=prompt, max_tokens=100)
            data = json.loads(gpt_chatbot_response)
            author = data.get("DocumentAuthor", "John Doe")
            title = data.get("DocumentTitle", "Hello, world!")
            subject = data.get("DocumentSubject", "Hello, world!")
            description = data.get("DocumentDescription", "Hello, world!")
            link = data.get("DocumentLink", "https://is.stuba.sk")
            file_path = data.get("DocumentFilePath", "/home/johnd")
        except json.JSONDecodeError:
            author = "John Doe"
            title = "Hello, world!"
            subject = "Hello, world!"
            description = "Hello, world!"
            link = "https://is.stuba.sk"
            file_path = "/home/johnd"
        
        return {
            'id': random.randint(0, 1000000),
            'author': await self.__create_completion(prompt=author, max_tokens=5),
            'title': await self.__create_completion(prompt=title, max_tokens=5),
            'subject': await self.__create_completion(prompt=subject, max_tokens=5),
            'description': await self.__create_completion(prompt=description, max_tokens=100),
            'link': await self.__create_completion(prompt=link, max_tokens=5),
            'file_path': await self.__create_completion(prompt=file_path, max_tokens=5),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
        }
    
    async def __gen_homework(self, username: str):
        prompt = f"""StuDModocol, Imagine, You'r username is "{username}". You got a new homework. Imagine about possible content of:
- What is the title of the homework? (answer alias: HomeworkTitle)
- What is the description of the homework? (answer alias: HomeworkDescription)
- What is the link of the homework? (answer alias: HomeworkLink)
"""
        try:
            gpt_chatbot_response = await self.__create_completion(prompt=prompt, max_tokens=100)
            data = json.loads(gpt_chatbot_response)
            title = data.get("HomeworkTitle", "Hello, world!")
            description = data.get("HomeworkDescription", "Hello, world!")
            link = data.get("HomeworkLink", "https://is.stuba.sk")
        except json.JSONDecodeError:
            title = "Hello, world!"
            description = "Hello, world!"
            link = "https://is.stuba.sk"
        
        return {
            'id': random.randint(0, 1000000),
            'title': await self.__create_completion(prompt=title, max_tokens=5),
            'description': await self.__create_completion(prompt=description, max_tokens=100),
            'link': await self.__create_completion(prompt=link, max_tokens=5),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
        }

    async def get_new_mails(self, username: str, password: str):
        if random.randint(0, 5):
            return []
        
        new_mails = [await self.__gen_email(username)]
        return new_mails

    async def get_documents(self, username: str, password: str):
        if random.randint(0, 5):
            return self.__documents_hashing[username]
        
        new_documents = []
        for _ in range(random.randint(1, 5)):
            new_documents.append(await self.__gen_document(username))
        
        self.__documents_hashing[username].extend(new_documents)
        
        return self.__documents_hashing[username]

    async def get_homeworks(self, username: str, password: str):
        if random.randint(0, 5):
            return self.__homeworks_hashing[username]
        
        new_homeworks = []
        for _ in range(random.randint(1, 5)):
            new_homeworks.append(await self.__gen_homework(username))

        self.__homeworks_hashing[username].extend(new_homeworks)
        
        return self.__homeworks_hashing[username]

    async def get_time_table(self, username: str, password: str):
        mock = [
            {
                "day": 0,
                "lesson": "1. hodina",
                "time": 8,
                "teacher": "Ing. Jonathan Joestar, PhD.",
                "room": "D2",
            }, 
            {
                "day": 0,
                "lesson": "2. hodina",
                "time": 2,
                "teacher": "Ing. George Joestar, PhD.",
                "room": "D2",
            },
            {
                "day": 1,
                "lesson": "1. hodina",
                "time": 1,
                "teacher": "Ing. Jonathan Joestar, PhD.",
                "room": "D2",
            },
            {
                "day": 1,
                "lesson": "2. hodina",
                "time": 3,
                "teacher": "Ing. George Joestar, PhD.",
                "room": "D2",
            },
            {
                "day": 2,
                "lesson": "1. hodina",
                "time": 1,
                "teacher": "Ing. Jonathan Joestar, PhD.",
                "room": "D2",
            }
        ]
        
        return mock