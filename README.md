# Understanding TDES and it's implementation
## Encryption and Decryption

Encryption is the process of converting plain text or data into a ciphertext, which is a scrambled and unreadable format, using an algorithm and a key. The purpose of encryption is to protect the confidentiality of the information being transmitted or stored, ensuring that only authorized parties can access and decipher it.

Decryption, on the other hand, is the reverse process of encryption. It involves converting the ciphertext back into its original plaintext form, using the appropriate decryption algorithm and key. Decryption allows authorized parties to access and interpret the encrypted data.

## TDES

TDES, or Triple Data Encryption Standard, is a symmetric encryption algorithm that uses multiple iterations of the Data Encryption Standard (DES) cipher to enhance security. DES, developed in the 1970s, became vulnerable to brute-force attacks due to its short key length. TDES was introduced as a way to strengthen DES by applying it multiple times with different keys.

TDES operates in three modes: 

1. **TDES-EEA3 (Encryption Algorithm 3)**: In this mode, data is encrypted with three independent DES keys, providing a higher level of security compared to single DES encryption.

2. **TDES-EIA3 (Integrity Algorithm 3)**: This mode involves applying TDES in CBC (Cipher Block Chaining) mode for encryption and CBC-MAC (Cipher Block Chaining Message Authentication Code) for integrity protection.

3. **TDES-EIA2 (Integrity Algorithm 2)**: Similar to TDES-EIA3, but with different padding and integrity protection mechanisms.

TDES is widely used in various industries for securing sensitive data, especially where legacy systems or regulatory requirements dictate its usage. However, due to its relatively slow speed and the emergence of more efficient encryption algorithms with stronger security properties, TDES is gradually being replaced by modern encryption standards like AES (Advanced Encryption Standard).

## Implementation Steps

1. Open CMD or Powershell.
2. Clone this with `git clone https://github.com/SyedSahil80328/istdates.git`
3. Install all requirements with `pip install -r requirements.txt`
4. Navigate to `cd istdates`
5. Run `python app.py`
6. Open browser and paste `http://127.0.0.1:5000/`
7. Open signup icon and create an account.
8. Open another window of CMD.
9. Navigate to same directory your application is running.
10. Run `python create.py`. It will contain your entire sign in credentials.
11. You'll see that the password is stored in encrypted form.
