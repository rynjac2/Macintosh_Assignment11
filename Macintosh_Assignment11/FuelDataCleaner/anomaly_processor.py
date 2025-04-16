
class AnomalyProcessor:

    @staticmethod

    def extract_anomalies(rows):

        """

        Separates out the rows where the 'Product' column contains 'Pepsi'

        (case insensitive). Expects `rows` to be a list of dictionaries.

        

        Returns:

            tuple: (clean_rows, anomalies) where:

                - clean_rows: rows where 'Product' does not contain Pepsi.

                - anomalies: rows where 'Product' contains Pepsi.

        """

        anomalies = []

        clean_rows = []

        for row in rows:

            # Use get() to safely retrieve the 'Product' value from each row.

            product = row.get("Product", "")

            if "pepsi" in product.lower():

                anomalies.append(row)

            else:

                clean_rows.append(row)

        return clean_rows, anomalies