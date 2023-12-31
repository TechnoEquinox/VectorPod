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

class VectorScratchTicket():
    def __init__(self):
        self.required_energy: int = 5
        self.lotto_number_count = 3
        self.min_jackpot: int = 100
        self.max_jackpot: int = 500
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
    
    def generate_xp(self):
        return random.randint(1, 5)
    
    def lotto_numbers(self):
        numbers = []
        for _ in range(self.lotto_number_count):
            number = random.randint(1, 5)  # Generate a random number between 1 and 5
            numbers.append(number)
        return numbers
    
    def get_jackpot(self):
        return random.randint(self.min_jackpot, self.max_jackpot)
    
    def do_action(self, robot_data, robot):
        robot_data["robot_energy_level"] = robot_data["robot_energy_level"] - self.required_energy
        earned_xp = self.generate_xp()
        print(f"Previous XP: {robot_data['robot_xp']}")
        print(f"Earned XP: {earned_xp}")
        robot_data["robot_xp"] = robot_data["robot_xp"] + earned_xp
        print(f"New XP: {robot_data['robot_xp']}")

        robot.behavior.drive_off_charger()
        winning_numbers = self.lotto_numbers()
        robot_numbers = self.lotto_numbers()

        print(f"Winning Numbers: {winning_numbers}")
        print(f"Robot Numbers: {robot_numbers}")

        robot.behavior.say_text("Match all three numbers exactly to win the jackpot!")
        robot.behavior.say_text(f"The winning numbers are {winning_numbers[0]}, {winning_numbers[1]}, and {winning_numbers[2]}.")
        robot.anim.play_animation_trigger('GreetAfterLongTime', ignore_body_track=True)
        robot.behavior.say_text(f"Good luck!")
        robot.anim.play_animation_trigger("CubePounceGetReady", ignore_body_track=True)

        robot.behavior.say_text(f"Our tickets numbers are {robot_numbers[0]}, {robot_numbers[1]}, and {robot_numbers[2]}")

        if winning_numbers == robot_numbers:
            jackpot_amount = self.get_jackpot()
            robot.anim.play_animation_trigger("BlackJack_VictorBlackJackLose", ignore_body_track=True)
            robot.behavior.say_text(f"We win! Looks like we just won {jackpot_amount} coins! Let me put all these coins in my wallet.")
            for count in range(5):
                print(f"Count: {count}")
                print("Lift down...")
                robot.motors.set_lift_motor(-5)
                time.sleep(0.5)
                print("Lift up")
                robot.motors.set_lift_motor(5)
                time.sleep(0.5)
                count += 1
            robot_data["robot_wallet"] = robot_data["robot_wallet"] + jackpot_amount
            self.write_json_file(filename=self.robot_config_path, data=robot_data)
        else:
            robot.behavior.say_text("We lost! Better luck next time.")
            robot.anim.play_animation_trigger("BlackJack_VictorWin", ignore_body_track=True)
            self.write_json_file(filename=self.robot_config_path, data=robot_data)

    def main(self):
        print("Reading robot config...")
        robot_data = self.read_json_file(self.robot_config_path)
        print("Connecting to the robot...")

        try:
            with anki_vector.Robot(ip=robot_data["ip_address"], escape_pod=True) as robot:
                if self.check_energy_level(robot_data=robot_data):
                    print("Checking for lottery ticket in inventory...")
                    # TODO: Check robot's inventory
                    robot.behavior.say_text("Let me get my lucky coin!")
                    self.do_action(robot_data=robot_data, robot=robot)
                else:
                    robot.behavior.say_text(f"I'm tired, I need {self.required_energy} energy to do that")  
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
    vector = VectorScratchTicket()
    vector.main()