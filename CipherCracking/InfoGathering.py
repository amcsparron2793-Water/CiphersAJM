import string

# this MIGHT be a playfair cipher?
candidate_string = """
H26JR-CFFDQ-C2QWX-KG7XP-TWV7Z
HF6QG-Y72KY-26VPM-7P2GY-QHX2Z
9442X-CXMHY-Y4WXJ-QDYYG-6G2TZ
Z9IEZ-N7MEE-64L3Y
XERKL-4ZMXK-X6GC9
SRCS-6565-MHTLH-BV6H-LBJQ
PH4B-36HF-LTDQK-J6QC-J6HV
ANNP-75PT-RDBC
5MCC-JQX7-KC59
AM4A-GJG7-EFL5
"""


class CipherCrackingBase:
    alphabet = string.ascii_letters

    def __init__(self, input_str: str):
        self.input_str = input_str
        self._letter_count = {}
        self.word_separator = '-'
        self.line_separator = '\n'

    @property
    def sym_count(self) -> dict:
        for char in self.input_str:
            if char != self.word_separator and char != self.line_separator:
                self._letter_count[char] = self.input_str.count(char)
        return self._letter_count

    @property
    def most_common_symbol(self):
        return [x for x in self.sym_count.items() if x[1] == max(self.sym_count.values())]


if __name__ == '__main__':
    ccb = CipherCrackingBase(candidate_string)