"""Helper functions for validating LFOM.
Created on January 6, 2021

@author: fchapin@aguaclarareach.org
"""

import os
from datetime import datetime

class ReportWriter(object):
    """Class to write validation results to a report file"""
    def __init__(self):
        if not os.path.exists('Reports'):
            os.mkdir('Reports')
        now = datetime.now()
        str_now = now.strftime('%m.%d.%Y.%H.%M.%S')
        self.report_name = 'Reports/Validation_Report_' + str_now + '.txt'
        self.report_file = open(self.report_name, 'x')
        self.report_file.write('AIDE Validation Report\n')
        self.result = 'Valid'

    def set_result(self, msg):
        """Write the given text to the report file

        Args:
            msg: string of text which represents validation result

        Returns:
            none
        """
        self.result = msg

    def get_result(self):
        """Write the given text to the report file

        Args:
            none

        Returns:
            result: string of text which represents validation result
        """
        return self.result


    def write_message(self, msg):
        """Write the given text to the report file

        Args:
            msg: string of text to add to the report file

        Returns:
            none
        """
        self.report_file.write(msg)

    def close(self):
        """Closes the report file associated with this ReportWriter

        Args:
            none

        Returns:
            none
        """
        self.report_file.close()
