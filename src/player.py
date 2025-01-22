import math

from pyray import *

from src import shared, utils
from src.asset_manager import ModelID
from src.decorations import Decoration
from src.logger import log
from src.packets import Packet

SPEED = 20
JUMP_VELOCITY = 0.007
GRAVITY = -0.02


class Player:
    def __init__(self):
        self.pos = Vector3(0, 0, 0)
        # self.pos.x = get_random_value(0, shared.MENU_WIDTH)
        # self.pos.y = get_random_value(0, shared.MENU_HEIGHT)
        # self.pos.z = get_random_value(-100, 100)

        if shared.model_id_argc is None:
            self.model_id = ModelID.CUBE_MAN
        else:
            self.model_id = getattr(ModelID, shared.model_id_argc)
        t = lambda: get_random_value(100, 255)
        self.color = Color(t(), t(), t(), 255)
        self.original_color = Color(self.color.r, self.color.g, self.color.b, 255)
        self.angle = math.pi / 2
        self.prev_mouse_pos = get_mouse_position()
        self.hitbox: BoundingBox | None = None
        self.model: None | Model = None
        self.velocity = Vector3(0, 0, 0)
        self.touched_ground = True

        self.current_model_id = ModelID.FLOOR
        self.is_editing_world = False

    def compute_angle(self) -> None:
        mouse_pos = get_mouse_position()
        z_delta = mouse_pos.x - self.prev_mouse_pos.x
        self.prev_mouse_pos.x, self.prev_mouse_pos.y = mouse_pos.x, mouse_pos.y

        turn_scale = 0.001
        self.angle -= z_delta * turn_scale
        self.angle %= 2 * math.pi

    def move(self):
        if is_key_down(KeyboardKey.KEY_SPACE) and self.touched_ground:
            self.velocity.y = JUMP_VELOCITY
            self.touched_ground = False

        # Get input for forward/backward (W/S) and strafing (A/D)
        forward = is_key_down(KeyboardKey.KEY_W) - is_key_down(KeyboardKey.KEY_S)
        strafe = is_key_down(KeyboardKey.KEY_A) - is_key_down(KeyboardKey.KEY_D)

        # Compute movement vector based on player's angle
        dx = math.sin(self.angle) * forward + math.cos(self.angle) * strafe
        dz = math.cos(self.angle) * forward - math.sin(self.angle) * strafe

        # Normalize movement vector to prevent diagonal speed boost
        magnitude = math.sqrt(dx**2 + dz**2)
        if magnitude > 0:
            dx /= magnitude
            dz /= magnitude

        self.velocity.y += GRAVITY * get_frame_time()

        self.velocity.x = SPEED * dx * get_frame_time()
        self.velocity.z = SPEED * dz * get_frame_time()
        self.velocity.y += self.velocity.y * get_frame_time()

    def resolve_collision_side(self, decoration: Decoration):
        if self.hitbox is None:
            return

        # Floor
        if self.pos.y > decoration.pos.y:
            if self.velocity.y < 0:
                self.velocity.y = 0
                self.touched_ground = True
            # self.pos.y = self.hitbox.max.y

    def collide_with_decorations(self):
        if self.hitbox is None:
            return

        self.color = self.original_color
        for dec in shared.world.dec_manager.decorations:
            if check_collision_boxes(dec.box, self.hitbox):
                self.color = Color(255, 0, 0, 255)
                self.resolve_collision_side(dec)

    def on_edit_mode(self):
        if is_key_pressed(KeyboardKey.KEY_Q):
            self.is_editing_world = not self.is_editing_world

        if not self.is_editing_world:
            return

    def update(self):
        self.on_edit_mode()
        self.move()
        self.collide_with_decorations()

        self.pos = vector3_add(self.pos, self.velocity)

    @staticmethod
    def draw_from_packet(packet: Packet) -> None:
        # px, py = int(packet.pos[0]), int(packet.pos[1])
        # draw_rectangle(px, py, 50, 50, packet.color)
        # draw_text(packet.name, px, py - 20, 20, GREEN)
        pass

    @staticmethod
    def draw_from_packet_3d(packet: Packet) -> Model:
        pos = Vector3(*packet.pos)
        model = shared.asset_manager.get_model_from_id(
            ModelID.from_value(packet.model_id)
        )
        model.transform = matrix_rotate_y(packet.angle)

        draw_model(model, pos, 1, packet.color)
        draw_model_wires(model, pos, 1, WHITE)

        return model

    def draw_3d(self):
        self.model = self.draw_from_packet_3d(shared.client.create_packet())
        self.hitbox = get_model_bounding_box(self.model)
        utils.set_box_pos(self.hitbox, shared.world.player.pos)

    def draw(self):
        self.draw_from_packet(shared.client.create_packet())
