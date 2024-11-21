import pygame


class Button:

    def __init__(self, screen, x, y, w, h, text, color=(255, 255, 255), bg_color=(0, 0, 0)):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color  # color of font
        self.text = text
        self.bg_color = bg_color  # background color
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render(self.text, True, self.color)
        # put the text in the center of the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class InputBox:
    def __init__(self, x, y, w, h, font_size=32, text=''):
        self.GRAY = (132, 133, 135)
        self.BLACK = (0, 0, 0)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (132, 133, 135)
        self.text = text # the content of the input box
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.BLACK)
        self.active = False  # whether to activate the input box
        self.color_active = pygame.Color('dodgerblue2')
        self.color_inactive = self.GRAY

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activated if you click on the input box, otherwise de-activated
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.text = ''
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        # if the input box is activated, then user can input text
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if event.key == pygame.K_RETURN:
                #     print(self.text)  # print the content of the input box
                # self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.BLACK)

    def draw(self, screen):
        # draw the input box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # draw the border
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self):
        # change the width of the input box
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width


class ScrollBar():
    def __init__(self,scrollbar_width,msg_log,font,area_x,area_y,area_width,area_height):
        self.scrollbar_width = scrollbar_width
        self.chat_offset_y = 0  # vertical scroll offset
        self.chat_offset_x = 0  # horizontal scroll offset
        self.is_dragging_vertical = False
        self.is_dragging_horizontal = False
        self.vertical_scroll_pos = 0
        self.horizontal_scroll_pos = 0
        self.font = font
        self.msg_log = msg_log
        self.line_height = font.get_height() + 5
        self.content_height = len(msg_log) * self.line_height
        self.content_width = max((font.size(str(line))[0] for line in msg_log),default=0) + 10
        self.area_x = area_x
        self.area_y = area_y
        self.area_width = area_width
        self.area_height = area_height
        self.vertical_scrollbar_length = self.area_height * self.area_height // max(self.area_height, self.content_height)
        self.horizontal_scrollbar_length = self.area_width * self.area_width // max(self.area_width, self.content_width)


    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # tell if the vertical scrollbar is clicked
            if (
                self.area_x + self.area_width <= mouse_x <= self.area_x + self.area_width + self.scrollbar_width and
                self.area_y <= mouse_y <= self.area_y + self.area_height
            ):
                self.is_dragging_vertical = True

            # tell if the horizontal scrollbar is clicked
            if (
                self.area_y + self.area_height <= mouse_y <= self.area_y + self.area_height + self.scrollbar_width and
                self.area_x <= mouse_x <= self.area_x + self.area_width
            ):
                self.is_dragging_horizontal = True

        #set all false when mouse is up
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging_vertical = False
            self.is_dragging_horizontal = False

        if event.type == pygame.MOUSEMOTION:
            # if the mouse is dragging the scrollbar, then update the position of the scrollbar
            if self.is_dragging_vertical:
                mouse_y = event.pos[1]
                self.vertical_scroll_pos = max(0, min(self.area_height - self.vertical_scrollbar_length,mouse_y - self.area_y))
                try:
                    self.chat_offset_y = self.vertical_scroll_pos * max(0, self.content_height - self.area_height) / (self.area_height - self.vertical_scrollbar_length)
                except ZeroDivisionError:
                    self.chat_offset_y = 0

            # if the mouse is dragging the scrollbar, then update the position of the scrollbar
            if self.is_dragging_horizontal:
                mouse_x = event.pos[0]
                self.horizontal_scroll_pos = max(0, min(self.area_width - self.horizontal_scrollbar_length, mouse_x - self.area_x))
                try:
                    self.chat_offset_x = self.horizontal_scroll_pos * max(0, self.content_width - self.area_width) / (self.area_width - self.horizontal_scrollbar_length)
                except ZeroDivisionError:
                    self.chat_offset_x = 0

    def draw(self,screen):
        pygame.draw.rect(screen, (100,100,100), (
            self.area_x +self.area_width, self.area_y+self.vertical_scroll_pos,
            self.scrollbar_width, self.vertical_scrollbar_length
        ))

        pygame.draw.rect(screen, (100,100,100), (
            self.area_x + self.horizontal_scroll_pos, self.area_y + self.area_height,
            self.horizontal_scrollbar_length, self.scrollbar_width
        ))

    def update(self):
        self.content_height = len(self.msg_log) * self.line_height
        self.content_width = max((self.font.size(str(line))[0] for line in self.msg_log), default=0) + 10
        try:
            self.vertical_scrollbar_length = self.area_height * self.area_height // max(self.area_height, self.content_height)
        except ZeroDivisionError:
            self.vertical_scrollbar_length = 0
        try:
            self.horizontal_scrollbar_length = self.area_width * self.area_width // max(self.area_width, self.content_width)
        except ZeroDivisionError:
            self.horizontal_scrollbar_length = 0
