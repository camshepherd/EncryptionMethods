import string

class Vigenere:
    def __init__(self):
        self.alphabet = list(string.ascii_uppercase)

    def encode(self, message, key):
        extended_key = ""
        while len(extended_key + key) <= len(message):
            extended_key = extended_key + key
        extended_key += key[0:len(message) - len(extended_key)]
        encrypted_message = ""
        for character_ref in range(len(message)):
            encrypted_message += self.alphabet[(ord(message[character_ref]) - 65 + ord(extended_key[character_ref]) - 65)%26]
        return encrypted_message

    def decode(self, cipher_text, key):
        extended_key = ""
        while len(extended_key + key) <= len(cipher_text):
            extended_key = extended_key + key
        extended_key += key[0:len(cipher_text) - len(extended_key)]
        message = ""
        for character_ref in range(len(cipher_text)):
            message += self.alphabet[(ord(cipher_text[character_ref]) - ord(extended_key[character_ref])) % 26]
        return message


if __name__ == "__main__":
    vigenere = Vigenere()
    assert vigenere.encode("BLACKBEARDISSAILINGTOJAMAICA", "YOHOHO") == "ZZHQRPCOYRPGQOPZPBEHVXHAYWJO", "encoding not working correctly"
    assert vigenere.decode("ZZHQRPCOYRPGQOPZPBEHVXHAYWJO", "YOHOHO") == "BLACKBEARDISSAILINGTOJAMAICA", "decoding not working correctly"

    print("Q1: LETSSAILFORTHESPANISHMAIN encrypted with PIECESOFEIGHT =" , vigenere.encode("LETSSAILFORTHESPANISHMAIN", "PIECESOFEIGHT"))
    print("Q2: Decryption of ZVTVKGVBLNWYJVCLBOOHSSKFIGWYOEDNZ using key GOLDCOINS =" , vigenere.decode("ZVTVKGVBLNWYJVCLBOOHSSKFIGWYOEDNZ", "GOLDCOINS"))

    C1 = "KPKWETQKAODLZMERBOCAPNEERINWHQYBUOQUWTXMKIIBLNISOQAFRQHFHBEYXUPDMIMHEJNURXYQCXMULOVEKKXZZQWUUIBVSLMDJYQGBEVBIXDSJVXVPMYAAZROGEBGWIEVHLADXKRUIUYZDNCJTTKXDCHKNWGDNCKQGCBZVZNJPOFDYWWYRDMKFHKXFMFRGLMKHRWHFRJVNSGAQJHNCBYGSCEOPDVRRPPFWLOGUSRHZRIIAKYGZBJVPPQLRMMFGFBXTSMBJFLBOAWBKCD"
    C2 = "IXYVAGYZLHMRCLAGUGXEQSMFXAZTHFCKNSGXINVHWDOOUPVUNYIZFMKYTOVKKEADYZPZGXWJFVSXGMXAZMHQTRPYGIXTESRVIGWWSLTHXIZIDPEVSSDRHIKKGDTYHWICSYTOIWPUBZNFVEZCHWWGHUAJBBXIJTGLRJHGLHXRNJANPNPZWZYCIPHPYOANIPHOBKKRPYJHVTTEHROJYQCDTRDOWUKGCEEPLVNZSRCMTOUYLHWNHXGHNMWJEMHCIOHKNIHXSOTMDRSCBQYZYNU"
    C3 = "YAGNKAIHHXBZDQPTWHMSHWINSAZDWTJXNRTWAISMEPXCAKFGSPINWPZTEAKMFOLSKKRYGHYGCELHQHCOUFFMBDWGHVUGYEWHJYOUDTJJJKLHYLPENAOOUKHOXIFSDSUNACTFCPGKLTAINMULRBNXBUMTCMYPAXLQDLAJMFPSDKEKEOKNRRHQPXDKXMHEPWJBINLDIZTOYPQCIAMBXLIJZDKQRVOFTNRQNGIYOOBSXKZEBHCLYNUTALHFXZVNZNFJZGOSBKCPLEKFOKIEWYX"
    print("Q3: C = C1 - C2 + C3 (from simultaneous equations) = ", vigenere.encode(vigenere.decode(C1, C2), C3))
