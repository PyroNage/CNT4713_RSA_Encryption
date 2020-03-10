# Flask is for routing and framework
# render_template is for rendering HTML
# request is for handling which request is made at each route as well as getting request.form data
# redirect is for redirecting to different (or the same) route
from flask import Flask, render_template, url_for, request, redirect

# Defining flask app name
app = Flask(__name__)

# Example for getting form data:
# insert_table_query = "INSERT INTO %s (email, firstName, lastName, age) VALUES ('%s', '%s', '%s', '%s');" % (
#   "userTable", request.form['email'], request.form['firstName'], request.form['lastName'],

# Initializing values for global scope variables
plainTextValue = ''
cipherTextValue = ''
decipheredTextValue = ''


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


def encrypt_data(data_to_encrypt):
    print(data_to_encrypt)


def decrypt_data(data_to_decrypt):
    print(data_to_decrypt)


# If the user clicks on the encrypt form, the app makes a post request to this route
@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt():
    encrypt_data(request.form['plainText'])
    return 'encrypt: %s' % request.form['plainText']


# If the user clicks on the decrypt form, the app makes a post request to this route
@app.route('/decrypt', methods=['POST', 'GET'])
def decrypt():
    decrypt_data(request.form['cipherText'])
    return 'decrypt: %s' % request.form['cipherText']


# @app.route('/delete/<string:email>') Showing this to show how to pass parameters to the route

# Running flask app
if __name__ == '__main__':
    app.run()
