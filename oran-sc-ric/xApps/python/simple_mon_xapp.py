#!/usr/bin/env python3

import argparse
import signal
import socket
import json
import threading
import logging
from datetime import datetime

class MyXapp:
    def __init__(self, udp_ip, udp_port):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.stop_event = threading.Event()
        self.ue_counter = 0
        self.metrics = []

    def udp_receiver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.udp_ip, self.udp_port))
        sock.setblocking(False)
        
        print(f"UDP Receiver started on {self.udp_ip}:{self.udp_port}...")
        while not self.stop_event.is_set():
            try:
                data, addr = sock.recvfrom(3000)
                try:
                    json_data = json.loads(data.decode('utf-8'))
                    self.process_metrics(json_data)
                except json.JSONDecodeError:
                    print("Received data is not in JSON format:", data.decode('utf-8'))
            except socket.error:
                pass

    def process_metrics(self, metrics_data):
        timestamp = metrics_data.get("timestamp", None)
        if timestamp:
            time_formatted = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')[:-3]
            print(f"\nMetrics Received at {time_formatted}:")

        ue_list = metrics_data.get("ue_list", [])
        for i, ue in enumerate(ue_list):
            ue_metrics = ue.get("ue_container", {})
            print(f"UE {i + 1} Metrics:")  # Added 1 to i to start from UE1
            for metric_name, value in ue_metrics.items():
                print(f"--Metric: {metric_name}, Value: {value}")

        self.metrics.append(metrics_data)  # Save the metrics data

    def start(self):
        print(f"xApp started. Listening for UDP metrics on port {self.udp_port}.")
        
        udp_thread = threading.Thread(target=self.udp_receiver)
        udp_thread.start()
        try:
            while not self.stop_event.is_set():
                pass
        except KeyboardInterrupt:
            print("xApp interrupted. Stopping...")
        
        self.stop_event.set()
        udp_thread.join()
        
        # Write all metrics to a JSON file upon stopping
        self.write_metrics_to_file()
        print("xApp stopped.")

    def write_metrics_to_file(self):
        output_filename = 'gnb_metrics.json'
        try:
            with open(output_filename, 'w') as file:
                for entry in self.metrics:
                    json.dump(entry, file)
                    file.write("\n")  # Add a new line after each entry
            print(f"Received data saved to {output_filename}. Exiting...")
        except Exception as e:
            print(f"Failed to write metrics to file: {e}")

    def signal_handler(self, sig, frame):
        print(f"Received signal {sig}, exiting...")
        self.stop_event.set()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP Metrics xApp')
    parser.add_argument("--udp_ip", type=str, default="127.0.0.1", help="UDP IP address to bind")
    parser.add_argument("--udp_port", type=int, default=55555, help="UDP port to listen on")
    args = parser.parse_args()

    myXapp = MyXapp(args.udp_ip, args.udp_port)

    signal.signal(signal.SIGQUIT, myXapp.signal_handler)
    signal.signal(signal.SIGTERM, myXapp.signal_handler)
    signal.signal(signal.SIGINT, myXapp.signal_handler)

    myXapp.start()

