#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------

# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return app.send_static_file("index.html")
from datetime import datetime


old_time = datetime(1970, 1, 1)

with open('0_sonarcloud.txt', 'r') as file:
   
    for line in file:
        # Strip the newline character from the line
        parts = line.split(" ")
        timestamp_str = parts[0]  # Extract the timestamp string
        timestamp_str = timestamp_str[:26] + "Z"
        try:
          new_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
          pass

        diff_in_seconds = (new_time - old_time).total_seconds()
        if  diff_in_seconds > 600:
          print(new_time)

        old_time = new_time