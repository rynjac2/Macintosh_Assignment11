# File Name : csv_handler.py
# Student Name: Ryan Jacob
# email:  Jacobry@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:  4/17/2025
# Course #/Section:  IS4010-002
# Semester/Year:  Spring 2025
# Brief Description of the assignment: To clean and update fuel data
# Brief Description of this module: csv_processor class which contains 4 methods for cleaning and updating the data
# Citations: https://chatgpt.com/, https://www.reddit.com/r/learnpython/comments/7wff25/splitting_a_singleline_address_into_its/, https://stackoverflow.com/questions/77643433/processing-large-csv-file-in-python



import csv
import os
import requests
import re


class csv_processor():
    def read_csv(self, file_path):
        """ 
           Loads data from a CSV file containing column headers, 
           converting each row into a dictionary keyed by header names. 
           All rows are returned as a list of these dictionaries.

           Args: file_path (str): Location of the CSV file to be read.

           Returns: list: List of row data as dictionaries keyed by column names. 
           Returns an empty list if the file is empty or if an error occurs during reading. 
        """
          
        data = []
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                data.append(row)

        return data



    def roundGrossPrice(self, data):
        """
        Formats numerical entries in the third column of each dictionary within a list by rounding them to two decimal places.

        Args:
            data (list): A list containing dictionaries, each representing a row from a CSV file with headers.

        Returns:
            list: The updated list with third-column values rounded totwo decimal places.
        """
        if not data:
            return []

        headers = list(data[0].keys())
        price_header = headers[2]

        print(f"Rounding prices in column '{price_header}' to two decimal places.")

        for row in data:

                value = float(row[price_header])
                row[price_header] = "{:.2f}".format(value)

        return data
        


    def duplicateDetector(self, data):
        """
        Filters out duplicate entries from a list of dictionaries, excluding consideration of the first column.
        Rows are treated as duplicates if all their values, except the first column, match exactly.

        Args:
            data (list): A list containing dictionaries, each representing a row from a CSV file.

        Returns:
            list: The original list with duplicates removed, based on comparison of all columns except the first.
        """
        if not data:
            return []

        headers = list(data[0].keys())  # Obtain headers to identify column positions
        new = set()  # Used to store unique rows based on values excluding the first column
        valid_data = []

        print("Duplicate rows removed.")
        # Iterate through rows to identify and exclude duplicates
        for row in data:
            # Create a tuple of values from the row, omitting the first column
            row_signature = tuple((key, row[key]) for key in headers[1:])

            # Add row to valid_data if its signature hasn't been encountered yet
            if row_signature not in new:
                valid_data.append(row)
                new.add(row_signature)

        return valid_data



    def removePepsi(self, data, phrase="Pepsi"):

        """
        Removes rows containing the specified phrase (default "Pepsi") in the 6th column,
        saving these removed rows to 'Data/dataAnomalies.csv'.

        Args:
            data (list): A list of dictionaries, each representing a row.
            phrase (str): Phrase to identify anomalies (default: "Pepsi").

        Returns:
            list: The original data excluding rows marked as anomalies.
        """

        if not data:
            return []

        # Ensure Data directory exists
        os.makedirs('Data', exist_ok=True)

        headers = data[0].keys() if data else []
        anomaly_data, valid_data = [], []

        for row in data:
            column_values = list(row.values())
            if len(column_values) >= 6 and phrase in column_values[5]:
                anomaly_data.append(row)
            else:
                valid_data.append(row)
        
        print(" 'Pepsi' anomalies removed.")

        # Save anomalies if any found
        if anomaly_data:
            with open('Data/dataAnomalies.csv', 'w', newline='', encoding='utf-8') as anomaly_file:
                writer = csv.DictWriter(anomaly_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(anomaly_data)
        else:
            print("No anomalies found.")

        return valid_data


    def zipcodeEditor(self, data, api_key):
        """ 
        Updates missing ZIP codes in addresses (found in the 4th column) by fetching them from the Zipcodebase API,
        based on provided city and state details. Limits updates to the first 5 addresses that lack ZIP codes.
        The finalized dataset is then saved to Data/cleanedData.csv.

        Args:
            data (list): List of dictionaries, each representing a data row.
            api_key (str): Zipcodebase API key.

        Returns:
            list: Updated dataset including added ZIP codes for up to 5 entries.
        """
        print("Zipcodes added to addresses not containing one.")
        if not data:
            return []

        headers = list(data[0].keys())
        address = headers[3]  # Column containing the addresses
        zip_cache = {}  # Cache to store fetched ZIP codes for city/state combinations
        count = 0  # Counter for how many addresses have been updated
        maxFill = 5  # Maximum number of addresses to update

        for row in data:
            if count >= maxFill:
                break

            full_address = row.get(address, '').strip()

            # Skip addresses that already contain ZIP codes
            if re.search(r'\b\d{5}(?:-\d{4})?\b', full_address):
                continue

            # Extract city and state from address
            section = full_address.split(',')
            if len(section) >= 2:
                city = section[-2].strip()
                state = section[-1].strip()[:2].upper()

                if city and state:
                    key = f"{city},{state}"

                    # Check cache first before API call
                    if key in zip_cache:
                        zip_code = zip_cache[key]
                        row[address] = f"{full_address} {zip_code}"
                        count += 1
                        continue

                    # Make API call to fetch ZIP code
                    try:
                        url = f"https://app.zipcodebase.com/api/v1/code/city?apikey={api_key}&city={city}&country=us"
                        response = requests.get(url)
                        if response.status_code == 200:
                            result = response.json()
                            zip_codes = result.get("results", [])

                            if zip_codes:
                                zip_code = zip_codes[0]
                                zip_cache[key] = zip_code
                                row[address] = f"{full_address} {zip_code}"
                                count += 1

                    except Exception:
                        # Silently handle API exceptions
                        pass

        # Save the fully updated dataset to a CSV file
        os.makedirs('Data', exist_ok=True)
        with open('Data/cleanedData.csv', 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        return data