import re

import requests



class ZipCodeUpdater:

    ZIPCODE_REGEX = re.compile(r'\b\d{5}\b')

    API_URL = "https://app.zipcodebase.com/api/v1/search"

    API_KEY = "cb0ff6c0-1608-11f0-823a-c3e5554fbab9"

    

    @staticmethod

    def get_zipcode_for_city(city):

        """

        Uses the Zipcodebase API to fetch a valid zipcode for the given city.

        Returns a zipcode as a string, or "00000" if the API call fails.

        """

        params = {"city": city}

        headers = {"apikey": ZipCodeUpdater.API_KEY}

        try:

            response = requests.get(ZipCodeUpdater.API_URL, params=params, headers=headers)

            response.raise_for_status()

            data = response.json()

            # Assuming the API returns a JSON structure like:

            # { "results": { "zipcode1": {...}, "zipcode2": {...}, ... } }

            results = data.get("results", {})

            if results:

                # Choose the first zipcode from the results.

                zipcode = list(results.keys())[0]

                return zipcode

        except Exception as e:

            print(f"API error for city '{city}': {e}")

        

        return "00000"  # Default zipcode if API fails

    

    @staticmethod

    def update_missing_zipcodes(rows, address_col="Address", max_updates=5):

        """

        For each row, if the address in the provided column does not contain a 5?digit zipcode,

        update it by appending a zipcode (retrieved from the API) to the address.

        Only the first max_updates rows missing a zipcode will be updated.

        """

        updated_count = 0

        

        for row in rows:

            # Check if we've already updated the maximum number of addresses.

            if updated_count >= max_updates:

                break

            

            if address_col not in row:

                continue

            

            address = row[address_col]

            if ZipCodeUpdater.ZIPCODE_REGEX.search(address):

                continue  # Skip if the address already has a zipcode

            

            # Attempt to extract the city assuming the format "Street, City, State".

            parts = address.split(",")

            if len(parts) >= 2:

                city = parts[-2].strip()

            else:

                city = address.strip()

            

            zipcode = ZipCodeUpdater.get_zipcode_for_city(city)

            new_address = address.strip() + ", " + zipcode

            row[address_col] = new_address

            

            updated_count += 1

        

        return rows
