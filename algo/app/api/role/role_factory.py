'''
Date: 2024-08-27 10:15:48
LastEditors: 牛智超
LastEditTime: 2024-08-27 10:16:06
FilePath: \app\api\role\role_factory.py
'''
from abc import ABC, abstractmethod


# 抽象产品
class AbstractButton(ABC):
    @abstractmethod
    def paint(self) -> str:
        pass

class AbstractTextField(ABC):
    @abstractmethod
    def paint(self) -> str:
        pass