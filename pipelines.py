#!/usr/bin/env python3
from api import get_data
import csv,datetime,os
import datetime

class ProcessCsvFile(object):
    """
    The Class is designed to close read file thread gracefully
    """
    def __init__(self, output_filepath):
        self._output_filepath = output_filepath

    # def close_csv(self):
    #     self._input_object.close()

    def write_csv_header(self, header_list):
        """write csv header with pre-defined content
        Args:
            filename as input
        """
        with open(self._output_filepath, 'w') as f_obj:
            writer = csv.writer(
                f_obj, delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerow(header_list)

    def write_csv(self, content):
        """write a csv file with intended content"""
        with open(self._output_filepath, 'a') as f_obj:

            writer = csv.writer(
                f_obj, delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
                )
            writer.writerow(content)

    def prepare_result_file(self):
        """
            The result file name needs to be calculated on the spot and time-stamped
            on the filename in order to avoid conflict on file name.
        """
        result_filename = 'result_' + str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + '.csv'
        self._output_filepath = os.path.join(self._output_filepath,result_filename)


if __name__ == '__main__':

    url = "https://api.buildkite.com/v2/organizations/myob/pipelines"
    pipelines = get_data(url,100)

    write_csv = ProcessCsvFile('.')
    write_csv.prepare_result_file()
    write_csv.write_csv_header(['slug', 'created_at'])
    for pipe in pipelines:
        write_csv.write_csv([pipe['slug'], pipe['created_at']])
