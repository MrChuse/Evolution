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


def energy_to_color(en):

    d = en/256
    return list(GRAY[i] * (1 - d) + YELLOW[i] * d for i in range(3))


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
        self.stats = ['Eng: ' + str(agent.energy), 'Brn' + str(agent.name)]
        self.stats_surfaces = []
        for stat in self.stats:
            self.stats_surfaces.append(pygame.font.SysFont('bahnschrift', 16).render(stat, True, (0, 0, 0)))
        self.active = True

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        self.stats = ['Eng: ' + str(self.agent.energy), 'Brn' + str(self.agent.name)]
        for k, surf in self.stats_surfaces:
            surf = pygame.font.SysFont('bahnschrift', 14).render(self.stat[k], True, (0, 0, 0))
            screen.blit(surf, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, WHITE, self.rect)

        pygame.draw.rect(screen, self.color, self.rect, 2)