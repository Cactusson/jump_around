"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare, tools
from .states import menu, game, gameover, message_screen


def main():
    """
    Add states to control here.
    """
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {'MENU': menu.Menu(),
                  'GAME': game.Game(),
                  'MESSAGE_SCREEN': message_screen.MessageScreen(),
                  'GAMEOVER': gameover.GameOver(),
                  }
    run_it.setup_states(state_dict, 'MENU')
    run_it.main()
