class WrongColumnName(Exception):
    def __init__(self, column_name):
        self.column_name = column_name
        self.message = f"Wrong column name: {self.column_name}"
        super().__init__(self.message)
        