'''
Created on Dec 7, 2012

@author: Jon

run at codeskulptor.org
http://www.codeskulptor.org/#user7-Ovr2f0jbBSgP3Ht.py


# asteroids
import simplegui
import math
import random

# globals
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False
rock_set = set([])
missile_set = set([])
explosion_set = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim   
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# Ship class
class Ship:
    global missile_set, explosion_set
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.friction = 0.988
        self.fire_speed = 10
        
    def increment_angle_vel(self):
        self.angle_vel += .065
        
    def decrement_angle_vel(self):
        self.angle_vel -= .065
    
    def shoot(self):
        vector = angle_to_vector(self.angle)
        missile_set.add(Sprite([(self.pos[0] + vector[0] * self.radius), (self.pos[1] + vector[1] * self.radius)], \
                           [(self.vel[0] + vector[0] * self.fire_speed), (self.vel[1] + vector[1] * self.fire_speed)], \
                            0, 0, missile_image, missile_info, missile_sound))
        missile_sound.rewind()
        missile_sound.play()
        
    def explode(self):
        explosion_set.add(Sprite(self.pos, [0, 0], self.angle, 0.0, explosion_image, explosion_info, explosion_sound))
    
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        if self.thrust == True:
            vector = angle_to_vector(self.angle)        
            self.vel[0] += vector[0] * 0.2
            self.vel[1] += vector[1] * 0.2
        for missile in list(missile_set):
            if missile.lifespan == None:
                missile.lifespan = 2
            missile.age += 2
            if missile.age >= missile.lifespan:
                missile_set.remove(missile)
        self.vel[0] *= self.friction
        self.vel[1] *= self.friction
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
        self.angle += self.angle_vel    
    

# Sprite class
class Sprite:
    global explosion_set
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
   
    def collide_with(self, item):
        if dist(self.pos, item.pos) <= self.radius + item.radius:
            return True
    
    def explode(self):
        explosion_set.add(Sprite(self.pos, [0, 0], self.angle, 0.0, explosion_image, explosion_info, explosion_sound))
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        if self.pos[0] and self.pos[1]:
            self.pos[0] = (self.pos[0] + self.vel[0]) % width
            self.pos[1] = (self.pos[1] + self.vel[1]) % height
            self.angle += self.angle_vel

           
def draw(canvas):
    global started, time, score, lives, rock_set, missile_set    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])

    # draw status
    canvas.draw_text("Lives", [25, 44], 24, "White")
    canvas.draw_text(str(lives), [25, 73], 24, "White")
    canvas.draw_text("Score", [width - 100, 44], 24, "White")
    canvas.draw_text(str(score), [width - 100, 73], 24, "White")
    
    # draw and track ship and sprites        
    my_ship.draw(canvas)
    for xp in list(explosion_set):
        xp.image_center = [xp.age * xp.image_size[0] + xp.image_center[0], xp.image_center[1]]
        if xp.age > xp.lifespan:
            explosion_set.remove(xp)
        else:
            xp.draw(canvas)
            xp.age += 1
    for rock in list(rock_set):
        rock.draw(canvas)
        if rock.collide_with(my_ship):
            my_ship.explode()
            rock.explode()
            rock_set.remove(rock)
            explosion_sound.rewind()
            explosion_sound.play()
            lives -= 1
    for missile in list(missile_set):
        missile.draw(canvas)
        for rock in list(rock_set):
            if missile.collide_with(rock):
                try:
                    rock.explode()
                    rock_set.remove(rock)
                    missile_set.remove(missile)
                    explosion_sound.rewind()
                    explosion_sound.play()
                    score += 10
                except:
                     continue                            
    
    # update ship and sprites
    my_ship.update()
    for rock in rock_set:
        rock.update()
    for missile in missile_set:
        missile.update()
        
    # game reset
    if lives == 0:
        started = False
        time = 0
        rock_set = set([])
        missile_set = set([])
        soundtrack.pause()
        
    # draw splash screen if not started or game reset
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())
            
# handlers    
def rock_spawner():
    global rock_set
    if len(rock_set) < 12 and started:
        new_rock = Sprite([random.randrange(width), random.randrange(height)], \
                        [random.random() * random.choice([1, -1]) * time / 1000., random.random() * random.choice([1, -1])], \
                        random.random() * 6.283, random.random() * random.choice([0.1, -0.1]), asteroid_image, asteroid_info)
        if not new_rock.collide_with(my_ship):
            rock_set.add(new_rock)
        else:
            rock_spawner()
                     
def keydown(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
        my_ship.image_center = [135, 45]
        ship_thrust_sound.play()
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    if key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()   
    
def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
        my_ship.image_center = [45, 45]
        ship_thrust_sound.rewind()
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    if key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
        
def click(pos):
    global started, lives, score
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        
# initialize
frame = simplegui.create_frame("Asteroids", width, height)
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# startup
timer.start()
frame.start()
'''