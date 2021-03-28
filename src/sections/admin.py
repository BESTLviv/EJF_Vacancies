from ..data import Data
from .section import Section

class Admin(Section):

    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call):
        pass

    def process_text(self, text):
        pass