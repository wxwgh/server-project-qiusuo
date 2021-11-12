from flask import Flask
from ui_services.layertree_service import layertree_service


# 主路由文件
app = Flask(__name__)

# 蓝图注册 需要把模块下声明的蓝图对象导入
app.register_blueprint(layertree_service, url_prefix="/layertree_service")

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port="18000",debug=True)
    app.run()
