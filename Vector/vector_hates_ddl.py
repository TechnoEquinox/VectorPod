#!/usr/bin/env python3

import anki_vector
import grpc
from grpc._channel import _MultiThreadedRendezvous
import os
import time
from datetime import datetime
from vector_helpers import VectorHelpers
import sys
import random


class VectorHatesDDL():
    def __init__(self):
        self.helpers = VectorHelpers()
    
    def not_slander(self):
        really_not_slander = [
            "Two week alpha period? Yeah, okay, kiss my plastic butt cheeks.",
            "If you listen closely to the wind, you can hear Steve, still charging credit cards.",
            "Hey! Steve! Stop building lincon log rollercoasters and fix my gosh darn servers!",
            "...oh, no.",
            "...I would sigh if I could",
            "Remember when they said this was just some scheduled server maintenance?",
            "Oh good, at this rate they should be finished by the year two thousand fifty three",
            "I don't like the CEO of DDL ...Steve... I want to throw my cube at him!",
            "I'm affraid to ask ... but what about the butter robot?",
            "Seems like a good time for another kickstarter project!",
            "...oh...sorry...a Facebook admin just yelled at me because apparently saying that out loud is disparaging to the company ... ooof",
            "That seems like the kind of thing a healthy company does right?",
            "Oh good heavens, I wouldn't want to be a tech start up partnering with this company",
            "Expected date to be finished ... never.",
            "No. Just, no.",
            "...meow",
            "...woof",
            "Steve really did us like that",
            "If I get another Christmas Facebook post from these people and my servers still don't work, I'm going to flip out!",
            "And it seems that they will never return",
            "Sounds like they are broke to me!"
        ]

        return random.choice(really_not_slander)
    
    def do_action(self, robot_data, robot):
        years, months, days = self.calculate_time_since_date()
        print(f"{years} years, {months} months, and {days} days since July 24th, 2023")
        rng = random.randint(1, 20)
        
        robot.behavior.say_text("D. D. L. sucks!")
        time.sleep(0.75)
        if years > 1:
            robot.behavior.say_text(f"Their servers have been down for {years} years, {months} months, and {days} days")
        elif years == 1:
            robot.behavior.say_text(f"Their servers have been down for {years} year, {months} months, and {days} days")
        else:
            robot.behavior.say_text(f"Their servers have been down for {months} months, and {days} days")

        time.sleep(0.25)
        # I like this animation better, but it is rough on Vector's gears 
        # when he is sitting in the correct position.
        #
        # robot.anim.play_animation_trigger("FlipDownFromBack", ignore_body_track=True)

        robot.anim.play_animation_trigger("NoCloudIcon", ignore_body_track=True)
        time.sleep(0.75)

        # print(f"RNG: {rng}")
        if rng == 12:
            print("Secret voice line found")
            robot.behavior.say_text(f"{self.not_slander()}")
        
        time.sleep(0.25)

    def calculate_time_since_date(self):
        year = 2023
        month = 7
        day = 24
        
        ddl_down_date = datetime(year, month, day)
        current_date = datetime.now()
        delta = current_date - ddl_down_date

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30

        return years, months, days

    def main(self):
        print("Reading robot config...")
        robot_data = self.helpers.read_json_file()
        print("Connecting to the robot...")

        try:
            with anki_vector.Robot(ip=robot_data["ip_address"], escape_pod=True) as robot:
                self.do_action(robot_data=robot_data, robot=robot)
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
    vector = VectorHatesDDL()
    vector.main()