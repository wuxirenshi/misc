# -*- coding: utf-8 -*-


class Symbol(object):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    EQUAL = '='
    COMMA = ','
    QUOTES = '\''
    LEFT_BRACKET = '('
    RIGHT_BRACKET = ')'
    NONE = 'None'
    FALSE = 'False'
    TRUE = 'True'


class Parse(Symbol):
    """字符串数据解析"""
    def __init__(self, data):
        self.data = data.replace('\\"', '\"')
        self.key = self.value = ''
        self.maps = {}
        self.status = Parse.ZERO

    @property
    def resource(self):
        if isinstance(self.data, str):
            for index, element in enumerate(self.data):
                if self.status == Parse.ZERO:
                    if element == Parse.EQUAL:
                        self.status = Parse.ONE
                        continue
                    self.key += element

                if self.status == Parse.ONE:
                    if element == Parse.COMMA:
                        self.update()
                        continue
                    self.value += element
                    if self.is_end(index):
                        self.update()
                        break
                    if element == Parse.QUOTES:
                        self.reset_value_with_status(Parse.TWO)
                        continue
                    if element == Parse.LEFT_BRACKET:
                        self.reset_value_with_status(Parse.THREE)
                        continue

                if self.status == Parse.TWO:
                    if self.is_end(index):
                        self.update()
                        break
                    if element == Parse.QUOTES:
                        self.status = Parse.ONE
                        self.value = self.value.decode("utf-8")
                        continue
                    self.value += element

                if self.status == Parse.THREE:
                    if self.is_end(index):
                        self.update()
                        break
                    if element == Parse.RIGHT_BRACKET:
                        parse = Parse(self.value)
                        self.value = parse.resource
                        self.status = Parse.ONE
                        continue
                    self.value += element
        return self.maps

    def reset(self):
        self.key = self.value = ''
        self.status = Parse.ZERO

    def is_end(self, index):
        return index == len(self.data)-1

    def process(self):
        if self.value == Parse.NONE:
            self.value = None
        if self.value == Parse.FALSE:
            self.value = False
        if self.value == Parse.TRUE:
            self.value = True

    def reset_value_with_status(self, status):
        self.value = ''
        self.status = status

    def update(self):
        self.process()
        self.maps[self.key.strip()] = self.value
        self.reset()
