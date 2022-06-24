import pandas as pd

# 设置显示窗口数据显示别全是...（可删除）
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

def change_data(data):
    # print('***\n','******\n', '创建新数据\n')
    def change(x):
        pair = []
        for i in x:
            pair.append(i.split('___')[1])
        return set(pair)
    # def change_pair(x):
    #     pair = []
    #     for i in x:
    #         pair.append(i.split('___')[1])
    #     return set(pair)
    #
    data_0 = data
    data_0['aibao与差集相同list'] = data_0['aibao与差集相同'].apply(lambda x: x.split('=hsbx='))
    data_0['aibao___定损配件list'] = data_0['aibao___定损配件'].apply(lambda  x: x.split('=hsbx='))
    data_1 = data_0[['报案号', '车架号', 'aibao与差集相同list', 'aibao___定损配件list']]
    data_1['pair'] = data_1['aibao___定损配件list'].apply(change)
    data_1['存在'] = data_1['aibao与差集相同list'].apply(lambda x: set(x))
    data_result = data_1[['报案号', '车架号', 'pair', '存在']]
    data_result['不存在'] = data_result['pair'] - data_result['存在']
    data_result['存在'] = data_result['存在'].apply(lambda x: sorted(list(x)))
    data_result['不存在'] = data_result['不存在'].apply(lambda x: sorted(list(x)))
    # print(data_result)
    return data_result


def match(new_data, price):
    # print("\n******获取价格******\n")
    report_no, brand, = [], []
    exist, exist_price = [], []
    nonexistence, nonexistence_price = [], []
    for i in range(len(new_data)):
        line = new_data.iloc[i]
        exist_price_str, nonexistence_str = '', ''
        # 存在
        for word in line['存在']:
            if word not in ['', ' ', None]:
                a = price[(price['报案号'] == line['报案号']) &
                          (price['车架号'] == line['车架号']) &
                          (price['配件名称'] == word)]
                exist_price_str += '-' + str(a.iloc[0, 8])
        # 不存在
        for word in line['不存在']:
            if word not in ['', ' ', None]:
                a = price[(price['报案号'] == line['报案号']) &
                          (price['车架号'] == line['车架号']) &
                          (price['配件名称'] == word)]
                nonexistence_str += '-' + str(a.iloc[0, 8])

        report_no.append(line['报案号'])
        brand.append(line['车架号'])
        exist.append(line['存在'])
        exist_price.append(exist_price_str.strip('-'))
        nonexistence.append(line['不存在'])
        nonexistence_price.append(nonexistence_str.strip('-'))

    return pd.DataFrame({'报案号': report_no, '车架号': brand,
                         '存在': exist, '价格1': exist_price,
                         '不存在': nonexistence, '价格2': nonexistence_price})

def result_data(result):
    # print("\n******格式文件创建******\n")
    report_no, brand, = [], []
    exist, exist_price = [], []
    nonexistence, nonexistence_price = [], []

    for i in range(len(result)):
        line = result.iloc[i]
        # print('\nline ', line)
        # print(i+1, ' ----> ', i/(len(result)))
        maxlen = max([1, len(line[2]), len(line[3].split('-')), len(line[4]), len(line[5].split('-'))])
        # 案件号写入一个
        report_no.append(line[0])
        report_no.extend(['' for i in range(maxlen - 1)])
        # 车架号写入一个
        brand.append(line[1])
        brand.extend(['' for i in range(maxlen - 1)])
        # 存在
        exist.extend(line[2])
        exist.extend(['' for i in range(maxlen - len(line[2]))])
        exist_price.extend(line[3].split('-'))
        exist_price.extend(['' for i in range(maxlen - len(line[3].split('-')))])
        # 不存在
        nonexistence.extend(line[4])
        nonexistence.extend(['' for i in range(maxlen - len(line[4]))])
        nonexistence_price.extend(line[5].split('-'))
        nonexistence_price.extend(['' for i in range(maxlen - len(line[5].split('-')))])
    # print(len(report_no), len(brand), len(exist), len(exist_price), len(nonexistence), len(nonexistence_price))
    return pd.DataFrame({'报案号': report_no, '车架号': brand,
                         '存在': exist, '价格1': exist_price,
                         '不存在': nonexistence, '价格2': nonexistence_price})

if __name__ == '__main__':
    data = pd.read_excel('./x定损与_结果与差集比对中间结果20220616.xlsx', sheet_name=0)
    data = data[['报案号', '车架号', 'aibao与差集相同', 'aibao___定损配件']].dropna(subset=['aibao___定损配件'])
    new_data = change_data(data)
    price = pd.read_excel('./_工时+配件.xlsx', sheet_name=1)
    data_price = match(new_data, price)
    # print("\n****创建文件连接文件")
    # data_price.to_excel('_存在-不存在（价格）中间集20220616(4).xlsx', index=False)
    result_excel = result_data(data_price)
    # print("\n****结果输出.xlsx")
    result_excel.to_excel('_存在-不存在（价格）20220616(4).xlsx', index=False)
