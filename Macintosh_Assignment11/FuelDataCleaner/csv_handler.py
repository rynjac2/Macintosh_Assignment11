
import csv



class CSVHandler:

    @staticmethod

    def read_csv(file_path):

        """

        Reads a CSV file and returns a tuple (data, header) where

        data is a list of dictionaries and header is a list of column names.

        """

        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            header = reader.fieldnames

            data = [row for row in reader]

        return data, header



    @staticmethod

    def write_csv(file_path, data, header):

        """

        Writes a list of dictionaries to a CSV file with the given header.

        """

        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=header)

            writer.writeheader()

            for row in data:

                writer.writerow(row)