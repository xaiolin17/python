#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: pcl
@file: 
@time: 2021/9/24 15:00
@desc: t_emp_position 公司部门岗位关系表     t_employee 员工信息表    t_employee_state 员工状态类型表
t_post_level 岗位层级表   t_post_type 岗位类别表      t_department 部门表    t_post 岗位表
t_company 公司基本信息表
"""
import json
import numpy as np
import pandas as pd
import pymysql
import io
import sys

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ipaddr = "17.0.XX.X0X"
username = "XXXX"
password = "XXXX"
port = 3306
db = "XXXX"

def connsql(post_level_name):
    conn = pymysql.connect(host=ipaddr, user=username, passwd=password, db=db, port=port)
    sql = '''SELECT 
                employee_name,                      #姓名
                employee_state_name,                #员工类型
                department_name,                    #部门
                post_name,                          #岗位
                post_type_name,                     #岗位类别
                post_level_name,                    #岗位层级
                company_name                        #公司名称
            FROM 
                ((((((t_employee LEFT JOIN t_emp_position ON  t_employee.employee_id = t_emp_position.emp_id)
                RIGHT JOIN t_employee_state ON t_employee.employee_state_id = t_employee_state.employee_state_id)
                LEFT JOIN t_post ON t_emp_position.post_id = t_post.post_id)
                LEFT JOIN t_department ON t_emp_position.dept_id = t_department.department_id)
                LEFT JOIN t_company ON t_emp_position.com_id = t_company.company_id)
                LEFT JOIN t_post_level ON t_emp_position.post_level_id = t_post_level.post_level_id)
                LEFT JOIN t_post_type ON t_emp_position.post_type_id = t_post_type.post_type_id
            WHERE 
                post_level_name = '%s' 
            ''' % post_level_name

    data = pd.read_sql(sql=sql, con=conn)
    conn.close()
    #pd.set_option('display.max_columns', None)  # 显示完整的列
    #pd.set_option('display.max_rows', None)  # 显示完整的行
    return data

def analysis(data):
    data.rename(columns={'employee_name': '姓名','department_name': '部门', 'post_type_name': '岗位类别','post_level_name': '岗位层级','employee_state_name': '员工类型',
                         'company_name': '公司名称','address': '公司地址','post_name': '岗位'}, inplace=True)

    data1 = data.to_dict(orient='records')

    newData = []
    for i in range(len(data1)):
        mData = {}
        keyNum = 0
        for item in data1[i]:
            mData.update({'key' + str(keyNum): item})
            mData.update({'value' + str(keyNum): data1[i][item]})
            keyNum += 1
        newData.append(mData)

    return newData

if __name__ == '__main__':
    post_level_name = '高层'
    current_page = 2
    current_number = 10

    #post_level_name = json.loads(sys.argv[1])['post_level_name']

    data = connsql(post_level_name)
    res = analysis(data=data)

    total_number = len(res)
    total_page = np.int32(np.ceil(np.divide(total_number, current_number)))
    current_dict = {'current_page': current_page, 'current_number': current_number}
    total_dict = {'total_page': total_page, 'total_number': total_number}
    # 页码和条数的字典
    current_dict.update(total_dict)

    res1 = res[(current_page - 1) * current_number:current_page * current_number - 1]
    res1.append(current_dict)
    print(res1)
