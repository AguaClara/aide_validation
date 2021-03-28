"""Helper functions for validating LFOM.
Created on January 6, 2021

@author: fchapin@aguaclarareach.org
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from fpdf import FPDF


class ReportWriter(object):
    """Class to write validation results to a report file"""

    def __init__(self):
        if not os.path.exists("Reports"):
            os.mkdir("Reports")
        now = datetime.now()
        str_now = now.strftime("%Y.%m.%d.%H.%M.%S")
        self.report_name = "Reports/Validation_Report_" + str_now + ".txt"
        self.report_file = open(self.report_name, "x+")
        self.report_file.write("AIDE Validation Report\n")
        self.result = "Valid"
        self.plot_graph = None
        self.r_squared = None

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

    def add_r2_plot(self, x_values, y_values, x_type, y_type):
        """

        Args:
            x_values: a list of values passed to compare with y to get correlation

            y_values: a list of values passed to compare with x to get correlation

            x_type: a string to describe the x_values

            y_type: a string to describe the y_values
        """
        r2 = np.corrcoef(x_values.magnitude, y_values.magnitude)[0, 1]**2
        self.r_squared = "The R^2 between the " + x_type + " and " + y_type + " is " + str(r2) + "."
        plt.plot(x_values, y_values)
        plt.xlabel(x_type)
        plt.ylabel(y_type)

        self.plot_graph = ".".join(self.report_name.split(".")[:-1] + ["png"])
        plt.savefig(self.plot_graph)

    def to_pdf(self, file_name=None, output_path=None, plot_path=None):
        """Convert report file to PDF

        Args:
            file_name: path to file to be converted. Defaults to None
                which uses report_name associated with this ReportWriter object

            output_path: path to output file. Defaults to None which replaces .txt
                in report_name associated with this ReportWriter object with .pdf

            plot_path: path of image to be added onto the pdf. Default to None
                which uses the plot_graph path associated with this ReportWriter
                object

        Returns:
            none

        """
        if file_name is None:
            file_name = self.report_name

        file = open(file_name, "r")

        if output_path is None:
            output_path = ".".join(self.report_name.split(".")[:-1] + ["pdf"])

        if plot_path is None:
            plot_path = self.plot_graph

        pdf = FPDF()
        # add a page and set font
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        # insert the lines in pdf then save
        for x in file:
            pdf.multi_cell(0, 5, txt=x, align="L")

        if plot_path is not None:
            pdf.image(plot_path, w=200)
            if self.r_squared is not None:
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, txt=self.r_squared, align="C")

        pdf.output(output_path)

    def close(self):
        """Closes the report file associated with this ReportWriter

        Args:
            none

        Returns:
            none
        """
        self.report_file.close()
