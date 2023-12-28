#!/home/connorbailey/vector-venv/bin/python3

import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps
import grpc
from grpc._channel import _MultiThreadedRendezvous
import json
import time
import random
from datetime import datetime, timedelta
from level_manager import LevelManager

class VectorGoForJog():
    def __init__(self):
        self.required_energy: int = 10
        self.cool_down: int = 300
        self.robot_config_path: str = "../wire-pod/chipper/webroot/robot_config.json"
    
    def read_json_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def write_json_file(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def check_energy_level(self, robot_data):
        if robot_data["robot_energy_level"] < self.required_energy:
            return False
        else:
            return True
    
    def time_elapsed_since_last_log(self, last_jog_str):
        # Parse the last_log string into a datetime object
        last_jog = datetime.strptime(last_jog_str, '%Y-%m-%dT%H:%M:%S')
        # Get the current datetime
        now = datetime.now()
        # Calculate the difference
        elapsed_time = now - last_jog

        return elapsed_time
    
    def generate_xp(self):
        return random.randint(1, 5)
    
    def find_money(self, data, robot):
        chance = random.randint(1, 100)
        print(f"Chance: {chance}")
        if chance > 90:
            found_money = random.randint(1, 3)
            if found_money > 1:
                robot.behavior.say_text(f"Oh hey look, I found {found_money} coins on the ground. Let me put them in my wallet.")
                
                count = 0
                for count in range(found_money):
                    print(f"Count: {count}")
                    print("Lift down...")
                    robot.motors.set_lift_motor(-5)
                    time.sleep(1.0)
                    print("Lift up")
                    robot.motors.set_lift_motor(5)
                    time.sleep(1.0)
                    count += 1
            else:
                robot.behavior.say_text(f"Oh hey look, I found {found_money} coin on the ground. Let me put it in my wallet.")
            data["robot_wallet"] = data["robot_wallet"] + found_money
            self.write_json_file(filename=self.robot_config_path, data=data)
    
    def do_action(self, robot_data, robot):
        robot_data["robot_energy_level"] = robot_data["robot_energy_level"] - self.required_energy
        earned_xp = self.generate_xp()
        print(f"Robot XP: {robot_data['robot_xp']}")
        print(f"Earned XP: {earned_xp}")
        robot_data["robot_xp"] = robot_data["robot_xp"] + earned_xp

        robot.behavior.drive_off_charger()
        robot.motors.set_lift_motor(5)
        for _ in range(8):
            print("Drive Vector straight...")
            robot.behavior.drive_straight(distance_mm(125), speed_mmps(100))
            
            self.find_money(data=robot_data, robot=robot)

            print("Turn Vector in place...")
            robot.behavior.turn_in_place(degrees(90))
        
        robot.motors.set_lift_motor(-5)
        robot.anim.play_animation_trigger('GreetAfterLongTime', ignore_body_track=True)
        robot.behavior.say_text(f"Wow! That was great! I earned {earned_xp} experience points")
        
        level_manager = LevelManager()
        if level_manager.check_if_level_up(robot_data=robot_data):
            robot.behavior.say_text(f"Oh? I also leveled up to Level {robot_data['robot_level'] + 1}!")
            robot_data["robot_level"] = robot_data["robot_level"] + 1
        
        self.write_json_file(filename=self.robot_config_path, data=robot_data)

        # robot.behavior.drive_on_charger()

    def main(self):
        print("Reading robot config...")
        robot_data = self.read_json_file(self.robot_config_path)

        print("Connecting to the robot...")
        try:
            with anki_vector.Robot(ip=robot_data["ip_address"], escape_pod=True) as robot:
                print("Checking time since last jog...")
                elapsed_time = self.time_elapsed_since_last_log(robot_data["last_jog"])
                
                if elapsed_time > timedelta(seconds=self.cool_down):
                    if self.check_energy_level(robot_data=robot_data):
                        robot.behavior.say_text("Lets go jogging!")
                        robot_data["last_jog"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                        self.write_json_file(self.robot_config_path, robot_data)

                        self.do_action(robot_data=robot_data, robot=robot)
                    else:
                        robot.behavior.say_text(f"I'm tired, I need {self.required_energy} energy to do that")
                else:
                    remaining_time = self.cool_down - elapsed_time.total_seconds()

                    hours, remainder = divmod(remaining_time, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    time_string = ""
                    if hours:
                        time_string += f"{int(hours)} hours "
                    if minutes:
                        time_string += f"{int(minutes)} minutes "
                    if seconds:
                        time_string += f"{int(seconds)} seconds"

                    robot.behavior.say_text(f"I can't go jogging yet. I need to wait for {time_string} more.")

        except grpc._channel._InactiveRpcError as e:
            if "Maximum auth rate exceeded" in str(e):
                print("Authentication rate limit exceeded. Please wait and try again later.")
            else:
                print(f"An unexpected error occurred: {e}")
        except _MultiThreadedRendezvous as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print("The request timed out.")
            else:
                print(f"An unexpected GRPC error occurred: {e.details()}")


if __name__ == "__main__":
    vector = VectorGoForJog()
    vector.main()