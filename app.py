from flask import Flask, request, render_template, redirect
from wakeonlan import send_magic_packet
import json
import re

app = Flask(__name__)
DB_FILE = 'db/db.json'


@app.route('/')
def index():  # put application's code here
    with open(DB_FILE) as db_file:
        db_dict = json.load(db_file)
        address_list = db_dict['mac_addresses']
    return render_template('index.jinja2', address_list=address_list)


@app.get('/send')
def send_packet():
    mac_address = request.args.get('mac_address')
    broadcast_address = return_broadcast_address()
    if broadcast_address == "":
        send_magic_packet(mac_address)
    else:
        send_magic_packet(mac_address, broadcast_address)
    return redirect('/')


@app.get('/add')
def add_entry():
    mac_address = request.args.get('mac_address')

    # Checks for valid mac address.
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
        with open(DB_FILE) as db_file:
            db_dict = json.load(db_file)

        db_dict['mac_addresses'].append(mac_address)

        with open(DB_FILE, 'w') as db_file:
            json.dump(db_dict, db_file)

        return redirect('/')
    else:
        return render_template('error_format.jinja2', mac_address=mac_address)


@app.get('/delete')
def remove_entry():
    mac_address = request.args.get('mac_address')

    with open(DB_FILE) as db_file:
        db_dict = json.load(db_file)

    db_dict['mac_addresses'].remove(mac_address)

    with open(DB_FILE, 'w') as db_file:
        json.dump(db_dict, db_file)

    return redirect('/')


@app.get('/updateBroadcast')
def update_broadcast_address():
    new_broadcast_address = request.args.get('broadcast_address')

    with open(DB_FILE) as db_file:
        db_dict = json.load(db_file)

    db_dict["broadcast_address"] = new_broadcast_address

    with open(DB_FILE) as db_file:
        json.dump(db_dict, db_file)


def return_broadcast_address():
    with open(DB_FILE) as db_file:
        db_dict = json.load(db_file)
    broadcast_address = db_dict["broadcast_address"]
    if not broadcast_address:
        return ""
    else:
        return broadcast_address


if __name__ == '__main__':
    app.run()
