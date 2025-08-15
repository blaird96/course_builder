import pathlib
# services/__init__.py
from .local.local_scaffold import LocalScaffold
from .google.drive_service import DriveService
from .google.calendar_service import CalendarService    
# Ensure the services package is recognized as a module
__path__ = [str(pathlib.Path(__file__).parent.resolve())]   
__all__ = [
    'LocalScaffold',
    'DriveService',
    'CalendarService'
]