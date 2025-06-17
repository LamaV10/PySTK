# Supertuxkart but for elitist

List of Celebs using Chinastk:

- Eis Würfel

- Einfaches E

- Kleiner am Netzwerk Angeschlossener Speicher X

- Enkelsohn

# Characters 

![chevyss-yoshi](https://github.com/user-attachments/assets/fdd368eb-90c9-4445-b6c0-d3bd83e1f50d)
![ferrari-rossa-tux](https://github.com/user-attachments/assets/963273f2-2bfd-46e5-966d-cc62510a3c66)

# Requirements

- Python with all the needed dependencies installed (see requirements.txt)
```
pip install -r requirements.txt
```
- Bash (to be able to execute the .sh files, which make the usage a bit easier(optional))

# Usage

If all the Requirements are fulfilled just execute "play.sh". 
If you cannot execute a .sh file because of your OS, go into Source/bin/ and execute the PySTK file.
The rest should be self explenatory.

# Music

In order to get music setup in the game, you can execute the musicSetup.sh script.
Then you can enter the location of your file (mp3 should always work).

For example:

```
/home/Bruno/Music/Easy.mp3
```

If this script doesn't work (because of a bug or a different OS) you have to manually modify the path in the music.py file in Line 11,
which is located in Source/bin/.

Example:

```
mixer.music.load('/home/Bruno/Music/YOUR_TITEL.mp3')
```
# Honorable Mentions 
shoutout to @CrazyPlayer7595 for starting this project (sending code back and forth over discord)
