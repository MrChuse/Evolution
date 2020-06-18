from core.game import Game
from draw_utils import *
import sys

FREQUENCY = 30

MAPW = 600
MAPH = 600

W = MAPW + 200
H = MAPH + 40

g = Game()
k = g.field.width
n = g.field.height
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
    print("SIZE SET", H, ":", W)
    #draw_start_menu(background, scr)


def cell_position(i, j, size):
    return i*size, j*size


def draw_start_menu(background, screen, menu=True):
    global g
    start_button = Button(40, 40, 120, 40, text='Start')
    setsize_button = Button(40, 100, 120, 40, text='Set size')
    setsize_button.lock()
    setmapw_inputbox = InputBox(170, 100, 100, 40)
    setmaph_inputbox = InputBox(280, 100, 100, 40)
    uploadgame_button = Button(40, 160, 120, 40, text='upload field')
    # imagine that we need to input a text object to generate a field, than to print it after clicking the button
    worlds = [Button(170 + j*70, 220, 60, 40, text=name, state=False) for j, name in enumerate(g.get_all_world_names())]
    sound_button = Button(40, 220, 120, 40, text='sound')

    buttons = [start_button, setsize_button, uploadgame_button, sound_button]
    inputs = [setmapw_inputbox, setmaph_inputbox]

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
            if uploadgame_button.clicked(event):
                for w in worlds:
                    w.unlock()
                    w.draw(scr)
            for w in worlds:
                if w.state and w.clicked(event):
                    g.load_game_from_file(w.text)
                    set_screen_size(background, screen, MAPW, MAPH)
                    background.fill(WHITE)
                    for button in buttons:
                        button.draw(screen)
                    for box in inputs:
                        box.draw(screen)
            if setsize_button.state and setsize_button.clicked(event):
                if 300 < int(setmapw_inputbox.text) < 1000 and \
                   300 < int(setmaph_inputbox.text) < 1000:
                    set_screen_size(background, screen, int(setmapw_inputbox.text), int(setmaph_inputbox.text))
                    background.fill(WHITE)
                    for button in buttons:
                        button.draw(screen)
                    for box in inputs:
                        box.draw(screen)
            for box in inputs:
                box.input(event)
                box.draw(screen)

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
    global g
    save_world_button = Button(40, 40, 120, 40, text='Save field')
    save_world_inputbox = InputBox(180, 40, 120, 40)
    upload_world_button = Button(40, 90, 120, 40, text='Upload field')
    worlds = [Button(180 + j*70, 90, 60, 40, text=name, state=False) for j, name in enumerate(g.get_all_world_names())]
    setsize_button = Button(40, 140, 120, 40, text='Set size')
    setsize_button.lock()
    setmapw_inputbox = InputBox(180, 140, 100, 40)
    setmaph_inputbox = InputBox(300, 140, 100, 40)
    # change_seed_button = Button(40, 240, 120, 40, text='Change seed')
    continue_button = Button(40, H - 70, 120, 40, text='Continue')

    buttons = [save_world_button, upload_world_button, setsize_button, continue_button]

    input_boxes = [save_world_inputbox, setmapw_inputbox, setmaph_inputbox]
    for button in buttons:
        button.draw(screen)
    for box in input_boxes:
        box.draw(screen)

    while settings:

        background.blit(screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                sys.exit()
            elif continue_button.clicked(event):
                settings = False
            elif setsize_button.state and setsize_button.clicked(event) :
                if 300 < int(setmapw_inputbox.text) < 1000 and \
                   300 < int(setmaph_inputbox.text) < 1000:
                    set_screen_size(background, screen, int(setmapw_inputbox.text), int(setmaph_inputbox.text))
                    background.fill(WHITE)
                    for button in buttons:
                        button.draw(screen)
                    for box in input_boxes:
                        box.draw(screen)

            elif save_world_button.clicked(event):
                g.save_game_to_file(save_world_inputbox.text)
                save_world_inputbox.text = ''
                save_world_inputbox.draw(scr)
            elif upload_world_button.clicked(event):
                for w in worlds:
                    w.unlock()
                    w.draw(scr)
            for w in worlds:
                if w.state and w.clicked(event):
                    g.load_game_from_file(w.text)
                    set_screen_size(background, screen, MAPW, MAPH)
                    settings = False
            for box in input_boxes:
                box.input(event)
                box.draw(screen)

        pygame.display.update()

    scr.fill(WHITE)


def draw_statistics(background, screen, statistics=True):
    num_agents_button = Button(40, 40, 120, 40, text='num_agents')
    gr_surf = pygame.Surface((MAPW, MAPH))
    gr_surf.fill(WHITE)
    bots_energy_button = Button(40, 90, 120, 40, text='bots_energy')
    env_energy_button = Button(40, 140, 120, 40, text='env_energy')
    total_energy_button = Button(40, 190, 120, 40, text='total_energy')
    avg_brain_button = Button(40, 240, 120, 40, text='avg_brain_len')
    max_brain_button = Button(40, 290, 120, 40, text='max_brain_len')

    continue_button = Button(40, H - 70, 120, 40, text='Continue')

    gr_buttons = [num_agents_button, bots_energy_button, env_energy_button, total_energy_button,
               avg_brain_button, max_brain_button]
    buttons = [continue_button]

    global g
    gr_1 = Graphic(0, 0, 380, 140, g.stats['num_agents'], name='num_agents', auto=True)
    gr_2 = Graphic(0, 200, 380, 140, g.stats['bots_energy'], name='bots_energy', auto=True)
    graphics = [gr_1, gr_2]

    for gr in graphics:
        gr.draw(gr_surf)

    for button in buttons:
        button.draw(screen)

    for button in gr_buttons:
        button.draw(screen)

    while statistics:

        background.blit(screen, (0, 0))
        screen.blit(gr_surf, (170, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                statistics = False
                pygame.quit()
                sys.exit()
            elif continue_button.clicked(event):
                statistics = False
            for button in gr_buttons:
                if button.clicked(event) and len(g.stats)>2:
                    gr_surf.fill(WHITE)
                    graphics[0] = graphics[1]
                    graphics[0].rect.move_ip(0, -200)
                    graphics[0].data_update(g.stats[graphics[1].name])
                    graphics[1] = Graphic(0, 200, 380, 140, g.stats[button.text],
                                          name=button.text, auto=True)
                    for gr in graphics:
                        gr.draw(gr_surf)

        pygame.display.update()

    scr.fill(WHITE)


def draw_cell(cell, surface, i, j, temp=False):

    x, y = cell_position(i, j, CELL_SIZE)
    pygame.draw.rect(surface,
                     (cell_color_map[cell.get_cell_type()]) if not temp else temperature_to_color(cell.get_temperature()),
                     (x, y, CELL_SIZE, CELL_SIZE))


def draw_foods(cell_matrix, surface):
    s = max(CELL_SIZE // 5, 2)
    min_surf = pygame.Surface((s, s))
    min_surf.fill(CACTUS)
    meat_surf = pygame.Surface((s, s))
    meat_surf.fill((0, 0, 255))
    for i, line in enumerate(cell_matrix):
        for j, cell in enumerate(line):
            x, y = cell_position(i, j, CELL_SIZE)
            if cell.is_minerals_here():
                surface.blit(min_surf, (x, y))
            if cell.is_meat_here():
                surface.blit(meat_surf, (x + CELL_SIZE - s, y + CELL_SIZE - s))


def draw_agent(agent, surface, energy_mode=False, simple=False):
    x, y = cell_position(agent.pos[0], agent.pos[1], CELL_SIZE)
    if simple:
        agent_surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
        agent_surf.fill((0, 0, 0) if not agent.alive else energy_to_color(agent.energy) if energy_mode else CACTUS)
        surface.blit(agent_surf, (x,y))
    else:
        x += max(CELL_SIZE // 5, 2)
        y += max(CELL_SIZE // 5, 2)
        s = CELL_SIZE - 2 * max(CELL_SIZE // 5, 2)
        agent_surf = pygame.Surface((s, s))
        agent_surf.fill((0, 0, 0) if not agent.alive else energy_to_color(agent.energy) if energy_mode else WHITE)
        if CELL_SIZE > 10 or not energy_mode:
            pygame.draw.rect(agent_surf, (0, 0, 0), (0, 0, s, s), 1)
        surface.blit(agent_surf, (x, y))


def draw_population(agent_list, cell_matrix, surface, eng, simple):
    for agent in agent_list:
        draw_agent(cell_matrix[agent[0]][agent[1]].agent, surface, eng, simple)


def draw_grid(width, surface):
    for x in range(0, CELL_SIZE*(n+1), CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, x), (CELL_SIZE*k, x), width)
    for y in range(0, CELL_SIZE*(k+1), CELL_SIZE):
        pygame.draw.line(surface, GRAY, (y, 0), (y, CELL_SIZE*n), width)


def draw_field(cell_matrix, surface, temp=False, simple=False):
    if simple:
        surface.fill(WHITE)
        draw_grid(1, surface)
    else:
        for i, line in enumerate(cell_matrix):
            for j, cell in enumerate(line):
                draw_cell(cell, surface, i, j, temp)


pygame.init()

background = pygame.display.set_mode((W, H))

scr = pygame.Surface((W, H))
scr.fill(WHITE)

draw_start_menu(background, scr)
scr = pygame.Surface((W, H))
scr.fill(WHITE)
map_surf = pygame.Surface((MAPW, MAPH))
map_surf.fill((255, 255, 255))
action_surf = pygame.Surface((MAPW, MAPH))

temp = False
eng = False
god = False
simple = False
gfx = True

temp_button = Button(30 + MAPW, 10, 55, 40, text='Temp', state=temp)
eng_button = Button(95 + MAPW, 10, 55, 40, text='Eng', state=eng)
god_mode_button = Button(30 + MAPW, 60, 55, 40, text='GOD', state=god)
gfx_button = Button(95 + MAPW, 60, 55, 40, state=gfx, text='GFX')
slowdown_button = Button(30 + MAPW, 110, 40, 40, text='<<<')
pause_button = Button(75 + MAPW, 110, 30, 40, text=' ||')
speedup_button = Button(110 + MAPW, 110, 40, 40, text='>>>')
statistics_button = Button(30 + MAPW, 160, 120, 40, text='Statistics')
#  god kills agents and spawns them
settings_button = Button(30 + MAPW, 210, 120, 40, text='Settings')
simple_button = Button(30 + MAPW, H - 60, 75, 40, state=simple, text='Simple!')
restart_button = Button(110 + MAPW, H - 60, 45, 40, state=simple, text='RST')

buttons = [temp_button, eng_button, slowdown_button, pause_button, speedup_button,
           god_mode_button, settings_button, simple_button, statistics_button, gfx_button, restart_button]
for b in buttons:
    b.draw(scr)

info_block = None
brain_data = None

draw_field(g.field.field, map_surf, temp, simple)
clock = pygame.time.Clock()

life = True
pause = True


while life:

    if not pause:
        g.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            life = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            # visualization modes
            if temp_button.clicked(event):
                temp = not temp
                draw_field(g.field.field, map_surf, temp, simple)
                temp_button.draw(scr)
            elif eng_button.clicked(event):
                eng = not eng
                draw_field(g.field.field, map_surf, temp, simple)
                eng_button.draw(scr)
            elif simple_button.clicked(event):
                simple = not simple
                draw_field(g.field.field, map_surf, temp, simple)
                simple_button.draw(scr)
            elif restart_button.clicked(event):
                g = Game()
                draw_field(g.field.field, map_surf, temp, simple)
            # speed manipulations
            elif slowdown_button.clicked(event):
                if FREQUENCY > 10:
                    FREQUENCY = FREQUENCY / 2
                    if not speedup_button.state:
                        speedup_button.unlock()
                        speedup_button.draw(scr)
                else:
                    slowdown_button.lock()
                    slowdown_button.draw(scr)
            elif speedup_button.clicked(event):
                if FREQUENCY < 2400:
                    FREQUENCY = FREQUENCY * 2
                    if not slowdown_button.state:
                        slowdown_button.unlock()
                        slowdown_button.draw(scr)
                else:
                    speedup_button.lock()
                    speedup_button.draw(scr)
            elif pause_button.clicked(event):
                pause = not pause
                pause_button.draw(scr)
            elif god_mode_button.clicked(event):
                god = not god
                god_mode_button.draw(scr)
            elif settings_button.clicked(event):
                map_surf.fill(WHITE)
                scr.fill(WHITE)
                draw_settings(background, scr)
                for b in buttons:
                    b.draw(scr)
                draw_field(g.field.field, map_surf, temp, simple)
            elif statistics_button.clicked(event):
                map_surf.fill(WHITE)
                scr.fill(WHITE)
                draw_statistics(background, scr)
                for b in buttons:
                    b.draw(scr)
                draw_field(g.field.field, map_surf, temp, simple)
            elif gfx_button.clicked(event):
                gfx = not gfx
                gfx_button.draw(scr)
                if gfx:
                    pygame.draw.rect(scr, WHITE, (10, MAPH + 11, 60, 14))
                else:
                    gfx_srf = pygame.font.SysFont('bahnschrift', 14)
                    gfx_msg = gfx_srf.render('GFX OFF', 0, (255, 0, 0))
                    if info_block:
                        pygame.draw.rect(scr, WHITE, info_block.rect)
                        pygame.draw.rect(scr, WHITE, brain_data.rect)
                        info_block = None
                        brain_data = None
                    scr.blit(gfx_msg, (10, MAPH + 11))
            elif info_block is not None and info_block.button.clicked(event):
                g.save_agent_to_file(info_block.agent)
                info_block.button.unlock()
            elif god and 10 < event.pos[0] < CELL_SIZE*k + 10 and 10 < event.pos[1] < 10 + CELL_SIZE*n:
                x, y = (event.pos[0] - 10)//CELL_SIZE, (event.pos[1] - 10)//CELL_SIZE

                if g.field.field[x][y].agent is not None:
                    g.field.kill_agent((x, y))
                    print('Agent removed')
                else:
                    g.field.spawn_agent((x, y), g.base_brain_settings, brain_type='interpreter')
                    print('Agent born')
                    draw_agent(g.field.field[x][y].agent, action_surf, eng)

            elif 10 < event.pos[0] < CELL_SIZE*k + 10 and 10 < event.pos[1] < 10 + CELL_SIZE*n:
                x, y = (event.pos[0] - 10) // CELL_SIZE, (event.pos[1] - 10) // CELL_SIZE
                if g.field.field[x][y].agent is not None:
                    info_block = InfoBox(g.field.field[x][y].agent, 30 + MAPW, 260, 120, 150)
                    brain_data = BrainData(g.field.field[x][y].agent, MAPW - 250, MAPH + 10)

    if gfx:
        if temp and not simple:
            draw_field(g.field.field, map_surf, temp=True, simple=False)
        action_surf.blit(map_surf, (0, 0))
        draw_population(g.field.q, g.field.field, action_surf, eng, simple)
        if not simple:
            draw_foods(g.field.field, action_surf)

    background.blit(scr, (0, 0))
    background.blit(action_surf, (10, 10))

    if info_block:
        info_block.draw(scr)
        brain_data.draw(scr)

    clock.tick(FREQUENCY)
    pygame.display.update()
