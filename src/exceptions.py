class WrongColumnName(Exception):
    """ this exception is raised when the column name is not in the dataframe columns inside the transformer

    Args:
        Exception (Exception): the base class for all exceptions 
    """
    def __init__(self, column_name):
        self.column_name = column_name
        self.message = f"Wrong column name: {self.column_name}"
        super().__init__(self.message)
        