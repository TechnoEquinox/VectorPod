# vectormyboi
A companion Python application for the Anki Vector.

Check out the Roadmap for the current development progress. 

robot_config.json and custom_page.html go under wire-pod/chipper/webroot/ to work properly

2 systemd services:
wire-pod.service and vector-flask.service

Art Credits:

QuinqueFive: https://ggbot.itch.io/quinquefive-font (Special Font Assets)

TODO: Find link for Minifarm assets, and find the author of the other assets as well

## Roadmap

### v0.1.0 - **(Completed Dec 30, 2023)**

Show basic proof of concept of the idea. Create an interface to interact with Vector and build a flask service around this. 

### v0.2.0 - **(In Development)**

1. Optimize and clean up the basic structure of the code base.
2. Implement the pipeline and the interface for a shop. The shop can be used to spend coins aquired.
3. Track jogging distance
4. Create a new scratch ticket game. Tickets must be purchased from the shop and can win a lot of coins.
5. Balance fixes
6. Clean up the UI so the text stands out more and so the page is easy to read.

### v0.3.0

1. Add trophies and other food items to the shop.
2. Improve on the inventory system. Create a robot utility that allows Vector to list off all the items he has in his inventory.
3. Add an inventory limit based off of the robot's level. The formula for this should be floor(robot_level * 1.40). Display the intentory limit statistcs in the menu bar
4. Move each section of menu items into a drop down section so unused areas can be hidden and so the user can customize their layout.
5. Add new activities linked to items that can be purchased in the shop.
     a. Dumbells (Strength Training), Book (Intellegence Training), Running Shoes (Speed Training)
     b. Create attributes for the robot. Each attribute should start at their own Level 1 and have their own seperate XP system.
     c. Once the player buys an item, they unlock the training for the attribute that is linked to their skill
     d. The skills can be used for other features in the future, but initally they should directly affect how the robot "Goes to Work"
     e. Player can then expend energy to "train" their robot
7. Add a new activity "Go to work". This activity should have the robot find and move his cube around like he is working at a warehouse.
   a. The robot must purchase the work pass in order to unlock this activity. The work pass should be like 25 coins.
   b. The first time the robot runs this activity, there is an RNG element that will determine their sallery based on their intellegence.
   c. The robot can move a number of "cargo" as determined by their strength attribute
   d. The robot gets paid their sallery per cargo moved based on their intellegence score. The rate at which the robot gets a raise is also affected by the intellegence score.
   e. The robot moves the cargo at a speed determined by the speed score. The robot also can make multiple more trips depending on the level of the speed score.

### v0.4.0

1. Add Farm Plots and Crops to the Shop.
   a. Players can purchase farm plots and then purchase seeds from the shop that can be planted and grown.
   b. Farm plots should be slightly expensive to where the player needs to save up for one. Multiple farm plots should be mid game content. 
3. This update is going to need to contain mutliple different activities related to farming. Will need to figure out how and where to organize all of this in the UI.
4. Different plants will have different grow times and yields. Higher yield plants should have coorisponding seeds that cost more.
5. Crops should be able to be sold in the shop once they are harvested.
6. When checking on the farm plots, vector should display the art of the current grow stage of the plant.
7. Create a hard coded playable space where Vector will reserve for his farm. This may be a little tricky due to the robot's awareness. We could also jsut have vector interact with his cube but this is a little less exciting.


### v0.5.0

1. Add more games like highlow and rock-paper-scissors. (Try and come up with more exciting games too).
2. Add an experimental tab where we can try out new things that aren't an activity or maybe directly related to the vectormyboi main idea.
3. For example, add the ASCI radar maping idea to the experimental tab
4. This release should really be a cleanup update with lots of optimizations, balence changes, and tweeks. After this release, the core gameplay should be ready for production.
5. Improve the battery_manager.py script. I don't know how yet but we should take another pass at it.
6. See if we can create a new section for the global robot stats as shown in wirepod, like total distance traveled, time activited, etc.
7. Rework the visuals with how each of the local robot stats are shown in the custom_page.html. Try doing some kind of rounded horizontal progress bar for the stats that replenish, and then maybe an icon graphic or something
   that changes as the stat improves over time.
8. Add some kind of badge system linked to the robot's level. Display the badge along side the robot's level. The badge art should get cooler as the robot levels up. 

### v1.0.0

1. Create helper shell scripts that will assist with the installation, update, and uninstall process.
2. Prepare the build for production release
3. Add an on-boarding web page that verifies the installation completed successfully, and includes a small tutorial of important information.


### v1.x.x

1. Look into moving the entire UI into a different framework like Vue.js or something. This can also fundamentally change the user experience with different layouts and menus. 
