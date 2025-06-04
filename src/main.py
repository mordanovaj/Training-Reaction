"""
Главный модуль приложения
"""
import tkinter as tk
import json
from typing import Dict, Any
from src.components.menu import Menu
from src.components.game_field import GameField
from src.utils.settings import WINDOW


class ReactionTrainer:
    def __init__(self):
        """Инициализация приложения"""
        self.root = tk.Tk()
        self.root.title(WINDOW["title"])
        # Устанавливаем полноэкранный режим
        self.root.attributes('-fullscreen', True)
        # Добавляем обработчик клавиши Escape
        self.root.bind('<Escape>', lambda e: self.root.quit())

        # Настройки игры
        self.game_mode = "color"
        self.difficulty = "medium"
        self.best_score = 0

        # Загрузка настроек
        self.load_settings()

        # Создание компонентов
        self.menu = Menu(self.root, {
            'continue_game': self.continue_game,
            'new_game': self.start_new_game,
            'select_mode': self.select_mode,
            'show_instructions': Menu.show_instructions,
            'exit_game': self.exit_game
        })
        
        # Обновляем отображение лучшего результата и настроек
        self.menu.update_best_score(self.best_score)
        self.menu.update_mode_and_difficulty(self.game_mode, self.difficulty)

        self.game_field = GameField(self.root, self.show_menu)

        # Показать меню при запуске
        self.show_menu()

    def load_settings(self) -> None:
        """Загружает настройки из файла"""
        try:
            with open('best_score.json', 'r') as f:
                data = json.load(f)
                self.best_score = data.get('best_score', 0)
                self.game_mode = data.get('game_mode', "color")
                self.difficulty = data.get('difficulty', "medium")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_settings(self) -> None:
        """Сохраняет настройки в файл"""
        scores = self.game_field.get_scores()
        with open('best_score.json', 'w') as f:
            json.dump({
                'best_score': max(scores['best_score'], self.best_score),
                'game_mode': self.game_mode,
                'difficulty': self.difficulty
            }, f)

    def show_menu(self) -> None:
        """Показывает меню"""
        self.game_field.stop_game()
        self.game_field.hide()
        self.menu.show()
        scores = self.game_field.get_scores()
        self.best_score = max(scores['best_score'], self.best_score)
        self.menu.update_best_score(self.best_score)
        self.menu.update_mode_and_difficulty(self.game_mode, self.difficulty)
        self.save_settings()

    def start_new_game(self) -> None:
        """Начинает новую игру"""
        self.menu.hide()
        self.game_field.show()
        self.game_field.start_game(
            self.game_mode,
            self.difficulty,
            current_score=0,
            best_score=self.best_score
        )
        self.menu.update_continue_button(True)

    def continue_game(self) -> None:
        """Продолжает текущую игру"""
        self.menu.hide()
        self.game_field.show()
        scores = self.game_field.get_scores()
        self.game_field.start_game(
            self.game_mode,
            self.difficulty,
            current_score=scores['current_score'],
            best_score=max(scores['best_score'], self.best_score)
        )

    def select_mode(self) -> None:
        """Открывает окно выбора режима"""
        def on_save(mode: str, difficulty: str) -> None:
            self.game_mode = mode
            self.difficulty = difficulty
            self.menu.update_mode_and_difficulty(mode, difficulty)
            self.save_settings()

        Menu.show_mode_selection(
            self.root,
            self.game_mode,
            self.difficulty,
            on_save
        )

    def exit_game(self) -> None:
        """Закрывает игру"""
        self.save_settings()
        self.root.quit()

    def run(self) -> None:
        """Запускает приложение"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        print("Starting application...")
        app = ReactionTrainer()
        print("Application created, starting main loop...")
        app.run()
        print("Application closed.")
    except Exception as e:
        import traceback
        print(f"Error occurred: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        input("Press Enter to exit...")