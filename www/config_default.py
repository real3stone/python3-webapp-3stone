# config_default.py

configs = {
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'database': 'awesome'
    },
    'session': {
        'secret': 'AwEsOmE'
    }
}

# 如果要部署到服务器时，通常要修改数据库的host等信息，直接修改config_default.py
# 不是一个好方法，更好的做法是编写一个config_override.py，用来覆盖某些默认设置

