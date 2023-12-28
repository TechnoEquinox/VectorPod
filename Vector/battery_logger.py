import anki_vector
import time
import csv

LOG_FILE = "battery_log.csv"

def log_battery_data():
    # Write header to CSV file
    with open(LOG_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Voltage", "Is Charging"])

    while True:
        # Establish a fresh connection for each iteration
        with anki_vector.Robot(escape_pod=True) as robot:
            battery_state = robot.get_battery_state()
            if battery_state:
                voltage = battery_state.battery_volts
                is_charging = battery_state.is_charging
                timestamp = time.time()

                with open(LOG_FILE, "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, voltage, is_charging])

        time.sleep(5)  # Log every 5 seconds

if __name__ == "__main__":
    log_battery_data()
