# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
# while True:
#     user_password = input('Please input your password:')
#     if user_password == '123':
#         print('Thanks for login!')
#         print('开始运行')
#         break
#     else:
#         print('Your password is wrong!')
#         print('Please input again!')

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor
from ui.Ui_SMeter_Statistics import Ui_MainWindow
from database_setting import database_setting
from db_Oracle import oral_operate
import os
import configparser
from typechange import typechange
from algorithm import algorithm
import traceback
import threads
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import cm
import xlwt

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
from datetime import datetime

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.Window)
        self.showMaximized()
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.database_set = database_setting()
        self.database_info = []
        self.database_info_old = []

        currentPath = os.getcwd()

        ini_path = currentPath + "\statistics_config.ini"
        ini_exist = os.path.exists(ini_path)

        if ini_exist == 0:
            try:
                # -----创建配置文件config.ini---------
                # TODO
                config = configparser.ConfigParser()
                config.add_section("供应商分布")

                config.set("供应商分布", "起始时间", self.DateTimeEdit_fac_start.text())
                config.set("供应商分布", "结束时间", self.DateTimeEdit_fac_end.text())

                config.add_section("到货后全检（表）")
                config.set("到货后全检（表）", "起始时间", self.DateTimeEdit_meterForm_start.text())
                config.set("到货后全检（表）", "结束时间", self.DateTimeEdit_meterForm_end.text())

                config.add_section("到货后全检（图）")
                config.set("到货后全检（图）", "起始时间", self.DateTimeEdit_meterGraph_start.text())
                config.set("到货后全检（图）", "结束时间", self.DateTimeEdit_meterGraph_end.text())

                config.add_section("全年误差分析")
                config.set("全年误差分析", "起始时间", self.DateTimeEdit_error_start.text())
                config.set("全年误差分析", "结束时间", self.DateTimeEdit_error_end.text())
                config.write(open(r"%s" % ini_path, "w"))
            except:
                traceback.print_exc()
        elif ini_exist == 1:

            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))

                facStartDateTime = config.get("供应商分布", "起始时间")
                facEndDateTime = config.get("供应商分布", "结束时间")
                self.DateTimeEdit_fac_start.setDateTime(QtCore.QDateTime(QtCore.QDate(int(facStartDateTime[0:4]),
                                                                                       int(facStartDateTime[5:7]),
                                                                                       int(facStartDateTime[8:10])),
                                                                          QtCore.QTime(int(facStartDateTime[11:13]),
                                                                                       int(facStartDateTime[14:16]),
                                                                                       int(facStartDateTime[17:]))
                                                                          ))
                self.DateTimeEdit_fac_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(facEndDateTime[0:4]),
                                                                                        int(facEndDateTime[5:7]),
                                                                                        int(facEndDateTime[8:10])),
                                                                           QtCore.QTime(int(facEndDateTime[11:13]),
                                                                                        int(facEndDateTime[14:16]),
                                                                                        int(facEndDateTime[17:]))
                                                                           ))

                meterFormStartDateTime = config.get("到货后全检（表）", "起始时间")
                meterFormEndDateTime = config.get("到货后全检（表）", "结束时间")
                self.DateTimeEdit_meterForm_start.setDateTime(QtCore.QDateTime(QtCore.QDate(int(meterFormStartDateTime[0:4]),
                                                                                        int(meterFormStartDateTime[5:7]),
                                                                                        int(meterFormStartDateTime[8:10])),
                                                                           QtCore.QTime(int(meterFormStartDateTime[11:13]),
                                                                                        int(meterFormStartDateTime[14:16]),
                                                                                        int(meterFormStartDateTime[17:]))
                                                                           ))
                self.DateTimeEdit_meterForm_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(meterFormEndDateTime[0:4]),
                                                                                      int(meterFormEndDateTime[5:7]),
                                                                                      int(meterFormEndDateTime[8:10])),
                                                                         QtCore.QTime(int(meterFormEndDateTime[11:13]),
                                                                                      int(meterFormEndDateTime[14:16]),
                                                                                      int(meterFormEndDateTime[17:]))
                                                                         ))

                meterGraphStartDateTime = config.get("到货后全检（图）", "起始时间")
                meterGraphEndDateTime = config.get("到货后全检（图）", "结束时间")
                self.DateTimeEdit_meterGraph_start.setDateTime(
                    QtCore.QDateTime(QtCore.QDate(int(meterGraphStartDateTime[0:4]),
                                                  int(meterGraphStartDateTime[5:7]),
                                                  int(meterGraphStartDateTime[8:10])),
                                     QtCore.QTime(int(meterGraphStartDateTime[11:13]),
                                                  int(meterGraphStartDateTime[14:16]),
                                                  int(meterGraphStartDateTime[17:]))
                                     ))
                self.DateTimeEdit_meterGraph_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(meterGraphEndDateTime[0:4]),
                                                                                         int(meterGraphEndDateTime[5:7]),
                                                                                         int(meterGraphEndDateTime[
                                                                                             8:10])),
                                                                            QtCore.QTime(
                                                                                int(meterGraphEndDateTime[11:13]),
                                                                                int(meterGraphEndDateTime[14:16]),
                                                                                int(meterGraphEndDateTime[17:]))
                                                                            ))

                errorStartDateTime = config.get("全年误差分析", "起始时间")
                errorEndDateTime = config.get("全年误差分析", "结束时间")
                self.DateTimeEdit_error_start.setDateTime(QtCore.QDateTime(QtCore.QDate(int(errorStartDateTime[0:4]),
                                                                                        int(errorStartDateTime[5:7]),
                                                                                        int(errorStartDateTime[8:10])),
                                                                           QtCore.QTime(int(errorStartDateTime[11:13]),
                                                                                        int(errorStartDateTime[14:16]),
                                                                                        int(errorStartDateTime[17:]))
                                                                           ))
                self.DateTimeEdit_error_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(errorEndDateTime[0:4]),
                                                                                      int(errorEndDateTime[5:7]),
                                                                                      int(errorEndDateTime[8:10])),
                                                                         QtCore.QTime(int(errorEndDateTime[11:13]),
                                                                                      int(errorEndDateTime[14:16]),
                                                                                      int(errorEndDateTime[17:]))
                                                                         ))
            except:
                traceback.print_exc()

        layout_fac = QtWidgets.QVBoxLayout(self.widget_fac)
        self.fig_fac = Figure()
        self.dynamic_canvas_fac = FigureCanvas(self.fig_fac)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_fac.addWidget(NavigationToolbar(self.dynamic_canvas_fac, self))
        layout_fac.addWidget(self.dynamic_canvas_fac)

        self.meterFormList = []

        layout_meterGraph = QtWidgets.QVBoxLayout(self.widget_meterGraph)
        self.fig_meterGraph = Figure()
        self.dynamic_canvas_meterGraph = FigureCanvas(self.fig_meterGraph)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_meterGraph.addWidget(NavigationToolbar(self.dynamic_canvas_meterGraph, self))
        layout_meterGraph.addWidget(self.dynamic_canvas_meterGraph)

        self.errorData = []

    @pyqtSlot()
    def on_pushButton_database_setting_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.database_set.setWindowFlags(Qt.Dialog)
        except Exception as e:
            print(e)
        self.database_set.show()

        self.database_set.signal_connect.connect(self.get_database_setting)
        self.database_set.signal_connect_2.connect(self.get_database_setting2)

    def get_database_setting(self, database_setting):
        self.database_info = database_setting


    def get_database_setting2(self, database_setting):
        self.database_info_old = database_setting


    @pyqtSlot()
    def on_pushButton_fac_clicked(self):
        self.pushButton_fac.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_fac.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\statistics_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
            return
        else:
            # -----改写exiest的数值
            try:
                config.read(r"%s" % ini_path)
                config.set("供应商分布", "起始时间", self.DateTimeEdit_fac_start.text())
                config.set("供应商分布", "结束时间", self.DateTimeEdit_fac_end.text())
                config.write(open(r"%s" % ini_path, "r+"))
            except:
                traceback.print_exc()
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.facThread = threads.facThread()
                self.facThread.setValue(self.database_info, self.database_info_old, self.DateTimeEdit_fac_start.text(), self.DateTimeEdit_fac_end.text())
                self.facThread.signal_facdata.connect(self.fac_exec)
                self.facThread.start()
        except:
            traceback.print_exc()
            self.pushButton_fac.setEnabled(True)
            
    def fac_exec(self, facList, numList):
        self.fig_fac.clf()
        ax = self.fig_fac.add_subplot(111)
        self.fig_fac.tight_layout()
        self.example_pie(ax, facList, numList)
        self.fig_fac.tight_layout()
        self.pushButton_fac.setEnabled(True)

    def example_pie(self, ax, facList, numList, fontsize=12):
        try:
            ax.cla()
            colors = cm.rainbow(np.arange(len(numList))/len(numList))
            explode = [0.01 for i in range(len(numList))]
            wedgeprops = {'linewidth': 0.5, 'edgecolor': 'gray'}
            ax.pie(numList, labels=None, colors=colors, explode=explode,
                   autopct='%3.1f%%', shadow=False,
                   startangle=90, pctdistance=0.8,
                   wedgeprops=wedgeprops)
            # labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
            # autopct，圆里面的文本格式，
            # %3.1f%%表示小数有三位，整数有一位的浮点数
            # shadow，饼是否有阴影
            # startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
            # pctdistance，百分比的text离圆心的距离
            # patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
            num = 0
            for i in numList:
                num += i
            percentList = np.array(numList)*100/num
            legendList = []
            for i in range(len(facList)):
                legendList.append("%s %.1f%%" % (facList[i], percentList[i]))

            # 设置x，y轴刻度一致，这样饼图才能是圆的
            ax.axis('equal')
            ax.legend(legendList)
            ax.figure.canvas.draw()
        except:
            traceback.print_exc()
        
    @pyqtSlot()
    def on_pushButton_meterForm_clicked(self):
        self.pushButton_meterForm.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_meterForm.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\statistics_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
            return
        else:
            # -----改写exiest的数值
            try:
                config.read(r"%s" % ini_path)

                config.set("到货后全检（表）", "起始时间", self.DateTimeEdit_meterForm_start.text())
                config.set("到货后全检（表）", "结束时间", self.DateTimeEdit_meterForm_end.text())
                config.write(open(r"%s" % ini_path, "r+"))
            except:
                traceback.print_exc()

        try:

            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.meterFormThread = threads.meterFormThread()
                self.meterFormThread.setValue(self.database_info, self.database_info_old, self.DateTimeEdit_meterForm_start.text(), self.DateTimeEdit_meterForm_end.text())
                # self.meterFormThread.signal_zerodata.connect(self.zero_exec)
                self.meterFormThread.signal_meterFormdata.connect(self.meterForm_exec)
                self.meterFormThread.start()
        except:
            traceback.print_exc()
            self.pushButton_meterForm.setEnabled(True)


    def meterForm_exec(self, meterFormList):
        try:

            self.tableWidget_meterForm.setColumnCount(len(meterFormList[0]))  # 设置表格的列数
            self.tableWidget_meterForm.setRowCount(len(meterFormList))  # 设置表格的行数
            headerList = ['厂家', '批次数', '总数（只）', '不合格数（只）', '合格率']

            for i in range(len(headerList)):
                    self.tableWidget_meterForm.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                        "%s" % headerList[i]))
            for i in range(len(meterFormList)):
                for j in range(len(meterFormList[0])):
                    if j < 4:
                        item0 = QtWidgets.QTableWidgetItem("%s" % meterFormList[i][j])
                    else:
                        item0 = QtWidgets.QTableWidgetItem("%.3f%%" % float(meterFormList[i][j]*100))
                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_meterForm.setItem(i, j, item0)

            self.tableWidget_meterForm.resizeColumnsToContents()
            self.meterFormList = meterFormList
            self.meterFormList.insert(0, headerList)
            # self.tableWidget_meterForm.itemClicked(QTableWidgetItem=self.tableWidget_meterForm.currentItem()).connect(self.meterForm_clicked)
        except:
            traceback.print_exc()
        self.pushButton_meterForm.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_export_meter_clicked(self):
        self.pushButton_export_meter.setDisabled(True)
        if self.meterFormList == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "无数据！")
            self.pushButton_export_meter.setEnabled(True)
            return

        try:
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
            today = datetime.today()
            today_date = datetime.date(today)

            for i in range(len(self.meterFormList)):
                for j in range(len(self.meterFormList[0])):
                    sheet.write(i, j, self.meterFormList[i][j])
            wbk.save('单相电能表全检合格率'+str(today_date)+'.xls')
            QtWidgets.QMessageBox.information(self, "Information:", "导出成功！")
            self.pushButton_export_meter.setEnabled(True)
        except:
            traceback.print_exc()
            self.pushButton_export_meter.setEnabled(True)


    @pyqtSlot()
    def on_pushButton_meterGraph_clicked(self):
        self.pushButton_meterGraph.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_meterGraph.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\statistics_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
            return
        else:
            # -----改写exiest的数值
            config.read(r"%s" % ini_path)
            config.set("到货后全检（图）", "起始时间", self.DateTimeEdit_meterGraph_start.text())
            config.set("到货后全检（图）", "结束时间", self.DateTimeEdit_meterGraph_end.text())
            config.write(open(r"%s" % ini_path, "r+"))

        try:

            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.meterGraphThread = threads.meterGraphThread()
                self.meterGraphThread.setValue(self.database_info, self.database_info_old, self.DateTimeEdit_meterGraph_start.text(), self.DateTimeEdit_meterGraph_end.text())
                # self.meterGraphThread.signal_zerodata.connect(self.meterGraphzero_exec)
                self.meterGraphThread.signal_meterGraphdata.connect(self.meterGraph_exec)
                self.meterGraphThread.start()
        except:
            traceback.print_exc()
            self.pushButton_meterGraph.setEnabled(True)
            # ---------set datas----------
            # meanlist = []
            # for i in range(60):
            #     for j in range(20):
            #         mean = float(self.alertData[i][j][0])
            #         meanlist.append(mean)
            # threesigma = algorithm.pauta(meanlist)



    def meterGraph_exec(self, meterGraphList):
        self.fig_meterGraph.clf()
        ax = self.fig_meterGraph.add_subplot(111)

        facList = []
        percentList = []
        for i in range(len(meterGraphList)):
            facList.append(meterGraphList[i][0])
            percentList.append(meterGraphList[i][1])
        # self.fig_meterGraph.tight_layout()
        self.example_bar(ax, facList, percentList)
        self.fig_meterGraph.tight_layout()

    def example_bar(self, ax, facList, percentList, fontsize=12):
        try:
            ax.cla()
            n_groups = len(facList)
            for i in range(len(facList)):
                if str(facList[i])[2] == '市':
                    facList[i] = str(facList[i])[3:5]
                else:
                    facList[i] = str(facList[i])[2:4]
            index = np.arange(n_groups)
            percentList = np.array(percentList)*100
            ax.bar(index, percentList, tick_label=facList, facecolor='lightskyblue', edgecolor='black', width=0.5)
            ax.set_ylim(90, 101)
            ax.set_ylabel('合格率', fontsize=fontsize+3)
            ax.set_xticklabels(facList, fontsize=fontsize+2)
            ax.set_yticklabels(['90%', '92%', '94%', '96%', '98%', '100%'], fontsize=fontsize)
            ax.set_title('单相电能表全检合格率', fontsize=fontsize+6)
            for x,y in zip(index, percentList):
                ax.text(x, y+0.5, '%.2f%%'% y, ha='center', fontsize=fontsize)
            ax.figure.canvas.draw()
        except:
            traceback.print_exc()
        self.pushButton_meterGraph.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_error_clicked(self):
        self.pushButton_error.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_error.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\statistics_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
            return
        else:
            # -----改写exiest的数值
            config.read(r"%s" % ini_path)
            config.set("全年误差分析", "起始时间", self.DateTimeEdit_error_start.text())
            config.set("全年误差分析", "结束时间", self.DateTimeEdit_error_end.text())
            config.write(open(r"%s" % ini_path, "r+"))

        try:

            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.errorThread = threads.errorThread()
                self.errorThread.setValue(self.database_info, self.database_info_old,
                                               self.DateTimeEdit_error_start.text(),
                                               self.DateTimeEdit_error_end.text())
                # self.errorThread.signal_zerodata.connect(self.errorzero_exec)
                self.errorThread.signal_errorData.connect(self.error_exec)
                self.errorThread.start()
        except:
            traceback.print_exc()
            self.pushButton_error.setEnabled(True)

    def error_exec(self, errorData):
        try:
            self.tableWidget_error.setColumnCount(len(errorData[0]))  # 设置表格的列数
            self.tableWidget_error.setRowCount(len(errorData))  # 设置表格的行数
            headerList = ['厂家', '检定合格数量（只）',
                          '正误差数量（化整值）', '负误差数量（化整值）', '零误差数量（化整值）',
                          '正误差占比（化整值）', '负误差占比（化整值）', '零误差占比（化整值）',
                          '正误差数量（平均值）', '负误差数量（平均值）', '零误差数量（平均值）',
                          '正误差占比（平均值）', '负误差占比（平均值）', '零误差占比（平均值）']

            for i in range(len(headerList)):
                self.tableWidget_error.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                    "%s" % headerList[i]))
            for i in range(len(errorData)):
                for j in range(len(errorData[0])):
                    if j < 5 or (j >=8 and j < 11) :
                        item0 = QtWidgets.QTableWidgetItem("%s" % errorData[i][j])
                    else:
                        item0 = QtWidgets.QTableWidgetItem("%.3f%%" % float(errorData[i][j] * 100))
                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_error.setItem(i, j, item0)

            self.tableWidget_error.resizeColumnsToContents()
            self.errorData = errorData
            self.errorData.insert(0, headerList)
            # self.tableWidget_meterForm.itemClicked(QTableWidgetItem=self.tableWidget_meterForm.currentItem()).connect(self.meterForm_clicked)
        except:
            traceback.print_exc()
        self.pushButton_error.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_export_error_clicked(self):
        self.pushButton_export_error.setDisabled(True)
        if self.errorData == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "无数据！")
            self.pushButton_export_error.setEnabled(True)
            return
        try:
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
            today = datetime.today()
            today_date = datetime.date(today)

            for i in range(len(self.errorData)):
                for j in range(len(self.errorData[0])):
                    sheet.write(i, j, self.errorData[i][j])
            wbk.save('全年误差分析' + str(today_date) + '.xls')
            QtWidgets.QMessageBox.information(self, "Information:", "导出成功！")
            self.pushButton_export_error.setEnabled(True)
        except:
            traceback.print_exc()
            self.pushButton_export_error.setEnabled(True)

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               "本程序",
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            self.database_set.close()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.setrecursionlimit(1000000)
    sys.exit(app.exec_())

#
# def mycodestart():
#     app = QtWidgets.QApplication(sys.argv)
#     ui = MainWindow()
#     ui.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     import sys, threading
#     sys.setrecursionlimit(100000)
#     threading.stack_size(200000000)
#     thread = threading.Thread(target=mycodestart)
#     thread.start()
