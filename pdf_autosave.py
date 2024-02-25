import pandas
import os
import mysql.connector

class PDF_autosave:
    def auto_save(dest, data):

        if dest == "csv":
            dataFrame = pandas.DataFrame(data)

            csv_file_path = 'database.csv'

            if not os.path.exists(csv_file_path):
                # make id for each pdf
                dataFrame.index.name = "id"
                dataFrame.index = 'F' + (dataFrame.index + 1).astype(str).str.zfill(5)
                dataFrame.to_csv(csv_file_path, index=True, header=True)

            else:
                # if csv exist, then append
                existing_df = pandas.read_csv(csv_file_path)
                last_index = existing_df.index.max()
                dataFrame.index = 'F' + (dataFrame.index + last_index + 2).astype(str).str.zfill(5)
                dataFrame.to_csv(csv_file_path, index=True, mode='a', header=False)

            print("Insertion successful")

        elif dest == "sql":
            _db_context = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_test"
            )

            cursor = _db_context.cursor()

            temp_name = str(data["file_name"][0])
            temp_content = str(data["file_content"][0])
            
            cursor.execute("INSERT INTO ms_file (file_name, file_content) VALUES (%s, %s)", (temp_name, temp_content))
            _db_context.commit() 
            print("Insertion successful")

            cursor.close()
            _db_context.close()