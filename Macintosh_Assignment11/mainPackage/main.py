from FuelDataCleaner.anomaly_processor import*

from FuelDataCleaner.data_cleaner import*

from FuelDataCleaner.csv_handler import*

from FuelDataCleaner.zipcode_updater import*



def main():

    # Define file paths.

    input_csv = "Data/fuel_purchases.csv"       # Input CSV file

    cleaned_csv = "Data/cleanedData.CSV"          # Output file for cleaned data

    anomalies_csv = "Data/dataAnomalies.CSV"      # Output file for anomalies

    

    # Read the CSV into a list of dictionaries along with the header.

    rows, header = CSVHandler.read_csv(input_csv)

    

    # Clean up the data: format Gross Price and remove duplicate rows.

    rows = DataCleaner.clean_data(rows)

    

    # Extract anomalies (rows where drivers purchased Pepsi).

    rows, anomalies = AnomalyProcessor.extract_anomalies(rows)

    if anomalies:

        CSVHandler.write_csv(anomalies_csv, anomalies, header)

        print(f"Wrote anomalies to {anomalies_csv}")

    else:

        print("No anomalies found.")

    

    # Update addresses missing a zipcode.

    rows = ZipCodeUpdater.update_missing_zipcodes(rows, address_col="Address")

    

    # Write the cleaned-up data to a new CSV file.

    CSVHandler.write_csv(cleaned_csv, rows, header)

    print(f"Cleaned data written to {cleaned_csv}")



if __name__ == "__main__":

    main()
