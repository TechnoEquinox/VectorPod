#!/usr/bin/env python3

import anki_vector
from anki_vector.util import degrees
import grpc
from grpc._channel import _MultiThreadedRendezvous
import os
import time
from vector_helpers import VectorHelpers
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

class VectorDrinkEnergy():
    def __init__(self):
        self.required_energy: int = 0
        self.helpers = VectorHelpers()
    
    def do_action(self, robot_data, robot):
        robot_data["robot_energy_level"] = robot_data["robot_energy_level"] - self.required_energy

        robot.behavior.drive_off_charger()
        robot.behavior.set_head_angle(degrees(45.0))
        image_path = os.path.join(os.path.expanduser("~"), 'wire-pod/chipper/plugins/vectormyboi/VectorConfig/face_images/can_14.png')
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        robot.screen.set_screen_with_image_data(screen_data, 3.0)
        time.sleep(0.25)
        
        sound_path = os.path.join(os.path.expanduser("~"), 'wire-pod/chipper/plugins/vectormyboi/VectorConfig/sounds/vector_bell_whistle.wav')
        robot.audio.stream_wav_file(sound_path, 75)
        time.sleep(2.0)

        robot.anim.play_animation_trigger('GreetAfterLongTime', ignore_body_track=True)

        robot_data["robot_energy_level"] = robot_data["robot_energy_level"] + 50.0
        self.helpers.write_json_file(data=robot_data)

        earned_xp = self.helpers.generate_xp(1, 1)
        print(f"Earned XP: {earned_xp}")
        robot.behavior.say_text(f"Oh. I also gained {earned_xp} experience point.")
        self.helpers.update_xp_and_check_level(earned_xp, robot)

    def main(self):
        print("Reading robot config...")
        robot_data = self.helpers.read_json_file()
        print("Connecting to the robot...")

        try:
            with anki_vector.Robot(ip=robot_data["ip_address"], escape_pod=True) as robot:
                if self.helpers.check_energy_level(self.required_energy):
                    energy_drink_id = 2
                    if energy_drink_id in robot_data["items"]:
                        print("Energy drink found in inventory.")
                        robot_data["items"].remove(energy_drink_id)
                        robot.behavior.say_text("Drink up!")
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
    vector = VectorDrinkEnergy()
    vector.main()