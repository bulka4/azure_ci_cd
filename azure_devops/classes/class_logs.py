"""
Class for creating a file with logs about created and deleted resources.
"""

from datetime import datetime
import pandas as pd
import os

class Logs:
    def __init__(
        self
        ,logs_folder_path = 'logs'
        ,logs_file_name = 'logs' # file name without the file extension. There will be automatically added csv extension.
    ):
        self.logs_file_path = os.path.join(logs_folder_path, logs_file_name + '.csv')

        if not os.path.exists(logs_folder_path):
            os.makedirs(logs_folder_path)
            self.logs = pd.DataFrame()
        elif not os.path.exists(self.logs_file_path):
            self.logs = pd.DataFrame()
        else:
            self.logs = pd.read_csv(self.logs_file_path, index_col = 0)


    def add_logs(
        self
        ,new_logs
    ):
        """
        The new_logs argument is a dataframe with new records which should be added to logs. They should not
        contain the 'date' column, it will be added here so it have the correct format.
        """
        date = datetime.now().strftime("%Y-%m-%d_%H:%M")
        new_logs['date'] = date

        self.logs = pd.concat((self.logs, new_logs), axis = 0)

    
    def save_logs(
        self
    ):
        self.logs.to_csv(self.logs_file_path)