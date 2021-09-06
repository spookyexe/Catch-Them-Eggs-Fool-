import pygame

class UI:
    def __init__(self, surface, surface_w, surface_h) -> None:
            self.screen = surface
            self.screen_width = surface_w
            self.screen_height = surface_h

            self.font_path = 'assets/misc/Roboto-Bold.ttf'
            self.tiny_font = pygame.font.Font(self.font_path, 16)
            self.big_font = pygame.font.Font(self.font_path, 64)
            self.medium = pygame.font.Font(self.font_path, 24)
            self.small_font = pygame.font.Font(self.font_path, 20)

            self.white_color = 'white'
            self.gray_color = 'gray'
            self.lightgray_color = (190, 190, 190)
            self.white_ish_color = (230, 230, 230)

            self.show_score = True

            self.credits = self.tiny_font.render(('Made by Spooky | ♫ Bobbin by David Renda'), True, self.gray_color)
            self.credits_pos = self.credits.get_rect(center=(self.screen_width, 20))
            self.credits_speed = 4

    def black_overlay(self):
        # black transparent overlay
        rect = pygame.Surface((self.screen_width-20,self.screen_height-20))
        rect.fill('black')
        rect.set_alpha(80)
        self.screen.blit(rect, (10, 10))

    def pause_screen(self):
        # bg overlay
        self.black_overlay()
        # pause text
        text = self.big_font.render(('PAUSED'), True, self.white_color)
        text_pos = text.get_rect(center=(self.screen_width/2, self.screen_height/4))
        self.screen.blit(text, text_pos)

    def lose_screen(self, score, highscore):
        self.show_score = False
        # bg overlay
        self.black_overlay()
        # you lost text
        text_lose = self.big_font.render(('You Lost!'), True, self.white_color)
        text_lose_pos = text_lose.get_rect(center=(self.screen_width/2, self.screen_height/4))
        self.screen.blit(text_lose, text_lose_pos)
        # shows the final score
        text_score = self.tiny_font.render((str(score)), True, self.white_ish_color)
        text_score_pos = text_score.get_rect(center=(self.screen_width/2, text_lose_pos.centery+100))
        self.screen.blit(text_score, text_score_pos)
        # try again
        text_retry = self.medium.render(('-- Press SPACEBAR to try Again --'), True, self.gray_color)
        text_retry_pos = text_retry.get_rect(center=(self.screen_width/2, self.screen_height-self.screen_height/4))
        self.screen.blit(text_retry, text_retry_pos)
        # highscore
        text_highscore = self.small_font.render((str(highscore)), True, self.lightgray_color)
        text_highscore_pos = text_highscore.get_rect(center=(self.screen_width/2, text_score_pos.centery+32))
        self.screen.blit(text_highscore, text_highscore_pos)

    def display_score(self, score):
        # displays the score if self.show_score is True
        if self.show_score:
            text = self.tiny_font.render((str(score)), True, self.white_ish_color)
            text_pos = text.get_rect(center=(self.screen_width/2, self.screen_height/32))
            self.screen.blit(text, text_pos)

    def show_instructions(self):
        # movement intructions
        text = self.tiny_font.render(('-- Press <- and -> to Move --'), True, self.gray_color)
        text_pos = text.get_rect(center=(self.screen_width/2, self.screen_height-20))
        self.screen.blit(text, text_pos)

    def start_screen(self, highscore):
        # bg ovelay
        self.black_overlay()
        # credits
        self.display_credits()
        # game title 1
        text_title = self.big_font.render(('Catch Them'), True, self.white_color)
        text_title_pos = text_title.get_rect(center=(self.screen_width/2, self.screen_height/4))
        self.screen.blit(text_title, text_title_pos)
        # game title 2
        text_title2 = self.big_font.render(('Eggs, Fool!'), True, self.white_color)
        text_title2_pos = text_title2.get_rect(center=(self.screen_width/2, text_title_pos.centery+64))
        self.screen.blit(text_title2, text_title2_pos)
        # shows highscore
        text_highscore = self.small_font.render((str(highscore)), True, self.lightgray_color)
        text_highscore_pos = text_highscore.get_rect(center=(self.screen_width/2, self.screen_height/2))
        self.screen.blit(text_highscore, text_highscore_pos)
        # start game
        text_start = self.small_font.render(('-- Move to Start Game --'), True, self.gray_color)
        text_pos = text_start.get_rect(center=(self.screen_width/2, self.screen_height-self.screen_height/4))
        self.screen.blit(text_start, text_pos)

    def display_credits(self):
        # displays the credits
        # move credits
        self.credits_pos.x += -self.credits_speed
        # bounce credits
        if self.credits_pos.left <= 0-self.credits_pos.w or self.credits_pos.right >= self.screen_width+self.credits_pos.w:
            self.credits_speed *= -1
        # blit credits
        self.screen.blit(self.credits, self.credits_pos)

