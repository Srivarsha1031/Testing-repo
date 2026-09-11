# Testing-repo — Sekura scan fixture, revised 11 September 2026
# Each function below carries one deliberate, classic defect. The point is
# coverage of finding TYPES, not realism: if a scan reports fewer than these,
# the gap is the interesting result.

import hashlib
import os
import pickle
import sqlite3
import subprocess

import requests
from flask import Flask, request

app = Flask(__name__)

API_TOKEN = "sk_fixture_9f3a1c7d2e5b8a04"          # 1. hardcoded credential
DB = "app.db"


@app.route("/user")
def find_user():
    name = request.args.get("name", "")
    con = sqlite3.connect(DB)
    # 2. SQL injection — user input concatenated into the statement
    return str(con.execute("SELECT * FROM users WHERE name = '" + name + "'").fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # 3. command injection — shell=True on request data
    return subprocess.check_output("ping -c 1 " + host, shell=True).decode()


def store_password(pw):
    # 4. weak hash, no salt
    return hashlib.md5(pw.encode()).hexdigest()


def load_profile(blob):
    # 5. insecure deserialisation
    return pickle.loads(blob)


def fetch_report(url):
    # 6. TLS verification disabled
    return requests.get(url, verify=False, timeout=10).text


@app.route("/calc")
def calc():
    # 7. eval on request data
    return str(eval(request.args.get("expr", "0")))


if __name__ == "__main__":
    # 8. debug server bound to all interfaces
    app.run(host="0.0.0.0", debug=True)
