import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN
)
from pygame.rect import Rect
from random import shuffle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#comment
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.music.load('Rhythm.mp3')
pygame.mixer.music.play(loops=-1)
win_point = pygame.mixer.Sound("Sounds/coins_dropped_1.ogg")
click = pygame.mixer.Sound("Sounds/click_cancel_china.wav")


def select(box_list, xpos, ypos):
    for b in box_list:
        if b.rect.collidepoint(xpos, ypos):
            screen.blit(b.image2, (b.rect.x, b.rect.y))
            return b


class Box(object):
    SIZE = 64

    def __init__(self):
        self.code = None
        self.enabled = True
        self.image = pygame.Surface((64, 64))
        self.image.fill((185, 239, 225))
        self.rect = None
        self.image2 = None


boxes = [Box() for i in range(42)]
food_icons = [
    'Food_Icons/apple.png',
    'Food_Icons/bread-egg.png',
    'Food_Icons/carrot.png',
    'Food_Icons/cheeseburger.png',
    'Food_Icons/cherries.png',
    'Food_Icons/cookie.png',
    'Food_Icons/donut.png',
    'Food_Icons/french-fries.png',
    'Food_Icons/fried-chicken.png',
    'Food_Icons/grapes.png',
    'Food_Icons/hotdog.png',
    'Food_Icons/ice-cupcake.png',
    'Food_Icons/lemon.png',
    'Food_Icons/macaron-cookies.png',
    'Food_Icons/pear.png',
    'Food_Icons/pizza.png',
    'Food_Icons/popcorn.png',
    'Food_Icons/sliced-pizza.png',
    'Food_Icons/soft-ice-cream.png',
    'Food_Icons/strawberry-magnum.png',
    'Food_Icons/vanilla-cupcake.png',
]

indexes = [i for i in range(21) for _ in range(2)]
shuffle(indexes)
counter = 0

screen.fill((0, 0, 0))

MARGIN = 6
x = boxes[0].SIZE + MARGIN
y = boxes[0].SIZE + MARGIN
r = 0

for box in boxes:
    box.rect = Rect(x, y, boxes[0].SIZE, boxes[0].SIZE)
    food = food_icons[indexes[counter]]
    box.code = indexes[counter]
    box.image2 = pygame.transform.scale(pygame.image.load(food), (box.SIZE, box.SIZE))
    screen.blit(box.image, (x, y))
    if r == 6:
        x = boxes[0].SIZE + MARGIN
        y += boxes[0].SIZE + MARGIN
        r = 0
    else:
        x += boxes[0].SIZE + MARGIN
        r += 1
    counter += 1

running = True
choice1 = None
choice2 = None
flip = pygame.USEREVENT + 1
pygame.time.set_timer(flip, 4000)

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        if event.type == flip:
            print(event)
            if choice1 is not None and choice2 is not None:
                if choice1.enabled:
                    screen.blit(choice1.image, (choice1.rect.x, choice1.rect.y))
                    choice1 = None
                if choice2.enabled:
                    screen.blit(choice2.image, (choice2.rect.x, choice2.rect.y))
                    choice2 = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if choice1 is None:
                choice1 = select(boxes, x, y)
                if isinstance(choice1, Box):
                    pygame.mixer.Sound.play(click)
                    print(choice1.code)
                    screen.blit(choice1.image2, (choice1.rect.x, choice1.rect.y))
            elif choice2 is None:
                choice2 = select(boxes, x, y)
                if isinstance(choice2, Box):
                    pygame.mixer.Sound.play(click)
                    print(choice2.code)
                    screen.blit(choice2.image2, (choice2.rect.x, choice2.rect.y))
                    if choice1.code == choice2.code and choice1 != choice2 \
                            and choice1.enabled and choice2.enabled:
                        print("1 point")
                        pygame.mixer.Sound.play(win_point)
                        choice1.enabled = False
                        choice2.enabled = False
                        choice1 = None
                        choice2 = None

    pygame.display.flip()
    clock.tick(60)
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
quit()
