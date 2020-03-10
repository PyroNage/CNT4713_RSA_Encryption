# Flask is for routing and framework
# render_template is for rendering HTML
# request is for handling which request is made at each route as well as getting request.form data
# redirect is for redirecting to different (or the same) route
from flask import Flask, render_template, url_for, request, redirect

# Import random for the RSA Encryption
import random

# Defining flask app name
app = Flask(__name__)

# Example for getting form data:
# insert_table_query = "INSERT INTO %s (email, firstName, lastName, age) VALUES ('%s', '%s', '%s', '%s');" % (
#   "userTable", request.form['email'], request.form['firstName'], request.form['lastName'],

# Initializing values for global scope variables
plainTextValue = ''
cipherTextValue = ''
decipheredTextValue = ''


# Code to encrypt will be placed here

# Algorithm from: https://crypto.stackexchange.com/questions/19444/rsa-given-q-p-and-e
# Algorithm takes in e and phi_of_n respectively and returns d
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return x


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def join_encrypted(ciphertext):
    # Generate the string using the values of the ciphertext list
    plain = [chr(char) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


# Parameters for encryption to be defined below
p = 47                          # p
q = 59                          # q
n = p * q                       # n
phi_of_n = (p - 1) * (q - 1)    # phi
e = 17                          # e was chosen by the video i was watching as a number that worked.
d = egcd(e, phi_of_n)           # find d from e * d mod phi_of_n = 1
publicKey = (e, n)              # public key tuple of value e and n
privateKey = (d, n)             # private key tuple of value d and n


# Main Route, defining the ability to make GET and POST requests to this main route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Print statement to check that post request is being received
        print('POST Request in index page')

        # STILL INSIDE THE IF POST -- Try to do this action
        try:
            print('We successfully processed the POST request. Here is the Data: %s' % plainTextValue)
            return redirect('/')

        # If there's an error run the code below
        except:
            return 'There was an issue adding your user.'

    # If the request is NOT a POST (so if the request is a GET)
    else:
        # return render_template('index.html', users=items)only showing this code to show how to pass parameters to html

        return render_template('index.html')


# If the user clicks on the encrypt form, the app makes a post request to this route
@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt_route():
    encrypted_text = encrypt(publicKey, request.form['plainText'])
    return 'Encrypted text: %s' % join_encrypted(encrypted_text)


# If the user clicks on the decrypt form, the app makes a post request to this route
@app.route('/decrypt', methods=['POST', 'GET'])
def decrypt_route():
    decrypted_text = encrypt(privateKey, request.form['cipherText'])
    return 'Decrypted text: %s' % join_encrypted(decrypted_text)


# @app.route('/delete/<string:email>') Showing this to show how to pass parameters to the route

# Running flask app
if __name__ == '__main__':
    app.run()
