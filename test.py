from gtts import gTTS
import pygame

def parler(texte):
    tts = gTTS(texte, lang='fr')
    tts.save("response.mp3")
    play_mp3("response.mp3")

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Utilisez la fonction pour lire un fichier MP3
if __name__ == "__main__":
    play_mp3("response.mp3")
