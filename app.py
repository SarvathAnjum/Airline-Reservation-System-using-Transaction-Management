from unittest import result
from flask import Flask, render_template, request, url_for, redirect
from csv import writer
import csv
from operator import itemgetter


class ticket:
    """First Name,Last Name,Phone Number,Departure Date,Arrival Date,Price,Seat Type"""


global d
global array_accId
d = {}
global arrayOfProducts

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

global array
global t
t = []


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/userlogin')
def ulogin():
    return render_template('userlogin.html')


@app.route('/userdetail', methods=['GET', 'POST'])
def book_p():

    return render_template('userdetail.html')


@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')


@app.route('/admin', methods=['POST', 'GET'])
def listmethod():
    global array
    array = unpack()
    if(request.method == 'POST'):
        account = request.form.get('account')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        dept = request.form.get('dept')
        destiny = request.form.get('destiny')
        seattype = request.form.get('seattype')
        phone = request.form.get('phone')
        price = request.form.get('price')
        pack(account, fname, lname, departure, arrival,
             dept, destiny, seattype, phone, price)

        post_ledger(array)
        return render_template('home.html')
    print("&&&&&&&&&&&&")
    print(array)
    arrayOfProducts = unpack_journal()
    return render_template('admin.html', dict_item=array, arrayOfProducts=arrayOfProducts)


####Add Contenets to csv File #########


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj, delimiter='|')
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def unpack_journal():
    i = 0
    with open("journal.csv") as file_name:
        file_read = csv.reader(file_name)

        array = list(file_read)
        arrayOfProducts = []
        for k in array:
            i = k
            for j in i:
                sub = j.split('|')
                arrayOfProducts.append(sub)
        return arrayOfProducts


def unpack():
    global array
    diction = {}
    global array_accId
    global arrayOfProducts

    i = 0
    with open("journal.csv") as file_name:
        file_read = csv.reader(file_name)

        array = list(file_read)
        arrayOfProducts = []
        for k in array:
            i = k
            for j in i:
                sub = j.split('|')
                arrayOfProducts.append(sub)
        arrayOfProducts.sort()

        for r in arrayOfProducts:
            key = r[0]
            if key not in diction.keys():
                diction[key] = [r]
            else:
                diction[key].append(r)
        for key in diction.keys():
            value = diction[key]
            sorted(value, key=itemgetter(3))
    return diction


def pack(account, fname, lname, departure, arrival, dept, destiny, seattype, phone, price):
    rowcontents = [account, fname, lname, departure, arrival,
                   dept, destiny, seattype, phone, price]
    append_list_as_row('journal.csv', rowcontents)


def post_ledger(array):

    test = array
    with open("ledger.csv", "w") as outfile:

        # pass the csv file to csv.writer.
        writer = csv.writer(outfile, delimiter='|')

        # convert the dictionary keys to a list
        key_list = list(test.keys())

        # find th length of the key_list
        limit = len(key_list)

        # the length of the keys corresponds to
        # no. of. columns.
        writer.writerow(test.keys())

        # iterate each column and assign the
        # corresponding values to the column
        for i in test:
            li = test[i]
            writer.writerow([li[0][0]])
            for k in li:
                writer.writerow(k)


@app.route('/search', methods=['GET', 'POST'])
def search():
    global array
    if(request.method == 'POST'):
        account = request.form.get('id')
        k = unpack()
        print('###########################')
        print(k)
        if account in k.keys():
            val = k.get(account)
            message = "Account present"
            return render_template('adminsearch.html', message=message, val=val)
        else:
            message = "Not present"
        return render_template('adminsearch.html', message=message)

    return render_template('adminsearch.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    global array
    global d
    global arrayOfProducts
    if(request.method == 'POST'):
        accountid = request.form.get('deleteadmin')
        global result
        result = []
        d = unpack()
        if accountid in d.keys():
            d.pop(accountid)
            print(d)
            post_ledger(d)
            message = "Account present deleting"
            for transac in arrayOfProducts:

                if(transac[0] != accountid):
                    result.append(transac)

            print("*****")
            with open("journal.csv", "w") as outfile:
                writer = csv.writer(outfile, delimiter='|')
                for i in result:
                    writer.writerow(i)
            return render_template('admindelete.html', message=message, d=d)
        else:
            message = " Account Not present"

        return render_template('admindelete.html', message=message)

    return render_template('admindelete.html')


if __name__ == "__main__":
    app.run(debug=True)
