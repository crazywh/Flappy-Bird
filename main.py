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
FPS = 60
font = pygame.font.SysFont('impact', 28)

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
		self.upSpeed = 10
		self.downSpeed = 2
		self.jump = False
		self.live = True

	def move(self):	
		if self.jump:
			self.upSpeed -= 1
			self.rect.top -= self.upSpeed
		else:
			self.downSpeed += 0.2
			self.rect.top += self.downSpeed


class Pipe(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.upPipe = pygame.image.load('image/top.png').convert_alpha()
		self.downPipe = pygame.image.load('image/bottom.png').convert_alpha()
		self.x = 300
		self.upy = -300
		self.downy = 500

	def move(self, score):
		self.x -= 5
		if self.x < -80:
			self.x = 400
			self.upy = randint(-400, -200)
			self.downy = randint(400, 600)
			score += 1
		return score

# 加载图片
bg = pygame.image.load('image/background.png').convert_alpha()

def print_text(font, x, y, text, color = (255,255,255)):
	ti = font.render(text, True, color)
	screen.blit(ti, (x, y))

def main():
	clock = pygame.time.Clock()
	bird = Bird(size)
	pipe = Pipe()
	delay = 0
	score = 0
	running = False

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN and bird.live:
				running = True
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key in [K_w, K_UP]:
					bird.jump = True
					bird.upSpeed = 10
			elif event.type == MOUSEBUTTONDOWN and bird.live:
				bird.jump = True
				bird.upSpeed = 10
		
		if ((bird.rect.top <= pipe.upy + 495 or bird.rect.bottom >= pipe.downy) and bird.rect.right < pipe.x + 98 and bird.rect.left > pipe.x) or bird.rect.top > 650:
			bird.live = False
		
		delay += 1
		if delay > 1000:
			delay = 0
		
		screen.blit(bg, (0, 0))
		screen.blit(bird.image, bird.rect)
		screen.blit(pipe.upPipe, (pipe.x, pipe.upy))
		screen.blit(pipe.downPipe, (pipe.x, pipe.downy))		
		if running:
			if bird.live:
				if not bird.live:
					bird.image = bird.dead_image
				elif bird.jump:
					if delay % 5 == 0:
						bird.index = (bird.index + 1) % 3
					bird.image = bird.images[bird.index]
				bird.move()
				score = pipe.move(score)
				print_text(font, 270, 300, "Score:" + str(score))
			else:
				print_text(font, 140, 250, "Game Over")
				print_text(font, 120, 300, "Your Score is " + str(score))
				print_text(font, 100, 350, "Press R To Restart")
				keys = pygame.key.get_pressed()
				if keys[K_r]:
					main()
				elif keys[K_ESCAPE]:
					pygame.quit()
					sys.exit()
		else:
			print_text(font, 100, 300, "Press Any Key To Start")
		
		pygame.display.update()
		clock.tick(FPS)

if __name__ == "__main__":
	main()