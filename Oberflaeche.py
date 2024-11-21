import pygame
from Draw import InputBox, Button, ScrollBar
import Client



white = (255, 255, 255)
black = (0, 0, 0)
screensize = (800, 600)
gray = (200, 200, 200)
white_1 = (255,255,255)



chat_box_x = 150
chat_box_y = 10

pygame.init()
pygame.font.init()
text_font = pygame.font.Font(None, 36)
user_list_font = pygame.font.Font(None, 24)


running = True # control the main loop


messages = [] # store the messages


# Initialize the name window
name_screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Name')
name_input = InputBox(70, 100, 260, 50, 32, 'Please enter your name')
name_button = Button(name_screen, 150, 200, 100, 50, 'Enter', bg_color=(0, 47, 167))
name = ''

is_window_screen = False
is_window_name = True

#to avoid "name can be undefined"
client_object = None
input_box = None
send_button = None
scroll_list = None
screen = None
user_list_surface = None
user_list = []


while running:
    while is_window_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                is_window_name = False
                is_window_screen = False
                break

            name_input.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and name_button.is_clicked(pygame.mouse.get_pos()):
                name = name_input.text

                #jump to the chat window
                is_window_name = False
                is_window_screen = True

                # Connect to the server
                try:
                    client_object = Client.Client(name)  # Initialize the Client
                    client_object.start()
                except Exception as e:
                    print(f"Error connecting to server: {e}")
                    running = False

        #draw the screen
        name_screen.fill(white)
        name_input.draw(name_screen)
        name_button.draw()
        pygame.display.flip()

    if is_window_screen:
        screen = pygame.display.set_mode(screensize)  # Reinitialize the screen
        pygame.display.set_caption('Chat')
        is_window_screen = True
        send_button = Button(screen, 650, 530, 100, 50, 'Send', bg_color=(0, 47, 167))
        input_box = InputBox(100, 530, 550, 50, 32, 'Enter your message')
        scroll_list = ScrollBar(12, messages, text_font, chat_box_x, chat_box_y, 550, 500)
        user_list_surface = pygame.Surface((100, 500))  # Adjust size as needed
        user_list_surface.fill(gray)
        user_list_rect = user_list_surface.get_rect(topleft=(10, 10))


    while is_window_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if client_object:
                    client_object.close()
                is_window_screen = False
                running = False

            input_box.handle_event(event)
            scroll_list.event_handler(event)

            # get the new message from the server
            try:
                new_messages = client_object.get_message()
                if new_messages:
                    for msg_type, content in new_messages:
                        if msg_type == "USER_LIST":
                            user_list = content
                        if msg_type == "MESSAGE":
                            messages.append(content)
            except Exception as e:
                print(f"Error retrieving messages: {e}")
                running = False
                

            if event.type == pygame.MOUSEBUTTONDOWN and send_button.is_clicked(pygame.mouse.get_pos()):
                messages.append(input_box.text)
                client_object.send_message(input_box.text)
                input_box.text = ''
                input_box.txt_surface = input_box.font.render('', True, input_box.BLACK)

        screen.fill(white)
        chat_box = pygame.Surface((550, 500))
        chat_box.fill(gray)

        # print the messages in the chat box
        for i, message in enumerate(messages):
            text = text_font.render(message, True, black)
            chat_box.blit(text, (-scroll_list.chat_offset_x, i * scroll_list.line_height - scroll_list.chat_offset_y))

        screen.blit(chat_box, (chat_box_x, chat_box_y))
        send_button.draw()
        input_box.draw(screen)

        # update the message to scrollBar
        scroll_list.msg_log = messages
        scroll_list.update()
        scroll_list.draw(screen)

        #draw user List
        user_list_title = pygame.font.Font(None, 32).render("User", True, black)

        user_list_surface.fill(white_1)
        user_list_surface.blit(user_list_title, (10, 0))
        if user_list:
            for i, user in enumerate(user_list):
                user_text = user_list_font.render(user, True, black)
                user_list_surface.blit(user_text, (10, (i * text_font.get_height()+20)))# +20 to avoid overlapping with the title
        screen.blit(user_list_surface, (10,10))


        pygame.display.flip()

pygame.quit()
