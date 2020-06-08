import pygame

# Our beautiful colours
SAND = (255, 255, 204)
ROCK = (128, 128, 128)
LEAVES = (0, 102, 51)
GRASS = (153, 204, 51)
WATER = (153, 255, 255)
BLACK = (0, 0, 0)

CACTUS = (0, 102, 51)
WHEAT = (255, 255, 2)
APPLE = (255, 0, 0)
FLOWER = (153, 51, 102)
FISH = (245, 156, 51)

# Temperature color map
BLUE = (0, 51, 15_3)
ORANGE = (255, 102, 0)
WHITE = (255, 255, 255)


def temperature_to_color(temp):

    d = abs(temp/64)
    if temp > 0:
        return list(WHITE[i] * (1 - d) + ORANGE[i] * d for i in range(3))
    else:
        return list(WHITE[i] * (1 - d) + BLUE[i] * d for i in range(3))


# Energy color map
GRAY = (128, 128, 128)
YELLOW = (255, 204, 0)
RED = (255, 0, 0)


def energy_to_color(en):

    d = en/256
    if en < 256:
        return list(GRAY[i] * (1 - d) + YELLOW[i] * d for i in range(3))
    else:
        d = en/1024
        return list(YELLOW[i] * (1 - d) + RED[i] * d for i in range(3))



cell_color_map = {4: ROCK,
                  3: SAND,
                  2: GRASS,
                  1: LEAVES,
                  0: WATER}

food_color_map = {4: WHEAT,
                  3: CACTUS,
                  2: FLOWER,
                  1: APPLE,
                  0: FISH}


class Button:
    def __init__(self, x, y, w, h, text='Button', state=True):
        self.rect = pygame.Rect((x, y, w, h))
        self.text = text
        self.txt_surface = pygame.font.SysFont('bahnschrift', 18).render(text, True, (0, 0, 0))
        self.state = state
        self.color = GRASS if self.state else GRAY

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                self.color = GRASS if self.state else GRAY
                return True
        return False

    def unlock(self):
        self.state = True
        self.color = GRASS

    def lock(self):
        self.state = False
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = pygame.font.SysFont('bahnschrift', 18).render(text, True, (0, 0, 0))
        self.active = True

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = GRASS if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = pygame.font.SysFont('bahnschrift', 18).render(self.text, True, (0, 0, 0))

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def unlock(self):
        self.active = True
        self.color = GRASS

    def lock(self):
        self.active = False
        self.color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class InfoBox:
    def __init__(self, agent, x, y, w, h, state=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.agent = agent
        self.color = GRAY
        self.stats = ['Eng: ' + str(agent.energy),
                      'maxEng: ' + str(agent.energy_cap),
                      'Brn: ' + str(agent.name),
                      'Rad: ' + str(agent.radius)]
        self.button = Button(x + 5, y + h - 40, w - 10, 35, text='Save')
        self.stats_surfaces = []
        for stat in self.stats:
            self.stats_surfaces.append(pygame.font.SysFont('bahnschrift', 14).render(stat, True, (0, 0, 0)))

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        self.stats = ['Eng: ' + str(self.agent.energy),
                      'maxEng: ' + str(self.agent.energy_cap),
                      'Brn: ' + str(self.agent.name),
                      'Rad: ' + str(self.agent.radius)]
        for k, surf in enumerate(self.stats_surfaces):
            surf = pygame.font.SysFont('bahnschrift', 14).render(self.stats[k], True, (0, 0, 0))
            screen.blit(surf, (self.rect.x + 5, self.rect.y + 5 + k*20))
        self.button.draw(screen)
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Graphic:
    def __init__(self, x, y, w, h, data, dynamic=False, name='', auto=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.name=name
        self.max = 1024
        self.min = 0
        self.step = 1
        if auto and len(data) > 1:
            self.set_size_auto(data)
        self.points = [[i*w//len(data) + x, y + h - data[i]*h//self.max] for i in range(0, len(data), self.step)]

    def data_update(self, data):
        self.points = [[i * self.rect.w // len(data)+ self.rect.x, self.rect.y + self.rect.h - data[i] * self.rect.h // self.max]
                       for i in range(0, len(data), self.step)]

    def set_max(self, m):
        self.max = m

    def set_min(self, m):
        self.min = m

    def set_step(self, st):
        self.step = st

    def set_size_auto(self, data):
        self.set_max(max(data) + 10)
        self.set_min(min(data) - 10)
        self.set_step(max((len(data)//self.rect.w//30), 1))

    def draw(self, scr, data=None):
        if data is not None:
            self.data_update(data)
        pygame.draw.rect(scr, WHITE, self.rect)
        pygame.draw.rect(scr, BLACK, self.rect, 2)
        if len(self.points) > 2:
            pygame.draw.aalines(scr, RED, False, self.points, 3)
        num = pygame.font.SysFont('bahnschrift', 12)
        max = num.render(str(self.max - 10), 0, (0, 0, 0))
        min = num.render(str(self.min + 10), 0, (0, 0, 0))
        scr.blit(max, (self.rect.x + self.rect.w + 5, self.rect.y))
        scr.blit(min, (self.rect.x + self.rect.w + 5, self.rect.y + self.rect.h - 12))
        if len(self.name) > 0:
            name = num.render(self.name, 0, (0, 0, 255))
            scr.blit(name, (self.rect.x, self.rect.y + self.rect.h + 2))