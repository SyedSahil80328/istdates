# Railway Nexus Automata
Railway Nexus Automata or Railway Station Management System is a web-based application system which manages all railway related activities. It has been built to support the following activities

1. **User Authentication**: This application has categorized the users as passengers, Station Masters, Station Clerks and Administrator. This application is loaded with strong encryption algorithm called TDES which is a block cipher for secured authentication. It ensures that no users can interchange their level of accessibilies.
2. **Railway ticket booking**: The users of passenger level can book their tickets by giving their personal details and mode of transportation. Based on the availability, a ticket will be generated with user details using Python's pdfkit module.
3. **Checking daily schedules**: Station masters can get the schedule of train in which it arrives at the current stations. All they need is to enter the station code. They get all the trains with timings with the help of ClearTrip updates.
4. **Announcement system with gTTs**: Station Masters can announce the passengers about the arrival and departure of a train with platform number and time with the help of Python's gTTs.
5. **Admin related activities**: This application is provided with facilities for administrators about checking the daily login of every users and creating organizational logins for railway employees.

Now let's see about the encryption algorithm used for login and signup purpose.

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

In this application, the first category (**TDES-EEA3**) is used which uses three independent keys for password encryption.

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
10. Run `python UserDetails.py`. It will contain your entire sign in credentials.
11. You'll see that the password is stored in encrypted form.

 **Note**: Creating ticket requires [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) application. So install it by clicking on the link given.
