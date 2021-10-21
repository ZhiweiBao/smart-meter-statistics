import numpy as np
# from scipy import stats
from datetime import datetime
import traceback

def classifyResource(data):
    result = [[[] for col in range(60)] for row in range(20)]
    try:

        for i in range(len(data)):
            a = data[i][0]-1
            b = data[i][1]-1
            # if float(data[i][2]) < 10:
            result[a][b].append(data[i][2])
    except:
        traceback.print_exc()
    return result

# def declassify(date, data):
#     result = []
#     try:
#         date = datetime.strptime(date, '%Y-%m-%d')
#         for i in range(len(data)):
#             for j in range(len(data[i])):
#                 for k in range(len(data[i][j])):
#                     data[i][j][k] = str(data[i][j][k])
#                 insertData = [date, j+1, i+1]
#                 insertData.extend(data[i][j])
#                 result.append(insertData)
#     except:
#         traceback.print_exc()
#     return result

# def classifyLocal(data):
#     result = [[['nan', 'nan', 'nan', 'nan', 'nan'] for col in range(20)] for row in range(60)]
#     try:
#
#         for i in range(len(data)):
#             a = data[i][0]-1
#             b = data[i][1]-1
#             result[b][a]=data[i][2:]
#     except:
#         traceback.print_exc()
#     return result

def terror_analyze(data):
    result = [[[0, float('nan')] for col in range(60)] for row in range(20)]
    tresult = [[0, float('nan')] for i in range(20)]
    try:
        if len(data) != 20 or len(data[0]) != 60:
            print("预警分析数据格式不正确！")
            return result
        for i in range(len(data)):
            num = 0
            res = []
            for j in range(len(data[i])):
                # # TODO 数据为''时如何处理
                # if data[i][j] == '':
                #     data[i][j] =
                # data[i][j] = float(data[i][j])
                if len(data[i][j]) <= 0:
                    result[i][j] = [0, float('nan')]
                else:
                    result[i][j] = [len(data[i][j]), mean(data[i][j])]
                res.extend(data[i][j])
                num = len(res)
            if num == 0:
                tresult[i] = [0, float('nan')]
            else:
                tresult[i] = [num, mean(res)]
    except:
        traceback.print_exc()
    return result, tresult


def alert_analyze(data):
    result = [[[0, 0, float('nan'), float('nan'), float('nan'), float('nan')] for col in range(60)] for row in range(20)]
    try:
        if len(data) != 20 or len(data[0]) != 60:
            print("预警分析数据格式不正确！")
            return result
        for i in range(len(data)):
            for j in range(len(data[i])):
                # # TODO 数据为''时如何处理
                # if data[i][j] == '':
                #     data[i][j] =
                # data[i][j] = float(data[i][j])
                if len(data[i][j]) <= 0:
                    result[i][j] = [0, 0, float('nan'), float('nan'), float('nan'), float('nan')]
                else:
                    result[i][j]=[len(data[i][j]), pass_percent(data[i][j]), mean(data[i][j]), var(data[i][j]), skew(data[i][j]), kurtosis(data[i][j])]
    except:
        traceback.print_exc()
    return result

def pass_percent(data):
    try:
        num = 0
        # if len(data) == 0:
        #     return 0
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
                if abs(data[i]) > 0.6:
                    num += 1
            except:
                num += 1
        result = 1 - num/len(data)
    except:
        result = 0
        traceback.print_exc()
    return result

def mean(data):
    try:
        error = []
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
                if data[i] < 1 and data[i] > -1:
                    error.append(data[i])
            except:
                pass
        if error == []:
            return float('nan')
        return np.mean(error)
    except:
        traceback.print_exc()
        return float('nan')

def var(data):
    try:
        error = []
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
                error.append(data[i])
            except:
                pass
        if error == []:
            return float('nan')
        return np.var(error)
    except:
        traceback.print_exc()
        return float('nan')

def skew(data):

    try:
        error = []
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
                error.append(data[i])
            except:
                pass
        n = len(error)
        if n == 0 or n == 1:
            return float('nan')
        m = 0
        m2 = 0
        m3 = 0
        for t in error:
            m += t
            m2 += t * t
            m3 += t ** 3
        m /= n
        m2 /= n
        m3 /= n
        # 代入公式求个值
        mu = m
        if (m2 - mu * mu) < 0:
            return float('nan')
        sigma = np.sqrt(m2 - mu * mu)
        if sigma == 0:
            return float('nan')
        skew = (m3 - 3 * mu * m2 + 2 * mu ** 3) / sigma ** 3
        return skew
    except:
        print(data)
        traceback.print_exc()
        return float('nan')


def kurtosis(data):
    try:
        error = []
        for i in range(len(data)):
            try:
                data[i] = float(data[i])
                error.append(data[i])
            except:
                pass
        n = len(error)
        if n == 0 or n == 1:
            return float('nan')
        m = 0
        m2 = 0
        m3 = 0
        m4 = 0
        for t in error:
            m += t
            m2 += t * t
            m3 += t ** 3
            m4 += t ** 4
        m /= n
        m2 /= n
        m3 /= n
        m4 /= n
        # 代入公式求个值
        mu = m
        if (m2 - mu * mu) < 0:
            return float('nan')
        sigma = np.sqrt(m2 - mu * mu)
        if sigma == 0:
            return float('nan')
        kurtosis = (m4 - 4 * mu * m3 + 6 * mu * mu * m2 - 4 * mu ** 3 * mu + mu ** 4) / sigma ** 4 - 3
        return kurtosis
    except:
        traceback.print_exc()
        return float('nan')

def pauta(data):
    x = []
    for i in range(len(data)):
        if str(data[i]) != 'nan':
            x.append(data[i])
    n = len(x)
    if n == 0 or n == 1:
        return [float('nan'),float('nan')]
    m = 0
    m2 = 0
    for t in x:
        m += t
        m2 += t * t
    m /= n
    m2 /= n
    mu = m
    sigma = np.sqrt(m2 - mu * mu)
    return [mu - (3 * sigma), mu + (3 * sigma)]
