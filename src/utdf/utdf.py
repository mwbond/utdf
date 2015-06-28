# Matthew Bond
# A class for working with UTDF (Universal Traffic Data Format) files


class UTDF():
    UTDF_VERSION = '8'

    def __init__(self, db_path, attributes):
        self.db = db_path
        self.attributes = attributes

    def correct_version(self, version=UTDF_VERSION):
        return version == self.attributes['UTDFVERSION']
