from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np


class DataArrange():
    def __init__(self, data):
        self.data = data
        self.HUM = {}
        self.GR = {}
        self.PSI = {}
        self.TMP = {}

    # "GR": "80.00337376508344",
    # "HUM": "20.109",
    # "PSI": "965.26",
    # "TMP": "27.4",
    # "TS": "1614496264"
    def get_data(self):
        for row in self.data:
            ts = self.get_ts(row)
            self.HUM[ts] = "{:.2f}".format(float(row['HUM']))
            self.GR[ts] = "{:.2f}".format(float(row['GR']))
            self.PSI[ts] = "{:.2f}".format(float(row['PSI']))
            self.TMP[ts] = "{:.2f}".format(float(row['TMP']))

    def get_ts(self, row):
        return datetime.fromtimestamp(int(row["TS"]))
