# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop

class DbConnection(object):
    """Reads in datas for personal database connection."""
    @staticmethod
    def open_file(file_name):
        with open(file_name, "r") as f:
            data_line = f.readlines()
            return data_line

