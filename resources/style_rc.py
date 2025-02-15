# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.6.3
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xc3\
[\
Controls]\x0d\x0aStyle\
 = Material\x0d\x0a\x0d\x0a[\
Material]\x0d\x0aVaria\
nce = Dark\x0d\x0aPrim\
ary = #0D1B2A\x0d\x0aA\
ccent = #7FDBCA\x0d\
\x0aForeground = #E\
1E1E6\x0d\x0aBackgroun\
d = #1B263B\x0d\x0a\x0d\x0a[\
Material/Font]\x0d\x0a\
Family = Calibri\
\x0d\x0aPixelSize = 20\
\x0d\x0a\
"

qt_resource_name = b"\
\x00\x0b\
\x09\xb0d\x86\
\x00c\
\x00o\x00l\x00o\x00r\x00s\x00.\x00c\x00o\x00n\x00f\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8f\x87\xfcD\xfe\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
