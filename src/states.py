from src import shared
from src.enums import State
from src.finder_state import FinderState
from src.game_state import GameState
from src.lobby_state import LobbyState
from src.menu_state import MenuState


class StateObj:
    def __init__(self):
        self.state_mapping = {
            State.GAME: GameState,
            State.MENU: MenuState,
            State.SERVER_FINDER: FinderState,
            State.LOBBY: LobbyState,
        }
        self.state = self.state_mapping.get(shared.current_state)()

    def update(self):
        self.state.update()

        if shared.current_state != None:
            self.state = self.state_mapping.get(shared.current_state)()
            shared.current_state = None

    def draw(self):
        self.state.draw()
