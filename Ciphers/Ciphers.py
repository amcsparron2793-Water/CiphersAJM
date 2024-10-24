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
                print(self.input_str, super().processed)  #.fget(self))
                final_list.append(super().processed)

            elif k == ' ':
                final_list.append(' ')
            else:
                pass
        self._processed = ''.join(final_list)
        return self._processed


class PlayfairCipher(EncryptionBaseClass):
    """
    Class to implement the Playfair cipher encryption algorithm.

    The PlayfairCipher class inherits from EncryptionBaseClass and is used for encrypting text
    using the Playfair cipher technique.

    - Alphabet: A string containing the lowercase alphabet excluding the letter 'j'.
    - Key: The encryption key provided by the user, converted to lowercase with 'j' replaced by 'i'.
    - Key Matrix: A 5x5 matrix generated based on the key provided and the alphabet.
    - Processed: A property that returns the encrypted plaintext using the Playfair cipher.
    - Preprocess Text: Method to preprocess the input text by converting to lowercase, replacing 'j' with 'i',
        and removing spaces. Inserts 'x' between duplicate letters and ensures even length.
    - Generate Key Matrix: Method to generate the key matrix used for encryption.
    - Find Position: Method to find the row and column position of a character within the key matrix.
    - Encrypt Pair: Method to encrypt a pair of characters using the Playfair cipher technique.
    - Encrypt Plaintext: Method to encrypt the preprocessed text using the Playfair cipher.
    - Display Key Matrix: Method to display the key matrix in a 5x5 grid format.
    """
    alphabet = string.ascii_lowercase.replace('j', '')
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'
    MODES = [ENCRYPT, DECRYPT]

    def __init__(self, key, input_str: str, mode='encrypt'):
        super().__init__(input_str)
        self._mode = mode

        self.key = key.lower().replace('j', 'i')
        self.key_matrix = self.generate_key_matrix(self.key)
        self._preprocessed_text = self._preprocess_text()

    @property
    def mode(self):
        if self._mode.lower() not in self.MODES:
            raise AttributeError('Invalid mode')
        return self._mode.lower()

    @property
    def processed(self):
        """
        :return: Returns the encrypted plaintext processed by the _encrypt_plaintext method.
        :rtype: str
        """
        return self._decrypt_encrypt_text()

    def generate_key_matrix(self, key):
        """
        :param key: The key used to generate the key matrix.
        :type key: str
        :return: A 5x5 matrix generated based on the key and the remaining characters of the alphabet.
        :rtype: list
        """
        key_matrix = []
        used_chars = set()

        # Add key characters to the matrix
        for char in key:
            if char not in used_chars:
                key_matrix.append(char)
                used_chars.add(char)

        # Add the rest of the alphabet to the matrix
        for char in self.alphabet:  # note: 'j' is omitted as it's combined with 'i'
            if char not in used_chars:
                key_matrix.append(char)
                used_chars.add(char)

        # Convert the list to a 5x5 matrix
        return [key_matrix[i:i + 5] for i in range(0, 25, 5)]

    def _preprocess_text(self):
        """
        :return: Preprocessed text with lower case, 'j' replaced by 'i', spaces removed,
            and 'x' inserted between duplicate letters.
        :rtype: str
        """
        # Preprocess text: lower case, replace 'j', remove spaces
        text = self.input_str.lower().replace('j', 'i').replace(" ", "")
        cleaned_text = []

        # Insert 'x' between duplicate letters and handle odd length
        i = 0
        while i < len(text):
            char = text[i]
            if i + 1 < len(text) and text[i] == text[i + 1]:
                cleaned_text.append(char)
                cleaned_text.append('x')
                i += 1
            else:
                cleaned_text.append(char)
                i += 1

        if len(cleaned_text) % 2 != 0:
            cleaned_text.append('x')
        self._preprocessed_text = ''.join(cleaned_text)
        return self._preprocessed_text

    def find_position(self, char):
        """
        :param char: The character to find the position of in the key matrix.
        :type char: str
        :return: Returns a tuple containing the row and column index of the character in the key matrix if found,
            otherwise None.
        :rtype: tuple(int, int) or None
        """
        for i, row in enumerate(self.key_matrix):
            if char in row:
                return i, row.index(char)
        return None

    def _encrypt_pair(self, a, b):
        """
        :param a: character to encrypt
        :type a: str
        :param b: character to encrypt
        :type b: str
        :return: the encrypted pair of characters
        :rtype: str
        """
        row_a, col_a = self.find_position(a)
        row_b, col_b = self.find_position(b)

        if row_a == row_b:
            return self.key_matrix[row_a][(col_a + 1) % 5] + self.key_matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            return self.key_matrix[(row_a + 1) % 5][col_a] + self.key_matrix[(row_b + 1) % 5][col_b]
        else:
            return self.key_matrix[row_a][col_b] + self.key_matrix[row_b][col_a]

    def _decrypt_pair(self, a, b):
        row_a, col_a = self.find_position(a)
        row_b, col_b = self.find_position(b)

        if row_a == row_b:
            return self.key_matrix[row_a][(col_a - 1) % 5] + self.key_matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            return self.key_matrix[(row_a - 1) % 5][col_a] + self.key_matrix[(row_b - 1) % 5][col_b]
        else:
            return self.key_matrix[row_a][col_b] + self.key_matrix[row_b][col_a]

    def _decrypt_encrypt_text(self):
        """
        :return: The encrypted version of the provided plaintext
            by encrypting pairs of characters using the `_encrypt_pair` method.
        :rtype: str
        """
        new_text = []

        for i in range(0, len(self._preprocessed_text), 2):
            a, b = self._preprocessed_text[i], self._preprocessed_text[i + 1]
            if self.mode == self.ENCRYPT:
                new_text.append(self._encrypt_pair(a, b))
            elif self.mode == self.DECRYPT:
                new_text.append(self._decrypt_pair(a, b))

        return ''.join(new_text)

    def display_key_matrix(self):
        """
        Display the contents of the key matrix in the console.

        :return: None
        :rtype: None
        """
        for row in self.key_matrix:
            print(' '.join(row))


def playfair_example():
    # Usage example
    key = "samplekey"
    plaintext = "hide the gold in the tree stump"

    cipher = PlayfairCipher(key, plaintext)
    ciphertext = cipher.processed

    print("Key Matrix:")
    cipher.display_key_matrix()
    # noinspection PyProtectedMember
    print(f"\nPrepared Text: {cipher._preprocessed_text}")
    print(f"Ciphertext: {ciphertext}")


def Rot13_test():
    scrambled = Rot13('Andrew MCSPARROn &').processed
    print(scrambled)
    unscrambled = Rot13(scrambled).processed
    print(unscrambled)


if __name__ == '__main__':
    playfair_example()
    #Rot13_test()
    #print(CaesarCipher('Andrew', 1).processed)
    # print(VigenereCipher('OCULORHINOLARINGOLOGY', 'attacking tonight').processed)
