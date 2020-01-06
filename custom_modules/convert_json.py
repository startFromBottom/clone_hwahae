import json


class JsonAlreadyConvertedException(Exception):
    pass


class ConvertJsonFormat:
    @staticmethod
    def _convert_format_to_db(path: str, model: str):
        """
        convert json format to insert database

        :param path: json file path
        :param model: appname.modelname
        
        """
        with open("path") as f:
            json_data = json_load(f)

        for each in json_data.get("data"):
            insert_row = {}
            insert_row["models"] = model
            insert_row["fields"] = each
