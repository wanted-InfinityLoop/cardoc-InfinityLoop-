import re


def password_validator(password):
    return re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$").match(password)

def tire_validator(tire):
    return re.compile("\d{3}\/\d{2}R\d{2}").match(tire)
