class ExcelProcessorError(Exception):
    pass

class DataValidationError(ExcelProcessorError):
    pass

class FileNotFoundError(ExcelProcessorError):
    pass

class ChartCreationError(ExcelProcessorError):
    pass

class DataProcessingError(ExcelProcessorError):
    pass

class EmptyDataError(DataValidationError):
    pass

class MissingColumnsError(DataValidationError):
    pass