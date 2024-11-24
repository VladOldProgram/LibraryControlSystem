class Singleton(type):
    """
    Класс паттерна Singleton, используемый в качестве метакласса при реализации 
    каким-либо классом этого паттерна.
    """

    __instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]