import pandas as pd
from urllib.parse import urlparse

class util:
    def read_excel_to_list(self, file_path):
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        # Convert the single column to a list
        # Assuming the column name is 'Column1'; adjust as needed
        data_list = df.iloc[:, 0].tolist()
        return data_list

    def get_next_path_segment(self, url):
        # Parse the URL
        parsed_url = urlparse(url)

        # Get the path from the URL
        path = parsed_url.path

        # Split the path into segments
        path_segments = path.strip('/').split('/')
        # Check if there's a next segment
        if len(path_segments) >= 1:
            return path_segments[0]
        else:
            return ''



    def __init__(self):
        file_path = 'tatasteel.xlsx'
        data_list = self.read_excel_to_list(file_path)
        path = set()
        for url in data_list:
            next_segment = self.get_next_path_segment(url)
            path.add(next_segment)
        search = ['report', 'invest', 'relation']
        useful = set()
        for url in data_list:
            for sear in search:
                if sear in url and 'media' not in url:
                    useful.add(url)
        for url in useful:
            print(url)
