# -*- coding: utf-8 -*-

import cx_Oracle
import traceback


class oracledb(object):
    def __init__(self, host='', user='',password=''):
        self.host = host
        self.user = user
        self.password = password

    def checkconnect(self):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            cur.close()
            cnxn.close()
            return True
        except:
            traceback.print_exc()
            return False

    def getMeterNum(self, startTime, endTime):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select distinct MANU_FACTUR,count(MANU_FACTUR) " \
                  "from METER_INFO " \
                  "where SAVE_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "group by MANU_FACTUR ".format(startTime, endTime)
            cur.execute(sql)
            rows = cur.fetchall()
            meterNumList = []
            for i in range(len(rows)):
                meterNumList.append(rows[i])
            cur.close()
            cnxn.close()
            return meterNumList
        except:
            traceback.print_exc()
            return []

    def getMeterFormList(self, startTime, endTime):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select MANU_FACTUR,count(distinct BATCHID),count(MANU_FACTUR)," \
                  "count(case when CHECK_RESULT = 0 then 1 else null end) " \
                  "from METER_INFO " \
                  "where SAVE_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "group by MANU_FACTUR".format(startTime, endTime)
            cur.execute(sql)
            rows = cur.fetchall()
            meterFormList = []
            for i in range(len(rows)):
                meterFormList.append(rows[i])
            cur.close()
            cnxn.close()
            return meterFormList
        except:
            traceback.print_exc()
            return []

    def getErrorData(self, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select M.MANU_FACTUR,count(M.GUID_ID)," \
                  "count(case when T.ROUNDERROR>0 then 1 else null end)," \
                  "count(case when T.ROUNDERROR<0 then 1 else null end)," \
                  "count(case when T.ROUNDERROR=0 then 1 else null end)," \
                  "count(case when T.AVERGERROR>0 then 1 else null end)," \
                  "count(case when T.AVERGERROR<0 then 1 else null end)," \
                  "count(case when T.AVERGERROR=0 then 1 else null end) " \
                  "from METER_INFO M, " \
                  "(select GUID_ID,AVERGERROR,ROUNDERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA " \
                  "union all " \
                  "select GUID_ID,AVERGERROR,ROUNDERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA_HIS) T " \
                  "where M.GUID_ID=T.GUID_ID " \
                  "and M.CHECK_RESULT = 1 " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('%s','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('%s','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.ITEMNAME = '基本误差P+,H,(1.0Ib,1.0)' " \
                  "group by M.MANU_FACTUR" % (startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()
            errorList = []
            for i in range(len(rows)):
               errorList.append(rows[i])
            cur.close()
            cnxn.close()
            return errorList
        except:
            traceback.print_exc()
            return []



class oracledb_old(oracledb):

    def getErrorData(self, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select M.MANU_FACTUR,count(M.GUID_ID)," \
                  "count(case when T.ROUNDERROR>0 then 1 else null end)," \
                  "count(case when T.ROUNDERROR<0 then 1 else null end)," \
                  "count(case when T.ROUNDERROR=0 then 1 else null end)," \
                  "count(case when T.AVERGERROR>0 then 1 else null end)," \
                  "count(case when T.AVERGERROR<0 then 1 else null end)," \
                  "count(case when T.AVERGERROR=0 then 1 else null end) " \
                  "from METER_INFO M, " \
                  "(select GUID_ID,AVERGERROR,ROUNDERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA " \
                  "union all " \
                  "select GUID_ID,AVERGERROR,ROUNDERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA_HIS) T " \
                  "where M.GUID_ID=T.GUID_ID " \
                  "and M.CHECK_RESULT=1 " \
                  "and T.TRIAL_DATE " \
                  "between to_date('%s','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('%s','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.ITEMNAME = '基本误差P+,H,(1.0Ib,1.0)' " \
                  "group by M.MANU_FACTUR" % (startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()
            errorList = []
            for i in range(len(rows)):
               errorList.append(rows[i])
            cur.close()
            cnxn.close()
            return errorList
        except:
            traceback.print_exc()
            return []

    def getMeterFormList(self, startTime, endTime):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select MANU_FACTUR,count(distinct BATCH_ID),count(MANU_FACTUR)," \
                  "count(case when CHECK_RESULT = 0 then 1 else null end) " \
                  "from METER_INFO " \
                  "where SAVE_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "group by MANU_FACTUR".format(startTime, endTime)
            cur.execute(sql)
            rows = cur.fetchall()
            meterFormList = []
            for i in range(len(rows)):
                meterFormList.append(rows[i])
            cur.close()
            cnxn.close()
            return meterFormList
        except:
            traceback.print_exc()
            return []

