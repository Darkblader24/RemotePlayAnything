import ntpath
import traceback

import win32api
from PyQt5.QtWidgets import QMessageBox


def show_error(title="An error has occurred!", text="Task failed successfully", details=True):
    message_box = QMessageBox(QMessageBox.Critical, str(title), str(text))
    if details:
        error = str(traceback.format_exc())
        print(error)
        message_box.setDetailedText(error)
    else:
        print(title, text)
    message_box.exec_()


def get_file_name(path):
    file_name = None
    prop_name = 'ProductName'

    if path.endswith(".exe"):
        try:
            # \VarFileInfo\Translation returns list of available (language, codepage)
            # pairs that can be used to retrieve string info. We are using only the first pair.
            lang, codepage = win32api.GetFileVersionInfo(path, '\\VarFileInfo\\Translation')[0]

            str_info_path = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, prop_name)
            file_name = win32api.GetFileVersionInfo(path, str_info_path)
        except Exception as e:
            print(e)

    return file_name if file_name else ntpath.split(path)[1]


def get_file_properties(fname):
    """
    Read all properties of the given file return them as a dictionary.
    """
    prop_names = ('Comments', 'InternalName', 'ProductName',
                  'CompanyName', 'LegalCopyright', 'ProductVersion',
                  'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                  'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixed_info = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixed_info
        props['FileVersion'] = "%d.%d.%d.%d" % (fixed_info['FileVersionMS'] / 65536,
                                                fixed_info['FileVersionMS'] % 65536,
                                                fixed_info['FileVersionLS'] / 65536,
                                                fixed_info['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        str_info = {}
        for propName in prop_names:
            str_info_path = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            str_info[propName] = win32api.GetFileVersionInfo(fname, str_info_path)

        props['StringFileInfo'] = str_info
    except:
        pass

    return props
