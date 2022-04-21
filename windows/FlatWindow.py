from dis import dis
from sys import flags
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from models import Market, Flat


class FlatWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        # self.fillTable()

    def onAdd(self):
        market = Market.get_by_id(self.cbb_market.currentData())

        flat = Flat(self.le_flat.text(), market.id)
        flat.save()

        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)
        self.table.setItem(row_count, 0,
                           QTableWidgetItem(str(market.id)))
        self.table.setItem(row_count, 1,
                           QTableWidgetItem(str(market.name)))
        self.table.setItem(row_count, 2,
                           QTableWidgetItem(str(flat.id)))
        self.table.setItem(row_count, 3,
                           QTableWidgetItem(str(flat.name)))

    def onUpd(self):
        flat_name = self.le_flat.text()
        mar_id = self.cbb_market.currentData()
        flat_id = int(self.table.item(self.sel_row, 2).text())

        flat = Flat(flat_name, mar_id, flat_id)
        flat.save()

        self.fillTable()

    def onDel(self):
        flat_name = self.le_flat.text()
        mar_id = self.cbb_market.currentData()
        flat_id = int(self.table.item(self.sel_row, 2).text())

        flat = Flat(flat_name, mar_id, flat_id)
        flat.delete()

        self.fillTable()

    def onClicked(self):
        self.sel_row = self.table.currentRow()
        flat_name = self.table.item(self.sel_row, 3).text()
        self.le_flat.setText(flat_name)

    def initUI(self):

        self.setGeometry(200, 200, 680, 400)
        self.resize(680, 400)

        self.qlb_market = QLabel("market", self)
        self.qlb_market.move(30, 30)

        self.cbb_market = QComboBox(self)
        self.cbb_market.move(80, 30)

        self.qlb_flat = QLabel("flatrict name", self)
        self.qlb_flat.move(280, 30)

        self.le_flat = QLineEdit(self)
        self.le_flat.move(380, 30)

        self.btn_add = QPushButton("Add", self)
        self.btn_add.move(530, 30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_upd = QPushButton("Update", self)
        self.btn_upd.move(530, 60)
        self.btn_upd.clicked.connect(self.onUpd)

        self.btn_del = QPushButton("Delete", self)
        self.btn_del.move(530, 90)
        self.btn_del.clicked.connect(self.onDel)

        self.table = QTableWidget(self)
        self.table.setGeometry(30, 60, 480, 300)
        self.table.setColumnCount(4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.clicked.connect(self.onClicked)

        self.cbb_market.currentIndexChanged.connect(self.fillTable)
        for mar in Market.objects():
            self.cbb_market.addItem(mar.name, mar.id)

    def fillTable(self):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(
            ["Mar id", 'Market name', 'flat id', 'Flat name'])
        self.table.setRowCount(0)
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        current_id = self.cbb_market.currentData()
        for flat in Flat.objects():
            flat.marketId
            if current_id == flat.marketId:
                market = flat.market
                row_count = self.table.rowCount()
                self.table.setRowCount(row_count + 1)
                self.table.setItem(row_count, 0,
                                   QTableWidgetItem(str(market.id)))
                self.table.setItem(row_count, 1,
                                   QTableWidgetItem(str(market.name)))
                self.table.setItem(row_count, 2,
                                   QTableWidgetItem(str(flat.id)))
                self.table.setItem(row_count, 3,
                                   QTableWidgetItem(str(flat.name)))
        self.table.resizeColumnsToContents()
