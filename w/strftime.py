#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:
@file: gxpt-qjtj-ct
@time: 2021/9/27 10:00
@desc: bpm_approve_opinion 审批意见表    bpm_apply 申请单管理
签章使用时间均以审批完成时间进行统计
"""
import json
import numpy as np
import pandas as pd
import pymysql
import io
import sys
import time
import datetime

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ipaddr = "1xx.x0.xx.x0x"
username = "root"
password = "xxxxxx"
port = 3306
db = "oa_prod_bpm_xxxx"

def connsql(year, month, applicant, companyName):
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
                task_name,                                           #审批
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
                process_name REGEXP '印章|印鉴'
                {(lambda x: '' if x == '' or x == None else 'AND YEAR(bpm_approve_opinion.update_time) = %d'  %x ) (year)}
                {(lambda x: '' if x == '' or x == None else f"AND apply_real_name REGEXP  '{applicant}' " ) (applicant)}
                {(lambda x: '' if x == '' or x == None else f"AND apply_company_name REGEXP  '{companyName}' " ) (companyName)}

            '''

    data = pd.read_sql(sql=sql, con=conn)
    conn.close()
    # pd.set_option('display.max_columns', None)  # 显示完整的列
    # pd.set_option('display.max_rows', None)  # 显示完整的行
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

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

if __name__ == '__main__':
    year = json.loads(sys.argv[1])['year']
    month = json.loads(sys.argv[1])['month']
    applicant = json.loads(sys.argv[1])['applicant']
    companyName = json.loads(sys.argv[1])['companyName']
    current_page = json.loads(sys.argv[1])['current_page']
    current_number = json.loads(sys.argv[1])['current_number']

    data = connsql(year, month, applicant, companyName)
    res = analysis(data=data)

    total_number = len(res)
    total_page = np.float64(np.ceil(np.divide(total_number, current_number)))
    current_dict = {'current_page': current_page, 'current_number': current_number}
    total_dict = {'total_page': total_page, 'total_number': total_number}
    # 页码和条数的字典
    current_dict.update(total_dict)

    res1 = res[(current_page - 1) * current_number:current_page * current_number]
    res1.append(current_dict)
    print(json.dumps(res1,ensure_ascii=False,cls=DateEncoder))