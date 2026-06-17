import pygame, sys
from random import randint, uniform # Random interger and floats numbers

class Ship(pygame.sprite.Sprite):
	def __init__(self, groups):
		#1. We have to init the parent class
		super().__init__(groups)
		#2. we need a surface -> is called 'image'
		self.image = pygame.image.load('graphics/ship.png').convert_alpha()
		#3. We need a rectangle
		self.rect = self.image.get_rect(center = (WINDOWS_WIDTH / 2, WINDOWS_HEIGHT/2))
		#4. Creating a mask
		self.mask = pygame.mask.from_surface(self.image)

		self.can_shoot = True
		self.shoot_time = None
	def input_position(self):
		pos = pygame.mouse.get_pos()
		self.rect.center = pos
	def laser_timer(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > 500:
				self.can_shoot = True
	def laser_shoot(self):
		if pygame.mouse.get_pressed()[0] and self.can_shoot:
			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()
			laser = Laser(self.rect.midtop, laser_group)
			laser_sound.play()
	def meteor_collision(self):
		if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
			pygame.quit()
			sys.exit()

	def update(self):
		self.laser_timer()
		self.laser_shoot()
		self.input_position()
		self.meteor_collision()

class Laser(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/laser.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)

		self.mask = pygame.mask.from_surface(self.image)
		# Float based position
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(0,-1)
		self.speed = 600
	def meteor_collision(self):
		if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
			self.kill() #Kill the laser
			explosion_sound.play()
	def update(self):
		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))

		if self.rect.bottom < 0: #Used to kill the laser above the window (less memory are used)
			self.kill()

		self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
	def __init__(self,pos, groups):
		super().__init__(groups)
		meteor_surf = pygame.image.load('graphics/meteor.png').convert_alpha()
		meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.8)
		self.meteor_scaled = pygame.transform.scale(meteor_surf, meteor_size)
		self.image = self.meteor_scaled
		# We can do this in just one line
		# self.image = pygame.transforme.scale(pyagem.image.load('graphics/meteor.png').convert_alpha(), ((randint(50, 100),randint(50,100)))
		self.rect = self.image.get_rect(center = pos)
		
		self.mask = pygame.mask.from_surface(self.image)

		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
		self.speed = randint(300, 700)

		self.rotation = 0
		self.speed_rotation = randint(10, 30)

	def rotate(self):
		self.rotation += self.speed_rotation * dt
		rotated_surf = pygame.transform.rotozoom(self.meteor_scaled, self.rotation,1)
		self.image = rotated_surf
		self.rect = self.image.get_rect(center = self.rect.center)
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.pos += self.direction * self.speed * dt
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))

		if self.rect.top > WINDOWS_HEIGHT: #Used to kill the meteor bellow the window (less memory are used)
			self.kill()

		self.rotate()

class Score():
	def __init__(self):
		self.font = pygame.font.Font('graphics/subatomic.ttf', 20)
	def display(self):
		font_text = f'Score: {pygame.time.get_ticks() // 1000}'
		font_surf = self.font.render(font_text, True, (255,255,255))
		font_rect = font_surf.get_rect(midbottom = (WINDOWS_WIDTH/2, WINDOWS_HEIGHT -20))
		screen_display.blit(font_surf, font_rect)
		pygame.draw.rect(screen_display, (255,255,255), font_rect.inflate(30,20), width = 2, border_radius = 1)

pygame.init()

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
WINDOWS_WIDTH, WINDOWS_HEIGHT = 920, 600

screen_display = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption('Asteroid Rain!')

#Background
background_surface = pygame.image.load('graphics/peakpx2.jpg')

spaceship_group = pygame.sprite.Group()
ship = Ship(spaceship_group)
#spaceship_group.add(ship)
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)

score = Score()

laser_sound = pygame.mixer.Sound('sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
backgound_music = pygame.mixer.Sound('sounds/music.wav')
backgound_music.play(loops = -1)
backgound_music.set_volume(0.8)

while True:

	for event in pygame.event.get():	
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == meteor_timer:
			meteor_x_pos = randint(-100, WINDOWS_WIDTH + 100)
			meteor_y_pos = randint(-150, -50)
			Meteor((meteor_x_pos, meteor_y_pos), meteor_group)

	screen_display.fill((0,0,0))
	dt = clock.tick(60) / 1000
	#Background
	screen_display.blit(background_surface, (0,0))

	spaceship_group.update()
	laser_group.update()
	meteor_group.update()
	
	score.display()

	#Drawing the ship/sprite
	laser_group.draw(screen_display)
	spaceship_group.draw(screen_display)
	meteor_group.draw(screen_display)

	pygame.display.update()