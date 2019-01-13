import string


class RSA:
    # This acts as a user in an RSA communication exchange, it has its own public and private keys as a result
    def __init__(self, n, e, d):
        print("created RSA")
        self.outcomes = {}
        self.n = n
        self.e = e
        self.d = d

    def clean(self):
        self.outcomes = {}

    def power(self, message, exponent, modulo, long_winded=False):
        # this is a recursive function with memoisation
        # returns (message^exponent) mod modulo
        # set long_winded flag to True to print all intermediate values
        if exponent == 1:
            return message % modulo
        binary_exponent = str(bin(exponent))[2:][::-1]
        powers = []
        for pos in range(len(binary_exponent)):
            if binary_exponent[pos] == "1":
                powers.append(pow(2,pos))
        if long_winded:
            print(message, "^", exponent, "mod", modulo, "=" , message, "^ (", "".join(["+" + str(power) for power in powers])[1:], ") mod " , modulo)
            print(message, "^", exponent, "mod", modulo, "=(", "".join(["*" + "(" + str(message) + "^" + str(power) + " mod " + str(modulo) + ")" for power in powers] )[1:], ") mod ", modulo)
        results = []
        if len(powers) > 1:
            for power in powers:
                if power in self.outcomes.keys():
                    results.append(self.outcomes[power])
                else:
                    results.append(self.power(message, power, modulo, long_winded=long_winded))
                    self.outcomes[power] = results[-1]
        else:
            results.append(self.power_of_2(message, powers[0], modulo, long_winded=long_winded))
        multiplication = 1
        for result in results:
            multiplication = (multiplication * result) % modulo
        final_result = multiplication % modulo
        if long_winded:
            print(message, "^", exponent, "mod " , modulo, "= ", final_result)
        return final_result

    def power_of_2(self, message, exponent, modulo, long_winded=False):
        # returns (message^exponent) mod modulo as long as exponent is a power of 2
        # set long_winded flag to True to print out all intermediate values
        if long_winded:
            print("Calculating "+ str(message) + "^" , exponent, "mod" , modulo)
        power = 1
        result = message % modulo
        while power < exponent:
            result = (result * result) % modulo
            power = 2 * power
        if long_winded:
            print(str(message) + "^" , exponent , "mod " , modulo, "=", result)
        return result

    def modulo_exponentiate(self, message, n, k, long_winded=False):
        # returns (message^k) mod n
        self.clean()
        return self.power(message, k, n, long_winded=long_winded)

    def encrypt(self, message, recipient_public_key):
        # returns (message^recipient_public_key.e) mod recipient_public_key.n
        # this function will encrypt and decrypt for any given key to be used
        return self.modulo_exponentiate(message, recipient_public_key[0], recipient_public_key[1])

    def decrypt(self, encrypted_message):
        # returns (encrypted_message ^ self.d) mod self.n
        # this function is ONLY for decrypting messages sent to this RSA Model, as such it will only use its private key
        # if you need to decrypt a message to a different individual just encrypt with the known key, since encrypt and
        # decrypt perform the same modulo_exponentiation method
        return self.modulo_exponentiate(encrypted_message, self.n, self.d)

if __name__ == "__main__":

    # harold acts as the user's RSA Communication presence
    harold = RSA(9436709, 1676267, 3497603)
    bob_public_key = (122269479,53407)
    # bank_key is the bank's public key
    bank_key = (76282747,65537)
    print("Starting Q4 i)")
    print("Q4(i): 17^54 mod 139 = ", harold.modulo_exponentiate(17, 139, 54, long_winded=True))
    print("Starting Q4 ii)")
    print("Q4(ii): 2345^65531 mod 265189 = ", harold.modulo_exponentiate(2345,265189, 65531, long_winded=True))
    print("Starting Q4 iii)")
    print("Q4(iii): 4733459^65537 mod 75968647 = ", harold.modulo_exponentiate(4733459, 75968647, 65537, long_winded=True))
    print("Q5: M^bank_public_e mod bank_public_n = ", harold.encrypt(654733, bank_key))
    print("Q6: M^own_private_d mod own_n = ", harold.decrypt(1684446))
    print("Q7: (C(M),C(S)) = (M^bank_public_e mod bank public_n, (M^own_private_d mod own_n)^bank_public_e mod bank public_n = ", (harold.encrypt(337722, bank_key), harold.encrypt(harold.decrypt(337722), bank_key)))
    Q8_tuple = (harold.decrypt(4647068),harold.encrypt(harold.decrypt(526345), bank_key))
    print("Q8: (C(M),C(S)) => (M,M) = (C(M)^own_private_d mod own_n, (C(S)^own_private_d mod own_n)^bank_public_e mod bank public_n)  = ", Q8_tuple)
    if Q8_tuple[0] != Q8_tuple[1]:
        print("Signature in Q8 was not valid")
    else:
        print("Signature in Q8 was valid")

    fake_MS = (harold.encrypt(23,bob_public_key), 23)
    print("Q9: Fake (M,S) from Bob = ", fake_MS)
    print("To confirm that (M,S) appears to come from Bob check that M = S^bob_public_e mod bob_public_n")
    print("Confirming that (M,S) appears to come from Bob:");
    if harold.encrypt(fake_MS[1], bob_public_key) != fake_MS[0]:
        print("signature was not valid for fake Bob message")
    else:
        print("signature was valid for fake Bob message")

    print("Q10: Crack message: ")
    for val in range(1000):
        message = harold.encrypt(val, bank_key)
        if message == 58621765:
            print("new three-digit pin = " , val)
            break