import pygame
import pika

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 50)

    def print_screen(self, screen, text_string):
        text_bitmap = self.font.render(text_string, True, WHITE)
        screen.blit(text_bitmap, [self.x_value, self.y_value])
        self.y_value += self.line_height

    def reset(self):
        self.x_value = 10
        self.y_value = 10
        self.line_height = 30

    def indent(self):
        self.x_value += 10

    def unindent(self):
        self.x_value -= 10

class Controller:
    def __init__(self):
        self.current_left = 0.0
        self.current_right = 0.0
        self.current_left_string = "0.0"
        self.current_right_string = "0.0"
        self.con = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672))
        self.channel = self.con.channel()
        self.channel.queue_declare(queue="control")

    def maybe_update_state(self, left_value, right_value):
        if self.__value_changed(left_value, right_value):
            rounded_left_value = "%.2f" % round(left_value * .85, 2)
            rounded_right_value = "%.2f" % round(right_value * .85, 2)
            self.__send_updated_state(rounded_left_value, rounded_right_value)
            self.current_left = left_value
            self.current_right = right_value
            self.current_left_string = rounded_left_value
            self.current_right_string = rounded_right_value

    def __send_updated_state(self, left_value, right_value):
        message = "[{}, {}]".format(left_value, right_value)
        self.channel.basic_publish(exchange="",
                                   routing_key="control",
                                   body=message)

    def __value_changed(self, left_value, right_value):
        return abs(self.current_left - left_value) > .05 or abs(
            self.current_right - right_value) > .05

    def close(self):
        self.con.close()

SIZE = [550, 700]
SCREEN = pygame.display.set_mode(SIZE)
DONE = False
CLOCK = pygame.time.Clock()

pygame.display.set_caption("Gamepad Input")
pygame.font.init()
pygame.joystick.init()

TEXT_PRINT = TextPrint()
CONTROLLER = Controller()

while DONE is False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True

    SCREEN.fill(BLACK)
    TEXT_PRINT.reset()

    GAMEPAD = pygame.joystick.Joystick(0)
    GAMEPAD.init()

    TEXT_PRINT.indent()

    TEXT_PRINT.print_screen(SCREEN, "Device:")
    TEXT_PRINT.print_screen(SCREEN, GAMEPAD.get_name())

    TEXT_PRINT.indent()
    LEFT_X = GAMEPAD.get_axis(0)
    LEFT_Y = GAMEPAD.get_axis(1)
    RIGHT_Y = GAMEPAD.get_axis(2)
    RIGHT_X = GAMEPAD.get_axis(3)
    CONTROLLER.maybe_update_state(LEFT_Y, RIGHT_Y)
    RIGHT_LABEL = "Right stick: ({:>4.3f}, {:>4.3f})"
    LEFT_LABEL = "Left stick: ({:>4.3f}, {:>4.3f})"
    TEXT_PRINT.print_screen(SCREEN, RIGHT_LABEL.format(LEFT_X, LEFT_Y))
    TEXT_PRINT.print_screen(SCREEN, LEFT_LABEL.format(RIGHT_X, RIGHT_Y))

    TEXT_PRINT.print_screen(SCREEN, "Button 1: {}".format(GAMEPAD.get_button(0)))
    TEXT_PRINT.print_screen(SCREEN, "Button 2: {}".format(GAMEPAD.get_button(1)))
    TEXT_PRINT.print_screen(SCREEN, "Button 3: {}".format(GAMEPAD.get_button(2)))
    TEXT_PRINT.print_screen(SCREEN, "Button 4: {}".format(GAMEPAD.get_button(3)))

    TEXT_PRINT.print_screen(SCREEN, "D-pad 0: {}".format(str(GAMEPAD.get_hat(0))))

    TEXT_PRINT.unindent()
    TEXT_PRINT.unindent()

    TEXT_PRINT.print_screen(SCREEN, "Controller state:")
    TEXT_PRINT.indent()
    TEXT_PRINT.print_screen(SCREEN, "Left: {}".format(CONTROLLER.current_left_string))
    TEXT_PRINT.print_screen(SCREEN, "Right: {}".format(CONTROLLER.current_right_string))
    # Update the screen
    pygame.display.flip()

    # Limit to 20 frames per second
    CLOCK.tick(20)

pygame.quit()
CONTROLLER.close()
