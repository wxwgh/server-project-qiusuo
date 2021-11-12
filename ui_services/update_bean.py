
class UpdateBean:

    datas=[]
    # 构造函数
    def __init__(self):
        # 初始化返回数据属性
        self.datas = []

    #递归方法
    def get_datas(self,info):
        for i in range(len(info)):
            data = []
            data.append(info[i]['node_type'])
            data.append(info[i]['order_code'])
            data.append(info[i]['parent_id'])
            data.append(info[i]['parent_node_type'])
            data.append(info[i]['id'])
            self.datas.append(data)
            if len(info[i]['children']) > 0:
                self.get_datas(info[i]['children'])
        return self.datas