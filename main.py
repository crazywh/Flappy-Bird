import pygame, os, sys
from pygame.locals import *
from random import *

# 设置窗口打开位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "500, 50"
# 初始化
pygame.init()
size = w, h = 400, 650
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption('Flappy Bird')
FPS = 30

# 定义小鸟类
class Bird(pygame.sprite.Sprite):
	def __init__(self, size):
		super().__init__()
		self.images = [
			pygame.image.load('image/0.png').convert_alpha(),
			pygame.image.load('image/1.png').convert_alpha(),
			pygame.image.load('image/2.png').convert_alpha(),
		]
		self.dead_image = pygame.image.load('image/dead.png').convert_alpha()
		self.index = 0
		self.image = self.images[self.index] 
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = 50, size[1] // 2		
		self.speed = 10
		self.live = True

	def autoMove(self):
		self.rect.top += 1
		if self.rect.right < 200:
			self.rect.right += 1
		else:
			self.rect.right = 200

	def moveUP(self):
		self.rect.top -= self.speed		

class Pipe(pygame.sprite.Sprite):
	def __init__(self, size, flag):
		super().__init__()
		if flag:
			self.image = pygame.image.load('image/top.png').convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.left, self.rect.top = 250, -400
		else:
			self.image = pygame.image.load('image/bottom.png').convert_alpha()
			self.rect = self.image.get_rect()
			self.rect.left, self.rect.bottom = 250, 1050

	def autoMove(self):
		self.rect.left -= 2
		if self.rect.right <= 0:
			self.rect.left = 250





# 加载图片
bg = pygame.image.load('image/background.png').convert_alpha()

def main():
	clock = pygame.time.Clock()
	bird = Bird(size)
	top = Pipe(size, True)
	bottom = Pipe(size, False)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key in [K_w, K_UP]:
					bird.moveUP()

		bird.autoMove()
		top.autoMove()
		bottom.autoMove()
		screen.blit(bg, (0, 0))
		screen.blit(bird.image, bird.rect)
		screen.blit(top.image, top.rect)
		screen.blit(bottom.image, bottom.rect)
		pygame.display.update()
		clock.tick(FPS)

if __name__ == "__main__":
	main()