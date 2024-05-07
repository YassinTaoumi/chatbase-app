import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load your MP3 file
pygame.mixer.music.load('output.mp3')

# Play the MP3 file
pygame.mixer.music.play()

# Keep the script running until the music is playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
