from flask import Flask, request, render_template, redirect
from wakeonlan import send_magic_packet
import json
import re

app = Flask(__name__)
DB_FILE = 'db/db.json'


@app.route('/')
def index():  # put application's code here
    with open(DB_FILE) as db_file:
        address_dict = json.load(db_file)
        address_list = address_dict['mac_addresses']
    return render_template('index.jinja2', address_list=address_list)


@app.get('/send')
def send_packet():
    mac_address = request.args.get('mac_address')
    send_magic_packet(mac_address)
    print('Sent packet!')
    return redirect('/')


@app.get('/add')
def add_entry():
    mac_address = request.args.get('mac_address')

    # Checks for valid mac address.
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
        with open(DB_FILE) as db_file:
            address_dict = json.load(db_file)

        address_dict['mac_addresses'].append(mac_address)

        with open(DB_FILE, 'w') as db_file:
            json.dump(address_dict, db_file)

        return redirect('/')
    else:
        return render_template('error_format.jinja2', mac_address=mac_address)


@app.get('/delete')
def remove_entry():
    mac_address = request.args.get('mac_address')

    with open(DB_FILE) as db_file:
        address_dict = json.load(db_file)

    address_dict['mac_addresses'].remove(mac_address)

    with open(DB_FILE, 'w') as db_file:
        json.dump(address_dict, db_file)

    return redirect('/')


if __name__ == '__main__':
    app.run()
