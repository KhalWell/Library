from abc import ABC, abstractmethod

import pandas as pd


class AbstractParser(ABC):

    @staticmethod
    @abstractmethod
    def pars_file(*args, **kwargs):
        pass


class BaseParser(AbstractParser):

    def pars_file(*args, **kwargs):
        try:
            data = pd.read_csv(*args, **kwargs)
            return data
        except Exception:
            return []

    @staticmethod
    def to_json(data, *args, **kwargs):
        return data.to_dict(*args, **kwargs)
