# Flask is for routing and framework
# render_template is for rendering HTML
# request is for handling which request is made at each route as well as getting request.form data
# redirect is for redirecting to different (or the same) route
from flask import Flask, render_template, url_for, request, redirect

# Defining flask app name
app = Flask(__name__)


# ------- Code to encrypt will be placed here --------

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


# Function to encrypt a string using the pk object and RSA logic
def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


# Function to join together the list of strings after they've been encrypted
def join_encrypted(ciphertext):
    # Generate the string using the values of the ciphertext list
    plain = [chr(char) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


# Function to decrypt a string using the pk object and RSA logic
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

# ---------- End of code to encrypt --------------

# Main Route, defining the ability to make GET and POST requests to this main route
@app.route('/', methods=['GET'])
def index():
    # If there are messages in the request (Look at the url while in index after making a request)
    if 'messages' in request.args:
        # Create a list of lists which will be used to show in the table in index
        encrypted_object = [request.args.getlist('messages')]
    else:
        # Create an empty list since we have no messages in request.args
        encrypted_object = []
    return render_template('index.html', encrypted_object=encrypted_object)


# If the user clicks on the encrypt form, the app makes a post request to this route
@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt_route():
    # Define the encrypted list of strings using the encrypt function passing it the public key
    encrypted_text = encrypt(publicKey, request.form['plainText'])
    # Also define the decrypted text using the decrypt function to build the return object
    decrypted_text = decrypt(privateKey, encrypted_text)

    # This is the object we return, it's a list since we use the index positions to show in the table in index.html
    built_object = [request.form['plainText'], join_encrypted(encrypted_text), decrypted_text]
    return redirect(url_for('.index', messages=built_object))


# If the user clicks on the decrypt form, the app makes a post request to this route
@app.route('/decrypt', methods=['POST', 'GET'])
def decrypt_route():
    # Define the decrypted text using the decrypt function to build the return object
    decrypted_text = encrypt(privateKey, request.form['cipherText'])

    # This is the object we return, it's a list since we use the index positions to show in the table in index.html
    built_object = ['Not Applicable!', request.form['cipherText'], join_encrypted(decrypted_text)]
    return redirect(url_for('.index', messages=built_object))


# Running flask app
if __name__ == '__main__':
    app.run()
