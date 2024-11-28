class BBAnalysisError(Exception):
    """Base exception for all brightbeam_analysis errors."""

    pass


class DataValidationError(BBAnalysisError):
    """Raised when data validation fails."""

    pass


class FileParsingError(BBAnalysisError):
    """Raised when file parsing fails."""

    pass


class AnalysisError(BBAnalysisError):
    """Raised when analysis calculations fail."""

    pass


class InsufficientDataError(BBAnalysisError):
    """Raised when there's not enough data for meaningful analysis."""

    pass
