# coding=utf-8
class ChoiceItem(object):
    """
    Класс для определения наборов перечислений.
    """
    def __init__(self, value, name):
        self.name = name
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        raise AttributeError


class Choices(object):
    """
    Класс для определения перечислений в полях моделей.
    """
    class ChoicesDescriptor(object):
        def __get__(self, instance, owner):
            return tuple([
                tuple([
                    owner.__dict__[attr_key].value,
                    owner.__dict__[attr_key].name
                ]) for attr_key in owner.__dict__.keys() if not attr_key.startswith('__')
            ])

        def __set__(self, instance, value):
            raise AttributeError

    choices = ChoicesDescriptor()

    def __getattribute__(self, attr):
        attr_instance = object.__getattribute__(self, attr)
        if attr_instance.__class__ is ChoiceItem:
            return attr_instance.value

        return attr_instance
