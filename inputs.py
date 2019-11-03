class Inputs:
    def __init__(self):
        self.rangeStart = None
        self.rangeEnd = None

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        self._filePath = filePath

    @property
    def stockName(self):
        return self._stockName

    @stockName.setter
    def stockName(self, stockName):
        self._stockName = stockName

    @property
    def startDate(self):
        return self._startDate

    @startDate.setter
    def startDate(self, startDate):
        self._startDate = startDate

    @property
    def endDate(self):
        return self._endDate

    @endDate.setter
    def endDate(self, endDate):
        self._endDate = endDate

    def resetInputData(self):
        self._filePath = ''
        self._stockName = ''
        self._startDate = ''
        self._endDate = ''
