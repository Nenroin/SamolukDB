class DataCryptographer:
    @staticmethod
    def lzss_encrypt_data(text: str) -> str:
        search_buffer: str = ""
        check_characters: str = ""
        output: str = ""

        for i, char in enumerate(text):
            check_characters += char
            offset: int = search_buffer.find(check_characters)

            if offset == -1 or i == len(text) - 1:
                privies_index: int = offset

                if i != len(text) - 1 or offset == -1:
                    current_check_characters = check_characters[:-1]
                else:
                    current_check_characters = check_characters

                offset = search_buffer.find(current_check_characters)
                length = len(current_check_characters)
                token = f"<{offset},{length}>"

                output += "".join(current_check_characters) if len(token) > length or offset == -1 else token

                if i == (len(text) - 1) and privies_index == -1:
                    output += check_characters[-1]

                check_characters = check_characters[-1:]

            search_buffer += char

        return output

    @staticmethod
    def lzss_decrypt_data(text: str):
        inside_token = False
        scanning_offset = True

        output: str = ""

        length = []
        offset = []

        for i, char in enumerate(text):
            if char == "<":
                inside_token = True
                scanning_offset = True
            elif char == "," and inside_token:
                scanning_offset = False
            elif char == ">" and inside_token:
                inside_token = False

                length_num = int("".join(length))
                offset_num = int("".join(offset))

                referenced_text = output[offset_num:][:length_num]

                if len(referenced_text) == 1:
                    output += "".join([referenced_text[0] for _ in range(length_num)])
                else:
                    output += referenced_text

                length, offset = [], []
            elif inside_token:
                if scanning_offset:
                    offset.append(char)
                else:
                    length.append(char)
            else:
                output += char

        return output

    @staticmethod
    def offset_encrypt_data(text: str, crypt_word:str = "nenroin") -> str:
        output: str = ""
        crypt_word_idx: int = 0

        for char in text:
            output += chr((ord(char) + ord(crypt_word[crypt_word_idx])) % 1114111)
            crypt_word_idx = (crypt_word_idx + 1) % len(crypt_word)

        return output

    @staticmethod
    def offset_decrypt_data(text: str, crypt_word:str = "nenroin"):
        output: str = ""
        crypt_word_idx: int = 0

        for char in text:
            output += chr((ord(char) - ord(crypt_word[crypt_word_idx])) % 1114111)
            crypt_word_idx = (crypt_word_idx + 1) % len(crypt_word)

        return output


if __name__ == '__main__':
    string: str = "Pease porridge hot, pease porridge cold, Pease porridge in the pot, nine days old; Some like it hot, some like it cold, Some like it in the pot, nine days old."
    encrypt_string: str = DataCryptographer.lzss_encrypt_data(string)
    print(encrypt_string)

    print(string)
    decrypt_string = DataCryptographer.lzss_decrypt_data(encrypt_string)
    print(decrypt_string)

    encrypt_string = DataCryptographer.offset_encrypt_data(string, "Andrey")
    print(encrypt_string)
    decrypt_string = DataCryptographer.offset_decrypt_data(encrypt_string, "Andrey")
    print(decrypt_string)
