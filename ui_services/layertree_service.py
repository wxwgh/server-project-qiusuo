from flask import Blueprint,request
from flask_cors import CORS
from postgis.postgis_dao import PostGisDao
from ui_services.result_bean import ResultBean
from ui_services.update_bean import UpdateBean
import json
#蓝图创建
layertree_service=Blueprint("layertree_service",__name__)

#获取图层树配置服务
@layertree_service.route("/get_layertree_config",methods=["GET"])
def get_layertree_config():
    sql_str = "select * from layertree order by order_code asc"
    datas = PostGisDao().select_all(sql_str)
    layer_config={}
    for i in range(len(datas)):
        if i == 0:
            layer_config={
                "id":datas[i]["id"],
                "node_name":datas[i]["node_name"],
                "parent_id":datas[i]["parent_id"],
                "node_type":datas[i]["node_type"],
                "is_leaf":datas[i]["is_leaf"],
                "order_code":datas[i]["order_code"],
                "children":[]
            }
        else:
            if datas[i]["node_type"] == "一级目录":
                temp_config={
                    "id": datas[i]["id"],
                    "node_name": datas[i]["node_name"],
                    "parent_id": datas[i]["parent_id"],
                    "node_type": datas[i]["node_type"],
                    "parent_node_type":datas[i]["parent_node_type"],
                    "is_leaf": datas[i]["is_leaf"],
                    "order_code": datas[i]["order_code"],
                    "children": []
                }
                layer_config["children"].append(temp_config)
            elif datas[i]["node_type"] == "二级目录":
                temp_config = {
                    "id": datas[i]["id"],
                    "node_name": datas[i]["node_name"],
                    "parent_id": datas[i]["parent_id"],
                    "node_type": datas[i]["node_type"],
                    "parent_node_type": datas[i]["parent_node_type"],
                    "is_leaf": datas[i]["is_leaf"],
                    "order_code": datas[i]["order_code"],
                    "children": []
                }
                for j in range(len(layer_config["children"])):
                    if datas[i]["parent_id"] == layer_config["children"][j]["id"]:
                        layer_config["children"][j]["children"].append(temp_config)
            elif datas[i]["node_type"] == "叶子节点":
                # temp_config = {
                #     "id": datas[i]["id"],
                #     "node_name": datas[i]["node_name"],
                #     "parent_id": datas[i]["parent_id"],
                #     "url_type": datas[i]["url_type"],
                #     "url": datas[i]["url"],
                #     "node_type": datas[i]["node_type"],
                #     "parent_node_type": datas[i]["parent_node_type"],
                #     "is_leaf": datas[i]["is_leaf"],
                #     "layer_name": datas[i]["layer_name"],
                #     "tile_matrix": datas[i]["tile_matrix"],
                #     "order_code": datas[i]["order_code"],
                #     "opacity":datas[i]["opacity"],
                #     "opacity_flag":datas[i]["opacity_flag"],
                #     "icon_size": datas[i]["icon_size"],
                #     "icon_color": datas[i]["icon_color"],
                #     "icon_class": datas[i]["icon_class"],
                #     "icon_image": datas[i]["icon_image"],
                #     "children": []
                # }
                datas[i]["children"]=[]
                temp_config = datas[i]
                for j in range(len(layer_config["children"])):
                    if datas[i]["parent_id"] == layer_config["children"][j]["id"]:
                        layer_config["children"][j]["children"].append(temp_config)
                    else:
                        for x in range(len(layer_config["children"][j]["children"])):
                            if datas[i]["parent_id"] == layer_config["children"][j]["children"][x]["id"]:
                                layer_config["children"][j]["children"][x]["children"].append(temp_config)
                                continue
    temp_data = []
    temp_data.append(layer_config)
    return json.dumps(temp_data)

#添加节点服务
@layertree_service.route("/add_layer_tree",methods=["POST"])
def add_layer_tree():
    info = json.loads(request.data)
    sql_str = "insert into layertree(id,node_name,parent_id,url_type,url,node_type,is_leaf,layer_name,tile_matrix,order_code,opacity,opacity_flag,parent_node_type,icon_size,icon_color,icon_class,icon_image,icon_radio)" \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
              (info['id'],info['node_name'],info['parent_id'],info['url_type'],info['url'],info['node_type'],info['is_leaf'],info['layer_name'],info['tile_matrix'],info['order_code'],info['opacity'],info['opacity_flag'],info['parent_node_type'],
               info['icon_size'],info['icon_color'],info['icon_class'],info['icon_image'],info['icon_radio'])
    temp_count = PostGisDao().add_pg(sql_str)
    if temp_count > 0:
        result = ResultBean(200, "节点添加成功").__dict__
    else:
        result = ResultBean(400, "节点添加失败").__dict__
    return result


#删除节点服务
@layertree_service.route("/delete_layer_tree",methods=["POST"])
def delete_layer_tree():
    ids = json.loads(request.data)
    sql_str = "delete from layertree where id in ({})".format(','.join(['\''+str(ids[i])+'\'' for i in range(len(ids))]))
    temp_count = PostGisDao().delete_pg(sql_str)
    if temp_count > 0 :
        result = ResultBean(200,"节点删除成功").__dict__
    else:
        result = ResultBean(400, "节点删除失败").__dict__
    return result

#更新节点服务
@layertree_service.route("/update_layer_tree",methods=["POST"])
def update_layer_tree():
    info= json.loads(request.data)
    datas = UpdateBean().get_datas(info["children"])
    sql_str = "update layertree set node_type = %s,order_code= %s,parent_id= %s,parent_node_type= %s where id = %s"
    temp_count = PostGisDao().update_all_pg(sql_str,datas)
    print(temp_count)
    if temp_count > 0 :
        result = ResultBean(200,"数据同步成功").__dict__
    else:
        result = ResultBean(400, "数据同步失败").__dict__
    return result





#重命名节点服务
@layertree_service.route("/rename_layer_tree",methods=["POST"])
def rename_layer_tree():
    info= json.loads(request.data)
    sql_str = "update layertree set node_name = {} where id = {}".format('\''+info["node_name"]+'\'','\''+info["id"]+'\'')
    print(sql_str)
    temp_count = PostGisDao().update_pg(sql_str)
    if temp_count > 0:
        result = ResultBean(200, "重命名成功").__dict__
    else:
        result = ResultBean(400, "重命名失败").__dict__
    return result

#测试服务 获取矢量数据
@layertree_service.route("/get_vector",methods=["GET"])
def get_vector():
    datas=[
        {
            "lng": "125.08",
            "lat": "5.51",
            "name": "菲律宾棉兰老岛"
        },
        {
            "lng": "155.14",
            "lat": "-6.19",
            "name": "所罗门群岛"
        },
        {
            "lng": "153.47",
            "lat": "-4.53",
            "name": "新爱尔兰地区"
        },
    ]
    return json.dumps(datas)
#测试服务 获取矢量数据
@layertree_service.route("/get_vector2",methods=["GET"])
def get_vector2():
    datas=[
        {
            "lng": "141.38",
            "lat": "37.39",
            "name": "日本本州东岸近海"
        },
        {
            "lng": "140.5",
            "lat": "27.9",
            "name": "日本小笠原群岛地区"
        },
        {
            "lng": "144.5",
            "lat": "39.9",
            "name": "日本本州东海岸附近海域"
        },
    ]
    return json.dumps(datas)