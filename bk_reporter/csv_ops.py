import os
import csv
import datetime


class ProcessCsvFile(object):
    """
    The Class is designed to close read file thread gracefully
    """

    def __init__(self, output_filepath):
        self._output_filepath = output_filepath

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

    def prepare_result_file(self, filename="result"):
        """
            The result file name needs to be calculated on the spot and time
            stamped on the filename in order to avoid conflict on file name.
        """
        result_filename = filename + '_' + str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + '.csv'
        self._output_filepath = os.path.join(
            self._output_filepath,
            result_filename
            )

    def write_csv(self, content):
        """
            write a csv file with intended content in format: [value1, value2]
        """
        with open(self._output_filepath, 'a') as f_obj:

            writer = csv.writer(
                f_obj, delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
                )
            writer.writerow(content)

    def generate_csv(self, header, dict_keys, content, filename="result"):
        """
            This func wraps sub-funcs [
                prepare_result_file,
                write_csv_header,
                write_csv]
            - create new file with the given filename at given path
            - write header
            - write csv rows
        """
        pass
