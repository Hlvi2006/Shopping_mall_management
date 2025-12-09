class BaseAppException(Exception):
    """Bütün xətaların törədiyi əsas klass"""
    pass

class ValidationException(BaseAppException):
    """Daxil edilən məlumat yanlış olduqda atılan xəta"""
    pass

class NotFoundException(BaseAppException):
    """Axtarılan məlumat tapılmadıqda atılan xəta"""
    pass

class BusinessRuleException(BaseAppException):
    """Biznes qaydası pozulduqda (məs: dolmuş dükana icarə vermək)"""
    pass

