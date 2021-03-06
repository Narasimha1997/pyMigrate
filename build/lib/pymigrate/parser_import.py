import re


class Parser:

    def __init__(self):
        self.from_stmt = r'^from (.*) import'
        self.import_stmt = r'^import (.*)'

    def parse(self, text):
        includes = []
        for line in text:
            matched = re.findall(self.from_stmt, line)
            if len(matched) > 0 and '.' in matched[0]:
                includes = includes + [matched[0].split(".")[0]]
            else:
                includes += matched
            # while checking imports, make sure multiple includes are handled:
            matched = re.findall(self.import_stmt, line)
            if len(matched) > 0 and ',' in matched[0]:
                new_tok = [token.strip() for token in matched[0].split(",")]
                includes = includes + new_tok
            else:
                includes += matched
        return includes
