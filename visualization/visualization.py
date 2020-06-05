from core.game import Game, print_map
from draw_utils import *
import sys

FREQUENCY = 30

MAPW = 440
MAPH = 440

W = MAPW + 200
H = MAPH + 40

g = Game()

k = g.field.width
n = g.field.height

g.field.spawn_agent((0, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
g.field.spawn_agent((k - 1, n - 1), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
g.field.spawn_agent((0, n - 1), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
g.field.spawn_agent((k - 1, 0), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')

CELL_SIZE = min(MAPW//k, MAPH//n)


def set_screen_size(background, scr, mapw, maph):
    global MAPH, MAPW, W, H, CELL_SIZE
    MAPH = maph
    MAPW = mapw
    W = MAPW + 200
    H = MAPH + 40
    CELL_SIZE = min(MAPW // k, MAPH // n)
    background = pygame.display.set_mode((W, H))
    scr = pygame.Surface((W, H))
    scr.fill(WHITE)
    print("SIZE SET", H,":",W)
    draw_start_menu(background, scr)


def cell_position(i, j, size):
    return i*size, j*size


def draw_start_menu(background, screen, menu=True):
    start_button = Button(40, 40, 120, 40, text='Start')
    setsize_button = Button(40, 100, 120, 40, text='Set size')
    setsize_button.lock()
    setmapw_inputbox = InputBox(170, 100, 100, 40)
    setmaph_inputbox = InputBox(280, 100, 100, 40)
    setseed_button = Button(40, 160, 120, 40, text='seed')
    uploadfield_button = Button(40, 220, 120, 40, text='upload field')
    # imagine that we need to input a text object to generate a field, than to print it after clicking the button
    uploadfield_inputbox = InputBox(170, 220, 240, 40)
    sound_button = Button(40, 280, 120, 40, text='sound')

    buttons = [start_button, setsize_button, setseed_button, uploadfield_button, sound_button]
    inputs = [uploadfield_inputbox, setmapw_inputbox, setmaph_inputbox]

    screen.fill(WHITE)

    for button in buttons:
        button.draw(screen)
    for box in inputs:
        box.draw(screen)

    while menu:

        background.blit(screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            if start_button.clicked(event):
                menu = False
            if uploadfield_button.clicked(event):
                uploadfield_inputbox.unlock()
            if setsize_button.state and setsize_button.clicked(event):
                set_screen_size(background, screen, int(setmapw_inputbox.text), int(setmaph_inputbox.text))
                setmaph_inputbox.text = ''
                setmaph_inputbox.text = ''

            uploadfield_inputbox.input(event)
            uploadfield_inputbox.draw(screen)

            setmapw_inputbox.input(event)
            setmapw_inputbox.draw(screen)

            setmaph_inputbox.input(event)
            setmaph_inputbox.draw(screen)

        if len(setmaph_inputbox.text) > 0 and len(setmapw_inputbox.text) > 0:
            if not setsize_button.state:
                setsize_button.unlock()
                setsize_button.draw(screen)
                pygame.display.update()
        elif setsize_button.state:
            setsize_button.lock()
            setsize_button.draw(screen)

        pygame.display.update()
    screen.fill(WHITE)


def draw_settings(background, screen, settings=True):
    save_field_button = Button(40, 40, 120, 40, text='Save field')
    upload_field_button = Button(40, 90, 120, 40, text='Upload field')
    save_population_button = Button(40, 140, 160, 40, text='Save population')
    upload_population_button = Button(40, 190, 160, 40, text='Upload population')
    change_seed_button = Button(40, 240, 120, 40, text='change seed')
    continue_button = Button(40, 290, 120, 40, text='Continue')

    buttons = [save_field_button, upload_field_button, save_population_button, upload_population_button,
               change_seed_button, continue_button]

    for button in buttons:
        button.draw(screen)

    while settings:

        background.blit(screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            if continue_button.clicked(event):
                settings = False

        pygame.display.update()


def draw_cell(cell, surface, i, j, temp=False):

    x, y = cell_position(i, j, CELL_SIZE)
    pygame.draw.rect(surface,
                     (cell_color_map[cell.get_cell_type()]) if not temp else temperature_to_color(cell.get_temperature()),
                     (x, y, CELL_SIZE, CELL_SIZE))
    if cell.is_food_here():
        draw_food(cell, surface, i, j)


def draw_food(cell, surface, i, j):
    x, y = cell_position(i, j, CELL_SIZE)
    pygame.draw.rect(surface, (food_color_map[cell.get_cell_type]), (x, y, max(CELL_SIZE//5, 2), max(CELL_SIZE//5, 2)))


def draw_fake_agent(agent, surface, energy_mode=False, simple=False):
    x, y = cell_position(agent.pos[0], agent.pos[1], CELL_SIZE)
    if simple:
        pygame.draw.rect(surface, CACTUS if not energy_mode else energy_to_color(agent.energy), (x, y, CELL_SIZE, CELL_SIZE))
    else:
        x += max(CELL_SIZE // 5 + 1, 2)
        y += max(CELL_SIZE // 5 + 1, 2)
        if CELL_SIZE > 10:
            pygame.draw.rect(surface, (0, 0, 0), (x-1, y-1, CELL_SIZE // 5*3 + 2, CELL_SIZE // 5*3 + 2))
        pygame.draw.rect(surface, WHITE if not energy_mode else energy_to_color(agent.energy), (x, y, CELL_SIZE//5*3, CELL_SIZE//5*3))


def draw_grid(width, surface):
    for x in range(0, CELL_SIZE*(n+1), CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, x), (CELL_SIZE*k, x), width)
    for y in range(0, CELL_SIZE*(k+1), CELL_SIZE):
        pygame.draw.line(surface, GRAY, (y, 0), (y, CELL_SIZE*n), width)


def draw_field(agent_list, agent_matrix, cell_matrix, surface, temp=False, eng=False, simple=False):
    if simple:
        surface.fill(WHITE)
        draw_grid(1, surface)
        for agent in agent_list:
            draw_fake_agent(agent_matrix[agent[0]][agent[1]], surface, eng, True)
    else:
        for i, line in enumerate(cell_matrix):
            for j, cell in enumerate(line):
                draw_cell(cell, surface, i, j, temp)
        for agent in agent_list:
            draw_fake_agent(agent_matrix[agent[0]][agent[1]], surface, eng, False)

pygame.init()

background = pygame.display.set_mode((W, H))

scr = pygame.Surface((W, H))
scr.fill(WHITE)

draw_start_menu(background, scr)
scr = pygame.Surface((W, H))
scr.fill(WHITE)
map_surf = pygame.Surface((MAPW + 1, MAPH + 1))
map_surf.fill((255, 255, 255))

temp = False
eng = False
god = False
simple = False

temp_button = Button(30 + MAPW, 10, 120, 40, text='Temperature', state=temp)
temp_button.draw(scr)

eng_button = Button(30 + MAPW, 60, 120, 40, text='Energy', state=eng)
eng_button.draw(scr)

slowdown_button = Button(30 + MAPW, 110, 40, 40, text='<<<')
pause_button = Button(75 + MAPW, 110, 30, 40, text=' ||')
speedup_button = Button(110 + MAPW, 110, 40, 40, text='>>>')

slowdown_button.draw(scr)
pause_button.draw(scr)
speedup_button.draw(scr)

god_mode_button = Button(30 + MAPW, 160, 120, 40, text='GOD MODE', state=god)
#  god kills agents and spawns them
god_mode_button.draw(scr)

settings_button = Button(30 + MAPW, 210, 120, 40, text='Settings')
settings_button.draw(scr)

simple_button = Button(30 + MAPW, 420, 120, 40, state=simple, text='Simple!')
simple_button.draw(scr)

info_block = None

draw_field(g.field.q, g.field.agents, g.field.field, map_surf, temp, eng, simple)
clock = pygame.time.Clock()

life = True
pause = True

while life:
    background.blit(scr, (0, 0))
    background.blit(map_surf, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            life = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            # visualization modes
            if temp_button.clicked(event):
                temp = not temp
                temp_button.draw(scr)

            if eng_button.clicked(event):
                eng = not eng
                eng_button.draw(scr)

            if simple_button.clicked(event):
                simple = not simple
                simple_button.draw(scr)

            # speed manipulations
            if slowdown_button.clicked(event):
                if FREQUENCY > 1:
                    FREQUENCY = FREQUENCY / 2
                    if not speedup_button.state:
                        speedup_button.unlock()
                        speedup_button.draw(scr)
                else:
                    slowdown_button.lock()
                    slowdown_button.draw(scr)
            if speedup_button.clicked(event):
                if FREQUENCY < 1200:
                    FREQUENCY = FREQUENCY * 2
                    if not slowdown_button.state:
                        slowdown_button.unlock()
                        slowdown_button.draw(scr)
                else:
                    speedup_button.lock()
                    speedup_button.draw(scr)
            if pause_button.clicked(event):
                pause = not pause
                pause_button.draw(scr)
            if god_mode_button.clicked(event):
                god = not god
                god_mode_button.draw(scr)
            if settings_button.clicked(event):
                map_surf.fill(WHITE)
                draw_settings(background, scr)
                draw_field(g.field.q, g.field.agents, g.field.field, map_surf, temp, eng, simple)
            elif god and 10 < event.pos[0] < CELL_SIZE*k + 10 and 10 < event.pos[1] < 10 + CELL_SIZE*n:
                x, y = (event.pos[0] - 10)//CELL_SIZE, (event.pos[1] - 10)//CELL_SIZE

                if g.field.agents[x][y] is not None:
                    g.field.kill_agent((x, y))
                    print('Agent removed')
                else:
                    g.field.spawn_agent((x, y), (((0, True), (2, True), (2, True)), 10, set()), 100, 255, 1, 'random')
                    print('Agent born')

                    draw_fake_agent(g.field.agents[x][y], map_surf, eng)
                    pygame.display.update()
            elif 10 < event.pos[0] < CELL_SIZE*k + 10 and 10 < event.pos[1] < 10 + CELL_SIZE*n:
                x, y = (event.pos[0] - 10) // CELL_SIZE, (event.pos[1] - 10) // CELL_SIZE
                if g.field.agents[x][y] is not None:
                    info_block = InfoBox(g.field.agents[x][y], 30 + MAPW, 260, 120, 150)

    if info_block:
        info_block.draw(scr)

    if not pause:
        #print_map(g)
        g.update()

    clock.tick(FREQUENCY)
    draw_field(g.field.q, g.field.agents, g.field.field, map_surf, temp, eng, simple)
    pygame.display.update()
