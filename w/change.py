#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:
@file: 
@time: 2021/9/27 10:00
@desc: bpm_approve_opinion 审批意见表    bpm_apply 申请单管理
出差时间均以审批完成时间进行统计
"""
import json
import numpy as np
import pandas as pd
import pymysql
import io
import sys
import time

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ipaddr = "1X2.XX.XX.XXX"
username = "root"
password = "XXX"
port = 3306
db = "oa_"

def connsql(month):
    conn = pymysql.connect(host=ipaddr, user=username, passwd=password, db=db, port=port)
    sql = f'''SELECT
                apply_title,                                         #申请标题
                apply_real_name,                                     #实际申请人
                apply_dept_name,                                     #申请人部门
                apply_company_name,                                  #申请人公司名称
                process_name,                                        #审核名称
                apply_status,                                        #申请状态
                bpm_apply.create_by  AS op_cby,                      #申请创建人
                bpm_apply.create_time AS op_ctime,                   #申请创建时间
                bpm_apply.update_by AS op_uby,                       #申请修改人
                bpm_apply.update_time AS op_utime,                   #申请修改时间
                flow_type,                                           #流程类型
                task_name,                                           #任务名
                approve_opinion,                                     #审批意见
                bpm_approve_opinion.create_by AS cby,                #审批人员
                bpm_approve_opinion.create_time AS ctime,            #审批时间
                bpm_approve_opinion.update_by AS uby,                #审批修改人
                bpm_approve_opinion.update_time AS utime             #审批修改时间
            FROM
                bpm_approve_opinion
                LEFT JOIN bpm_apply ON bpm_approve_opinion.apply_id = bpm_apply.id
            WHERE
                bpm_approve_opinion.deleted = 0 AND
                {(lambda x: '' if x == '' else 'MONTH(bpm_approve_opinion.update_time) = %d AND'  %x ) (month)}
                process_name REGEXP '因公外出|出销差' AND
                bpm_apply.apply_status = 3

            '''

    data = pd.read_sql(sql=sql, con=conn)
    conn.close()
    pd.set_option('display.max_columns', None)  # 显示完整的列
    pd.set_option('display.max_rows', None)  # 显示完整的行
    return data

def analysis(data):
    data[['op_ctime','op_utime','ctime','utime']] = data[['op_ctime','op_utime','ctime','utime']].astype(str)

    data.rename(columns={'apply_title': '申请标题', 'apply_real_name': '实际申请人', 'apply_dept_name': '申请人部门',
                         'apply_company_name': '申请人公司名称', 'process_name': '审核名称',
                         'apply_status': '申请状态', 'op_cby': '申请创建人', 'op_ctime': '申请创建时间', 'op_uby': '申请修改人',
                         'op_utime': '申请修改时间',
                         'flow_type': '流程类型', 'task_name': '任务名', 'approve_opinion': '审批意见', 'cby': '审批人员',
                         'ctime': '审批时间', 'uby': '审批修改人', 'utime': '审批修改时间'}, inplace=True)

    data = data.to_dict(orient='records')

    newData = []
    for i in range(len(data)):
        mData = {}
        keyNum = 0
        for item in data[i]:
            mData.update({'key' + str(keyNum): item})
            mData.update({'value' + str(keyNum): data[i][item]})
            keyNum += 1
        newData.append(mData)

    return newData

if __name__ == '__main__':
    month = 9
    current_page = 2
    current_number = 10
    # month = json.loads(sys.argv[1])['month']
    # current_page = json.loads(sys.argv[1])['current_page']
    # current_number = json.loads(sys.argv[1])['current_number']

    data = connsql(month)
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
