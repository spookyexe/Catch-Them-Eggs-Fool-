from UI import UI
from egg import Egg
from player import Player

import pygame, random, json

class Game:
    def __init__(self, surface, surface_w, surface_h) -> None:
        self.screen = surface
        self.screen_width = surface_w
        self.screen_height = surface_h

        self.close_window = False

        self.player_color = (190, 190, 190)
        self.player = Player(self.screen, self.screen_width, self.screen_height, (80, 40), (self.screen_width/2, self.screen_height-self.screen_height/8), self.player_color)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.moving = False

        self.egg_color = 'white'
        self.egg_speed = 6
        self.egg_x = self.screen_width/2
        self.egg_group = pygame.sprite.Group()
        self.spawn_egg = pygame.USEREVENT
        self.spawn_time = 1000
        pygame.time.set_timer(self.spawn_egg, self.spawn_time)

        self.score = 0
        self.text_color = 'white'

        self.lose = False

        self.paused = False
        self.pause_amount = 0

        self.ui = UI(self.screen, self.screen_width, self.screen_height)

        self.json_file = 'highscore.json'
        # get new highscore
        with open(self.json_file, 'r') as f:
            high_score = json.load(f)
            self.high_score = high_score['highscore']
        # bg music
        music = pygame.mixer.Sound('assets/audio/2019-06-25_-_Bobbin_-_www.FesliyanStudios.com_-_David_Renda.mp3')
        music.play(loops=-1)

    def move_start(self):
        if not self.moving:
            self.ui.start_screen(self.high_score)
            self.ui.show_score = False

    def set_highscore(self):
        # if score is higher than prev highscore
        if self.score >= int(self.high_score):
            # open highscore file
            with open (self.json_file, 'r') as f:
                high_score = json.load(f)

                high_score['highscore'] = str(self.score)

                with open(self.json_file, 'w') as f:
                    # set new highscore
                    json.dump(high_score, f)
                    # get new highscore
                    self.high_score = high_score['highscore']

    def pause_screen(self):
        if (self.pause_amount%2) == 0:
            self.paused = False
            # unpause
        else:
            self.paused = True
            # pause

        if self.paused:
            # stops all movement
            for eggs in self.egg_group.sprites():
                eggs.speed = 0
            self.player.velocity = 0
            # displays the pause screen
            self.ui.pause_screen()

    def lose_screen(self):
        if self.lose:
            # displays the lose screen
            self.ui.lose_screen(self.score, self.high_score)
            # kills all eggs if player loses
            for eggs in self.egg_group.sprites():
                eggs.kill()

    def game_over(self):
        # checks if any egg in self.egg_group crosses the game over line
        for eggs in self.egg_group.sprites():
            if eggs.lose:
                self.lose = True
                # plays the game over sound
                self.sound('game_over')

    def increase_egg(self):
        # increases the egg speed and spawn time if you reach a certain score
        for eggs in self.egg_group.sprites():
            eggs.speed = self.egg_speed
            if self.score >= 20:
                self.egg_speed = 7
                self.spawn_time = 800
            if self.score >= 50:
                self.egg_speed = 8
                self.spawn_time = 600
            if self.score >= 70:
                self.egg_speed = 9
                self.spawn_time = 500
            if self.score >= 90:
                self.egg_speed = 10
                self.spawn_time = 400
            if self.score >= 120:
                self.egg_speed = 11
                self.spawn_time = 300
            if self.score >= 150:
                self.egg_speed = 12
                self.spawn_time = 200

    def player_egg_collide(self):
        # if an egg and the player collides
        if pygame.sprite.spritecollide(self.player, self.egg_group, True):
            # removes the egg and adds a score
            self.score += 1
            # play catch sound
            self.sound('catch')

    def events(self):
        # events
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                self.close_window = True
            # keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.velocity -= self.player.speed
                    self.moving = True
                    self.ui.show_score = True
                if event.key == pygame.K_RIGHT:
                    self.player.velocity += self.player.speed
                    self.moving = True
                    self.ui.show_score = True
                
                if event.key == pygame.K_ESCAPE and not self.lose:
                    self.pause_amount += 1
                    print('PAUSED')
                    self.sound('game_over')

                if event.key == pygame.K_SPACE and self.lose:
                    self.lose = False
                    self.score = 0
                    self.egg_speed = 6
                    self.spawn_time = 1000
                    self.ui.show_score = True

            if event.type == pygame.KEYUP and not self.paused:
                if event.key == pygame.K_LEFT:
                    self.player.velocity += self.player.speed
                if event.key == pygame.K_RIGHT:
                    self.player.velocity -= self.player.speed
            # spawn egg
            if event.type == self.spawn_egg and not self.lose and not self.paused and self.moving:
                self.egg_group.add(self.create_egg())
                self.sound('spawn')

    def random_egg_x(self):
        # randomizes the egg x
        spawn_locations = [25, 75, 125, 175, 225, 275, 325, 375, 425, 475]
        self.egg_x = random.choice(spawn_locations)

    def create_egg(self):
        # creates an egg
        return Egg(self.screen, self.screen_width, self.screen_height, (30, 40), (self.egg_x, 10), self.egg_color)

    def sound(self, sound):
        # plays sound
        catch = pygame.mixer.Sound('assets/audio/catch.wav')
        game_over = pygame.mixer.Sound('assets/audio/game_over.wav')
        spawn = pygame.mixer.Sound('assets/audio/spawn.wav')

        if sound == 'game_over':
            game_over.play()
        if sound == 'catch':
            catch.play()
        if sound == 'spawn':
            spawn.play()

    def run(self):
        # draw
        self.egg_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.ui.display_score(self.score)
        self.ui.show_instructions()
        # call methods
        self.random_egg_x()
        self.events()
        self.player_egg_collide()
        self.game_over()
        self.increase_egg()
        self.lose_screen()
        self.pause_screen()
        self.set_highscore()
        self.move_start()
        # call sprite methods
        self.player.update()
        self.egg_group.update()