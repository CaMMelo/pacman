import pygame

import grid
import pacman
import ghost
import config
import globals

CHANGESTATEEVENT = pygame.USEREVENT + 1

class Game:

    ghosts_state = ghost.CHASE
    ghost_value = 200

    def __init__(self):

        self.grid   = grid.Grid()
        self.pacman = pacman.Pacman((13, 26), 0, 0)

        self.blinky = ghost.Blinky((13, 14), 0, 0)
        self.inky   = ghost.Inky((13, 14), 0, 0)
        self.pinky  = ghost.Pinky((13, 14), 0, 0)
        self.clyde  = ghost.Clyde((13, 14), 0, 0)

        self.ghosts = pygame.sprite.Group()

        self.ghosts.add(self.blinky)
        self.ghosts.add(self.inky)
        self.ghosts.add(self.pinky)
        self.ghosts.add(self.clyde)

        pygame.time.set_timer(CHANGESTATEEVENT, self.ghosts_state * 1000)

    def reset_positions(self):
        ''' reset all character positions '''

        self.pacman.reset((13, 26), 4, 0, 0)

        for g in self.ghosts:
            g.reset((13, 14), ghost.FAST, 0, 0)

    def game_over(self, screen):
        ''' draw game over screen '''

        text = globals.FONT.render('GAME OVER', True, (255,0,0))
        pos = (config.SCREEN_SIZE[0] // 2 - text.get_width() // 2, 19.8 * config.TILE_SIZE)
        screen.blit(text, pos)

    def victory(self, screen):
        ''' draw victory screen '''
        
        text = globals.FONT.render('YOU WON!!', True, (0,0,255))
        pos = (config.SCREEN_SIZE[0] // 2 - text.get_width() // 2, 19.8 * config.TILE_SIZE)
        screen.blit(text, pos)

    def draw_lifes(self, screen):

        start = (1, 34.3)
        screen_pos = [start[0]*config.TILE_SIZE, start[1]*config.TILE_SIZE]

        for l in range(0, self.pacman.lives - 1):

            screen.blit(globals.PACMAN_SPRITES[0][0][0], screen_pos)
            screen_pos[0] += config.TILE_SIZE*2

    def draw_score(self, screen):

        text = globals.FONT.render('SCORE', True, (255,255,255))
        pos = (config.SCREEN_SIZE[0] // 2 - text.get_width() // 2, 0)
        screen.blit(text, pos)

        text = globals.FONT.render(str(self.pacman.score), True, (255,255,255))
        pos = (config.SCREEN_SIZE[0] // 2 - text.get_width() // 2, config.TILE_SIZE)
        screen.blit(text, pos)


    def change_ghosts_state(self, spill = False):

        speed = ghost.FAST
        self.ghost_value = 200

        if spill:

            state = ghost.FRIGHTENED
            speed = ghost.SLOW

        else:

            if self.ghosts_state == ghost.CHASE:
                self.ghosts_state = ghost.SCATTER
                state = ghost.SCATTER
            else:
                self.ghosts_state = ghost.CHASE
                state = ghost.CHASE

        for g in self.ghosts:
            g.speed = speed
            g.state = state

        pygame.time.set_timer(CHANGESTATEEVENT, self.ghosts_state * 1000)

    def loop(self, screen):

        running = True

        clock = pygame.time.Clock()

        while running:

            clock.tick(60)

            keys = pygame.key.get_pressed()

            if pygame.event.get(CHANGESTATEEVENT):
                self.change_ghosts_state()

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:

                    running = False

            if keys[pygame.K_DOWN]:
                self.pacman.update_way(self.grid.grid, globals.DOWN)
            if keys[pygame.K_UP]:
                self.pacman.update_way(self.grid.grid, globals.UP)
            if keys[pygame.K_RIGHT]:
                self.pacman.update_way(self.grid.grid, globals.RIGHT)
            if keys[pygame.K_LEFT]:
                self.pacman.update_way(self.grid.grid, globals.LEFT)

            screen.fill((30,30,30,0))

            if self.pacman.consume_pellet(self.grid.grid):
                self.change_ghosts_state(True)

            # check collisions

            ghosts = pygame.sprite.spritecollide(self.pacman, self.ghosts, False)

            for g in ghosts:

                if g.state == ghost.FRIGHTENED:

                    g.reset((13, 14), ghost.FAST, 0, 0)
                    self.pacman.score += self.ghost_value
                    self.ghost_value >>= 1

                else:

                    self.pacman.lives -= 1
                    self.reset_positions()
                    break

            self.grid.draw_grid(screen)
            self.pacman.update(screen, self.grid.grid)
            self.ghosts.update(screen, self.grid.grid, [self.pacman.grid_pos, self.blinky.grid_pos])

            self.draw_score(screen)
            self.draw_lifes(screen)

            # end game

            if self.pacman.lives == 0:
                self.game_over(screen)
                running = False

            if self.grid.pellet_count == 0:
                self.victory(screen)
                running = False

            pygame.display.flip()













if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode(config.SCREEN_SIZE)

    g = Game()
    g.loop(screen)
