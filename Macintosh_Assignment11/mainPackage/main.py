# File Name : main.py
# Student Name: Cole Crooks
# email:  crookscl@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:  4/17/2025
# Course #/Section:  IS4010-002
# Semester/Year:  Spring 2025
# Brief Description of the assignment: To clean and update fuel data
# Brief Description of this module: csv_processor class which contains 4 methods for cleaning and updating the data
# Citations: https://chatgpt.com/


from FuelDataCleaner.csv_handler import *

# Main execution block
if __name__ == "__main__":

    # Initialize CSV processing class
    csv = csv_processor()

    # Read data from the fuel purchase CSV file
    data_list = csv.read_csv("Data/fuelPurchaseData.csv")

    # Round gross prices in the data to two decimal places
    rounded_data = csv.roundGrossPrice(data_list)

    # Remove duplicate entries from the dataset
    duplicate_data = csv.duplicateDetector(rounded_data)

    # Remove rows containing 'Pepsi' anomalies from the dataset
    remove_pepsi = csv.removePepsi(duplicate_data)

    # Update addresses missing ZIP codes using the Zipcodebase API
    zip_codes = csv.zipcodeEditor(remove_pepsi, "cb0ff6c0-1608-11f0-823a-c3e5554fbab9")





    