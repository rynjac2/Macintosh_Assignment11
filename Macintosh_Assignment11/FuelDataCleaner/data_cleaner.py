class DataCleaner:

    @staticmethod

    def clean_data(rows):

        # Format "Gross Price" to exactly 2 decimals.

        for row in rows:

            if "Gross Price" in row and row["Gross Price"]:

                try:

                    row["Gross Price"] = f"{float(row['Gross Price']):.2f}"

                except ValueError:

                    # If conversion fails, leave the original value.

                    pass

        

        # Remove duplicate rows.

        seen = set()

        unique_rows = []

        for row in rows:

            # Create a tuple representation of the row.

            row_tuple = tuple(sorted(row.items()))

            if row_tuple not in seen:

                seen.add(row_tuple)

                unique_rows.append(row)

        return unique_rows
