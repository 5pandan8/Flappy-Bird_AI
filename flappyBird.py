import pygame
import neat
import time
import os
import random
pygame.font.init()

GEN = 0

# Setting the dimensions of the window
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Getting the images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

#Setting Font style
STAT_FONT = pygame.font.SysFont('comicsans', 50)

# Making class for each element in game i.e BIRD, BASE, PIPE
class Bird:
    IMGS = BIRD_IMGS
    # The max angle at which the BIRD will tilt
    MAX_ROTATION = 25
    # THe velocity at which the BIRD will tilt
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # The angle at which the Bird will be tilt
        self.tilt = 0
        # How many times we called moves the Bird
        self.tick_count = 0
        # The Velocity at which the Bird is moving in y axis. (The Bird only moves in y axis)
        self.vel = 0
        # The height at which the bird is at
        self.height = self.y
        # What image of bird is currently being displayed
        self.img_count = 0
        # Setting the img of bird to be displayed
        self.img = self.IMGS[0]

    def jump(self):
        # Resetting the number of moves to 0
        self.tick_count = 0
        # Setting the velocity of the jump (negative because we are moving upwards while jumping)
        self.vel = -10.5
        # At what height the bird is at now
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # Getting the distance the bird should move in y-axis only
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2

        # if the distance is too large we need to restrict it to a valid max distance
        if d >= 16:
            d = 16
        # if the distance is too small adjust it too
        if d < 0:
            d -= 2

        # Changing the y position of the bird i.e making it jump
        self.y = self.y + d

        # Setting the correct angle at which the bird will tilt
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        # Incrementing the the number of times bird img changed
        self.img_count += 1
        # Changing to the next image of bird in animation
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If the Bird is falling down Setting the Bird image as the one at index 1
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Actually rotating/ tilting the image of the Bird
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        # Drawing the Image of Bird on the window
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    # The Gap distance between the upper and lower pipe
    GAP = 200
    # The velocity at which the pipes will move in x-axis
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        # Getting the TOP Pipe Image
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        # Getting the BOTTOM Pipe Image
        self.PIPE_BOTTOM = PIPE_IMG
        # Checking if the Bird has passes the pipe
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        # Setting the top left point of the top pipe
        self.top = self.height - self.PIPE_TOP.get_height()
        # Setting the top left point of the bottom pipe
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Getting the distance between the bird and top & bottom pipe respectively
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Checking if the bird overlap with top or bottom pipe
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1

    # List of the neural networks of each bird
    nets = []
    # List of Genomes for each bird
    ge = []
    # List of Birds
    birds = []

    # Setting the Bird, its genomes and its neural network
    # ( "_, g" in for loop because genomes are tuples in format (id, genomes)
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        # fitness value means how well did the bird perform according to our needs
        g.fitness = 0
        ge.append(g)

    score = 0

    base = Base(730)
    pipes = [Pipe(600)]
    # Setting the window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # Setting the clock to get a particular Frame rate
    clock = pygame.time.Clock()

    # Making a game loop which will run at a given Frame rate
    running = True
    while running:
        clock.tick(30)
        # Checking for the event of click on close button on the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # Index of the pipe
        # At most only 2 pipes will be there on the screen so the pipes list will always only have index 0 and 1
        pipe_ind = 0
        if len(birds) > 0:
            # Checking if the bird has passes the pipe at pipe_ind or not
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # Changing pipe_ind to next pipe
                pipe_ind = 1
        else:
            running = False
            break

        # Making the birds move
        for x, bird in enumerate(birds):
            bird.move()

            # Awarding fitness point to birds to have passed a pipe
            # (Because only the birds who have passed the pipe are in the list)
            ge[x].fitness += 0.1

            # Getting the output from the neural network of the bird based on input parameters
            # Input parameters: Bird position, distance from top pipe, distance from bottom pipe
            # Output is to Jump or not
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        # To add a pipe or not
        add_pipe = False
        # List of pipes to remove
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                # if the bird collides with the pipe remove it from all the lists i.e birds, genomes, neural networks
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # Setting the passed value for pipe to True
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Removing the pipe after it has left the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        # Adding the pipe
        if add_pipe:
            score += 1
            # Awarding fitness to bird for successfully passing the pipe
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        # Removing the pipes
        for r in rem:
            pipes.remove(r)

        # Removing the Bird if it has jumped out of screen or fallen out of the screen
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if score > 50:
            break

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):

    # Setting the configurations for the neat algorithm
    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         config_path)

    # Making the population for the neat algorithm
    p = neat.Population(config)

    # Adding the status reporters
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(main, 50)


if __name__ == "__main__":
    # Getting the current directory
    local_dir = os.path.dirname(__file__)
    # Making the path to the config file
    config_path = os.path.join(local_dir, "CONFIG.txt")
    run(config_path)
