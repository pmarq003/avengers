import pygame.mixer

pygame.mixer.init()
bgm = pygame.mixer.Channel(0)
sfx = pygame.mixer.Channel(1)

def get_sfx():
    return sfx

def get_bgm():
    return bgm

def play_bgm(sound_path):
    snd = pygame.mixer.Sound(sound_path)
    bgm.play(snd, -1)

def play_sfx(sound_path):
    snd = pygame.mixer.Sound(sound_path)
    sfx.play(snd)

def set_bgm_vol(vol):
    bgm.set_volume(vol/100.0)

def set_sfx_vol(vol):
    sfx.set_volume(vol/100.0)

def get_bgm_vol():
    return int(bgm.get_volume()*100)

def get_sfx_vol():
    return int(sfx.get_volume()*100)