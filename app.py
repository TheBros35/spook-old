from flask import Flask, request, render_template, redirect
from wakeonlan import send_magic_packet
import json
import re
import logging
import os

app = Flask(__name__)
DB_FILE = 'db/db.json'
LOG_FILE = 'spook.log'
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)
logging.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logging.WARNING, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


@app.route('/')
def index():  # put application's code here
    with open(DB_FILE) as db_file:
        db_dict = json.load(db_file)
        address_list = db_dict['mac_addresses']
    return render_template('index.jinja2', address_list=address_list)


@app.get('/send')
def send_packet():
    mac_address = request.args.get('mac_address')
    send_magic_packet(mac_address)
    logging.warning(f'Sent packet to {mac_address}')
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

        logging.warning(f'Added new address {mac_address}')
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

    logging.warning(f'Deleted address {mac_address}')
    return redirect('/')


@app.route('/viewLog')
def view_log():
    with open(LOG_FILE) as log_file:
        log_list = log_file.readlines()
    return render_template('view_log.jinja2', log=log_list)


if __name__ == '__main__':
    app.run()
