# Spotipi-Matrix
A modified version of Ryan Ward's Spotipi project using a Raspberrypi Zero 2 w
Project: https://www.youtube.com/watch?v=6i8kzqvh94E&t=95s
### Getting Started
### NOTE: Make sure you have a pi zero/ zero 2(w) with a rgb matrix 64x64 with a soldered bonnet
* Create a new application within the [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications) <br />
* Edit the settings of the application within the dashboard.
    * Set the redirect uri to any local url such as http://127.0.0.1/callback
    * NOTE: You will use this to access your website
### Creating a idle picture
* To create a picture when you are not listening to anything, you are going to scp a photo from your computer
* To do this, go to your terminal
* Next use ```scp {NOTE: a shortcut for directory is to drag the picture into the terminal}```
```
scp path_of_photo your_username@raspberrypi.local:raspberrpi_program_directory
```
* NOTE: You will need to remember the name of the photo to change a constant in the program later on. EX: Image1.png
### Creating the main program
* First step is to ssh to your raspberry pi
* Use:
```
ssh insert_your_username@raspberrypi.local
```
in your terminal to ssh into your raspberrypi
* Find a directory to put your code in (/Videos,/Home, ect)
* NOTE: use ```cd insert_your_directory``` to switch directories and ```ls``` to look at the files in that directory
* Once you have found the directory you want your code in, make a nano file for the main program
   * To do this, use ```sudo nano insert_your_filename.py```
* Now paste in this code
   * (spotipi main code) ```use file MainSpotipi.py above to access the code```
* NOTE: To paste in nano, use ctrl + U
* When you finish pasting in the code, be sure to change the Client ID and Secret on lines 25-26
* Also change line 101 to the correct name of the idle picture in your directory
   * ex: default_image_path = 'your_Image.png' 
### Creating a webflask app
* paste this into your raspberrypi terminal:
```
pip3 install flask
```
* Now that we have installed webflask, we are going to make a file to paste the HTML code to make the website neat
* Make sure you are in the same directory as the main program
* Now in the same directory as your main program, make a file named templates
* To do this use:
```
mkdir templates
```
* cd into the new file "templates"
* Inside the file, you're gonna make another file named "index.html"
* To do this use:
```
sudo nano index.html
```
* and paste in this code:
```
use file index.html above to access the code
```
   * REMEMBER: use ctrl + U in nano to paste
### Creating the webcontrols
* In the same directory as the main program and webflask app, you're gonna make another file controling the website
* To do this use: ```sudo nano insert_your_filename.py```
* Then paste this code into that file:
```
use file webcontrols.py above to access the code
```
* NOTE: Change your Client ID, Secret, and redirect URI on lines 10-12
* NOTE: Change your path to the name of the file of the main program on line 64
   * ex: script_path = 'INSERT_MAIN_PROGRAM_PATH.py'

### Running the program
* Once you have finished all the steps you're gonna run the program
* Make sure you are on the same directory as the programs to execute
* Use ```sudo python3 yourwebcontrolfile.py```
* Once you have run the program, go to your web browser and type in your URI link
* This should bring you to the website that has the controls
* You want to click authorize with spotify which will redirect you
* Copy the link you were redirected to and paste it into prompt and submit it
* Now click start script and it should work
### Maintaining the program
* Everytime you ssh into your raspberrypi, you have to cd into the directory and use ```sudo python3 yourwebcontrolfile.py``` to run the program, then you can open the website
* Every hour, a new token will generate and you will have to redo the authorizing process again.


