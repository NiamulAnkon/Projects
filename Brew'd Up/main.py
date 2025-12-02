import sys

from menu import run_menu


def main():
    try:
        start = run_menu()
        if not start:
            # User closed menu or chose to quit
            return

        # Import gameplay only when needed
        import main_gameplay

        # Run the gameplay loop
        main_gameplay.run_game()

    except Exception as e:
        # On exception, print traceback and attempt to save game state
        try:
            import traceback
            traceback.print_exc()
            if 'main_gameplay' in sys.modules:
                mg = sys.modules['main_gameplay']
                if hasattr(mg, 'game_state_obj') and hasattr(mg.game_state_obj, 'save'):
                    mg.game_state_obj.save()
        except Exception:
            pass
        raise


if __name__ == '__main__':
    main()
