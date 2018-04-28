# config_override.py

# config_default.py作为开发环境的标准配置，
# config_override.py作为生产环境的标准配置，
# 这样就即方便地在本地开发，又可以随时把应用部署到服务器！

configs = {
    'db': {
        'host': '127.0.0.1'
    }
}
