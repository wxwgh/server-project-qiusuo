import psycopg2

class PostGisDao:

    #构造函数
    def __init__(self):
        #打开数据连接
        self.conn= psycopg2.connect(
            database="postgres",
            user="postgis",
            password="0",
            host="192.168.84.30",
            port="5432"
        )
        #获取操作游标
        self.cursor = self.conn.cursor()

    #全部查询操作
    def select_all(self,sql_str):
        #执行查询
        self.cursor.execute(sql_str)
        #获取结果
        result = self.cursor.fetchall()
        #获取字段
        fields = self.cursor.description
        datas=[]
        for i in range(len(result)):
            data={}
            for s in range(len(fields)):
                data[fields[s][0]]=result[i][s]

            datas.append(data)

        self.conn.close()
        return datas
    #删除操作
    def delete_pg(self,sql_str):
        # 执行删除
        self.cursor.execute(sql_str)
        self.conn.commit()
        temp_count = self.cursor.rowcount
        self.conn.close()
        return temp_count
    #添加操作
    def add_pg(self,sql_str):
        # 执行添加
        self.cursor.execute(sql_str)
        self.conn.commit()
        temp_count = self.cursor.rowcount
        self.conn.close()
        return temp_count

    # 更新操作
    def update_pg(self, sql_str):
        # 执行更新
        self.cursor.execute(sql_str)
        self.conn.commit()
        temp_count = self.cursor.rowcount
        self.conn.close()
        return temp_count
    #批量更新操作
    def update_all_pg(self,sql_str,datas):
        # 执行更新
        self.cursor.executemany(sql_str,datas)
        self.conn.commit()
        temp_count = self.cursor.rowcount
        self.conn.close()
        return temp_count