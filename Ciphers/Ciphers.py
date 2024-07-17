import string


class EncryptionBaseClass:
    alphabet = string.ascii_letters

    def __init__(self, input_str: str):
        self.input_str = input_str
        self._processed = None

    @property
    def processed(self):
        return self._processed


class Rot13(EncryptionBaseClass):
    @property
    def processed(self):
        letter_list = []
        for letter in self.input_str:
            if letter in self.alphabet or letter == ' ':
                if letter != ' ':
                    letter_index = self.alphabet.index(letter)
                    # mod 26 means restart at 0 if the sum is greater than or equal to 26
                    new_letter_index = (letter_index + 13) % 26
                    letter_list.append(self.alphabet[new_letter_index])
                else:
                    letter_list.append(' ')
            elif letter.isdigit():
                letter_list.append(letter)
            else:
                letter_list.append(letter)
        self._processed = ''.join(letter_list)
        return self._processed


class CaesarCipher(EncryptionBaseClass):
    def __init__(self, input_str: str, shift_amount: int):
        super().__init__(input_str)
        self.shift_amount = shift_amount

    @property
    def processed(self, mode: str = 'encrypt'):
        if mode:
            mode = mode.lower()
        else:
            raise AttributeError("Invalid mode, mode must be either \'encrypt\' or \'decrypt\'")

        letter_list = []
        for letter in self.input_str:
            if letter in self.alphabet or letter == ' ':
                if letter != ' ':
                    letter_index = self.alphabet.index(letter)
                    if mode == 'encrypt':
                        # mod 26 means restart at 0 if the sum is greater than or equal to 26
                        new_letter_index = (letter_index + self.shift_amount) % 26
                    elif mode == 'decrypt':
                        # mod 26 means restart at 0 if the sum is greater than or equal to 26
                        new_letter_index = (letter_index - self.shift_amount) % 26
                    else:
                        raise AttributeError("Invalid mode, mode must be either \'encrypt\' or \'decrypt\'")
                    letter_list.append(self.alphabet[new_letter_index])
                else:
                    letter_list.append(' ')
            elif letter.isdigit():
                letter_list.append(letter)
            else:
                letter_list.append(letter)
        self._processed = ''.join(letter_list)
        return self._processed


class VigenereCipher(CaesarCipher):
    def __init__(self, key: str, input_str: str, shift_amount: int = 0):
        super().__init__(input_str, shift_amount)
        self.key = key
        self.mod_number = len(self.key)
        if shift_amount != 0:
           self.shift_amount = 0
        else:
            self.shift_amount = shift_amount
        self._shift_list: list = []
        self.original_input_string = self.input_str

    def GetShiftAmount(self, letter):
        return self.alphabet.index(letter.lower())

    @property
    def processed(self, mode: str = 'encrypted'):
        final_list = []
        for k in self.key:
            if k in self.alphabet:
                self.shift_amount = self.GetShiftAmount(k)
                print(self.shift_amount)
                # FIXME: this will just shift the key itself - this should be a letter from self.original_input_string
                self.input_str = k.lower()
                print(self.input_str, super().processed)#.fget(self))
                final_list.append(super().processed)

            elif k == ' ':
                final_list.append(' ')
            else:
                pass
        self._processed = ''.join(final_list)
        return self._processed


def Rot13_test():
    scrambled = Rot13('Andrew MCSPARROn &').processed
    print(scrambled)
    unscrambled = Rot13(scrambled).processed
    print(unscrambled)


if __name__ == '__main__':
    #Rot13_test()
    #print(CaesarCipher('Andrew', 1).processed)
    print(VigenereCipher('OCULORHINOLARINGOLOGY', 'attacking tonight').processed)