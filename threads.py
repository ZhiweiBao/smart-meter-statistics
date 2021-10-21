from PyQt5 import QtCore
from db_Oracle import oral_operate
from typechange import typechange
from algorithm import algorithm
import traceback


class facThread(QtCore.QThread):
    signal_facdata = QtCore.pyqtSignal(list, list)

    def __int__(self, parent=None):
        super(facThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            meterNum1 = db_op.getMeterNum(self.startTime, self.endTime)
            meterNum2 = db_op_old.getMeterNum(self.startTime, self.endTime)
            facList = []
            numList = []
            for i in range(len(meterNum1)):
                facList.append(meterNum1[i][0])
                numList.append(meterNum1[i][1])
            for i in range(len(meterNum2)):
                if meterNum2[i][0] in facList:
                    index = facList.index(meterNum2[i][0])
                    numList[index] += meterNum2[i][1]
                else:
                    facList.append(meterNum2[i][0])
                    numList.append(meterNum2[i][1])

            self.signal_facdata.emit(facList, numList)
        except:
            traceback.print_exc()

class meterFormThread(QtCore.QThread):
    signal_meterFormdata = QtCore.pyqtSignal(list)


    def __int__(self, parent=None):
        super(meterFormThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime
    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            meterNum1 = db_op.getMeterFormList(self.startTime, self.endTime)
            meterNum2 = db_op_old.getMeterFormList(self.startTime, self.endTime)
            facList = []
            batchList = []
            numList = []
            unqualList = []
            for i in range(len(meterNum1)):
                facList.append(meterNum1[i][0])
                batchList.append(meterNum1[i][1])
                numList.append(meterNum1[i][2])
                unqualList.append(meterNum1[i][3])
            for i in range(len(meterNum2)):
                if meterNum2[i][0] in facList:
                    index = facList.index(meterNum2[i][0])
                    batchList[index] += meterNum2[i][1]
                    numList[index] += meterNum2[i][2]
                    unqualList[index] += meterNum2[i][3]
                else:
                    facList.append(meterNum2[i][0])
                    batchList.append(meterNum2[i][1])
                    numList.append(meterNum2[i][2])
                    unqualList.append(meterNum2[i][3])
            meterFormList = []
            for i in range(len(facList)):
                meterFormList.append([facList[i], batchList[i], numList[i], unqualList[i], (1-unqualList[i]/numList[i])])
            self.signal_meterFormdata.emit(meterFormList)
        except:
            traceback.print_exc()

class meterGraphThread(QtCore.QThread):
    signal_meterGraphdata = QtCore.pyqtSignal(list)
    # TODO

    def __int__(self, parent=None):
        super(meterGraphThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime
    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            meterNum1 = db_op.getMeterFormList(self.startTime, self.endTime)
            meterNum2 = db_op_old.getMeterFormList(self.startTime, self.endTime)
            facList = []
            numList = []
            unqualList = []
            for i in range(len(meterNum1)):
                facList.append(meterNum1[i][0])
                numList.append(meterNum1[i][2])
                unqualList.append(meterNum1[i][3])
            for i in range(len(meterNum2)):
                if meterNum2[i][0] in facList:
                    index = facList.index(meterNum2[i][0])
                    numList[index] += meterNum2[i][2]
                    unqualList[index] += meterNum2[i][3]
                else:
                    facList.append(meterNum2[i][0])
                    numList.append(meterNum2[i][2])
                    unqualList.append(meterNum2[i][3])
            meterGraphList = []
            for i in range(len(facList)):
                meterGraphList.append([facList[i], (1-unqualList[i]/numList[i])])
            self.signal_meterGraphdata.emit(meterGraphList)
        except:
            traceback.print_exc()

class errorThread(QtCore.QThread):
    signal_errorData = QtCore.pyqtSignal(list)


    def __int__(self, parent=None):
        super(errorThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            errorData1 = db_op.getErrorData(self.startTime, self.endTime)
            errorData2 = db_op_old.getErrorData(self.startTime, self.endTime)
            facList = []
            numList = []
            roundpList = []
            roundnList = []
            roundzList = []
            avergpList = []
            avergnList = []
            avergzList = []
            for i in range(len(errorData1)):
                facList.append(errorData1[i][0])
                numList.append(errorData1[i][1])
                roundpList.append(errorData1[i][2])
                roundnList.append(errorData1[i][3])
                roundzList.append(errorData1[i][4])
                avergpList.append(errorData1[i][5])
                avergnList.append(errorData1[i][6])
                avergzList.append(errorData1[i][7])
            for i in range(len(errorData2)):
                if errorData2[i][0] in facList:
                    index = facList.index(errorData2[i][0])
                    numList[index] += errorData2[i][1]
                    roundpList[index] += errorData2[i][2]
                    roundnList[index] += errorData2[i][3]
                    roundzList[index] += errorData2[i][4]
                    avergpList[index] += errorData2[i][5]
                    avergnList[index] += errorData2[i][6]
                    avergzList[index] += errorData2[i][7]
                else:
                    facList.append(errorData2[i][0])
                    numList.append(errorData2[i][1])
                    roundpList.append(errorData2[i][2])
                    roundnList.append(errorData2[i][3])
                    roundzList.append(errorData2[i][4])
                    avergpList.append(errorData2[i][5])
                    avergnList.append(errorData2[i][6])
                    avergzList.append(errorData2[i][7])
            errorDataList = []
            for i in range(len(facList)):
                errorDataList.append([facList[i], numList[i],
                                      roundpList[i], roundnList[i], roundzList[i],
                                       (roundpList[i] / numList[i]),
                                       (roundnList[i] / numList[i]),
                                       (roundzList[i] / numList[i]),
                                      avergpList[i], avergnList[i], avergzList[i],
                                       (avergpList[i] / numList[i]),
                                       (avergnList[i] / numList[i]),
                                       (avergzList[i] / numList[i])])
            self.signal_errorData.emit(errorDataList)
        except:
            traceback.print_exc()