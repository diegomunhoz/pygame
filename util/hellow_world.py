import pygame, time

pygame.init()
window = pygame.display.set_mode((600,300))
myfont = pygame.font.SysFont("Arial", 60)
label = myfont.render("Hellow World", 1, (255,255,0))
window.blit(label, (100,100))
pygame.display.update()
time.sleep(3)
pygame.quit()