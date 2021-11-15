from flask import Flask
from ui_services.layertree_service import layertree_service
from flask_cors import CORS

# 主路由文件
app = Flask(__name__)

CORS(app)
# 蓝图注册 需要把模块下声明的蓝图对象导入
app.register_blueprint(layertree_service, url_prefix="/layertree_service")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=15000)
    # app.run()