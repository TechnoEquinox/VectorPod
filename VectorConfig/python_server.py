#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import logging
from shop_handler import ShopHandler

app = Flask(__name__)
CORS(app)

shop_handler = ShopHandler()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def execute_script_in_venv(script_path):
    venv_python_path = os.path.join(os.path.expanduser("~"), 'vector-venv/bin/python3')
    
    command = [
        venv_python_path,
        script_path
    ]

    # The environment variable can be set directly in the subprocess call
    env = dict(PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python')

    logging.debug(f"Executing command: {command}")

    try:
        output = subprocess.check_output(command, env=env)
        return True, output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e}")
        return False, str(e)

@app.route('/run_level_manager', methods=['POST'])
def run_level_manager():
    script_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/plugins/vectormyboi/Vector/level_manager.py")
    logging.debug(f"Script path: {script_path}")
    success, message = execute_script_in_venv(script_path)
    return jsonify(success=success, message=message), 200 if success else 500

@app.route('/run_go_for_jog', methods=['POST'])
def run_go_for_jog():
    script_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/plugins/vectormyboi/Vector/vector_go_for_jog.py")
    logging.debug(f"Script path: {script_path}")
    success, message = execute_script_in_venv(script_path)
    return jsonify(success=success, message=message), 200 if success else 500

@app.route('/run_scratch_ticket', methods=['POST'])
def run_scratch_ticket():
    script_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/plugins/vectormyboi/Vector/vector_scratch_ticket.py")
    logging.debug(f"Script path: {script_path}")
    success, message = execute_script_in_venv(script_path)
    return jsonify(success=success, message=message), 200 if success else 500

@app.route('/run_wallet_manager', methods=['POST'])
def run_wallet_manager():
    script_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/plugins/vectormyboi/Vector/wallet_manager.py")
    logging.debug(f"Script path: {script_path}")
    success, message = execute_script_in_venv(script_path)
    return jsonify(success=success, message=message), 200 if success else 500

@app.route('/run_battery_manager', methods=['POST'])
def run_battery_manager():
    script_path = os.path.join(os.path.expanduser("~"), "wire-pod/chipper/plugins/vectormyboi/Vector/battery_manager.py")
    logging.debug(f"Script path: {script_path}")
    success, message = execute_script_in_venv(script_path)
    return jsonify(success=success, message=message), 200 if success else 500

@app.route('/buy_item', methods=['POST'])
def buy_item():
    data = request.get_json()
    item_id = data.get('item_id')
    success, message = shop_handler.handle_purchase(item_id)
    return jsonify(success=success, message=message), 200 if success else 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8091)
