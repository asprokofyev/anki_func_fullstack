import random
import sys
import time
from typing import Dict, Tuple


STOP_WORD = 'СТОП'
DEFAULT_DICTIONARY_FILENAME = 'words.txt'
MAIN_MENU = '''Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        '''


def load_words(filename: str = DEFAULT_DICTIONARY_FILENAME) -> Dict[str, str]:
    """
    Загружает пары 'слово, перевод' из текстового файла и возвращает словарь.
    Если файл не найден, выводит сообщение и завершает программу с кодом 1.
    """
    words_dictionary = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 2:
                    word, translate = parts
                    words_dictionary[word.strip()] = translate.strip()
    except FileNotFoundError:
        print(f'Ошибка: файл "{filename}" не найден.')
        sys.exit(1)
    return words_dictionary


def save_words(
        words: dict[str, str],
        filename: str = DEFAULT_DICTIONARY_FILENAME
) -> None:
    """Сохраняет словарь в файл, перезаписывая его содержимое."""
    with open(filename, 'w', encoding='utf-8') as file:
        for word, translation in words.items():
            file.write(f'{word}, {translation}\n')
    print(f'Было сохранено {len(words)} слов в файл {filename}')


def show_all_words(words: dict[str, str]) -> None:
    """
    Выводит все пары 'слово - перевод' через точку с запятой в одну строку
    """
    if not words:
        print('Словарь пуст. Добавьте слова перед игрой.')
        return

    print('; '.join(
        [f'{word} - {translation}' for word, translation in words.items()]
    ))


def add_words(words: dict[str, str]) -> None:
    """
    Добавляет новые пары в словарь в интерактивном режиме.
    Для завершения введите 'СТОП' при запросе слова или перевода.
    """
    while True:
        word = input('Введите слово: ').strip()
        if word.upper() == STOP_WORD:
            break

        translation = input('Введите перевод: ').strip()
        if translation.upper() == STOP_WORD:
            break

        words[word] = translation


def start_game(words: dict[str, str]) -> None:
    """
    Обычный режим игры: бесконечные вопросы
    с подсчётом правильных ответов и времени.
    """
    if not words:
        print('Словарь пуст. Добавьте слова перед игрой.')
        return

    correct_count = 0
    total_time = 0.0
    attempts = 0

    print('Чтобы закончить, введите СТОП')

    while True:
        word = random.choice(list(words.keys()))
        correct_translation = words[word]

        exit_flag, is_correct, answer_time = ask_and_check(
            word, correct_translation
        )

        if exit_flag:
            break

        attempts += 1
        total_time += answer_time

        if is_correct:
            correct_count += 1
            print(f'Верно! Время на ответ: {answer_time:.2f} секунд')
        else:
            print(
                f'Неправильно, правильный ответ: {correct_translation} '
                f'(Время на ответ: {answer_time:.2f} секунд)'
            )

    print('Спасибо за игру!')

    if attempts > 0:
        avg_time = total_time / attempts
        print(f'Ваш итоговый счёт: {correct_count}')
        print(
            f'Время игры: {total_time:.2f} секунд '
            f'(среднее время: {avg_time:.2f} сек.)'
        )
    else:
        print('Вы не ответили ни на один вопрос.')


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """
    Запрашивает перевод слова, замеряет время и возвращает:
    (exit_flag, is_correct, answer_time)
    exit_flag = True при вводе стоп-слова.
    """
    print(f'Ваше слово: {word}')
    start = time.time()
    user_input = input('Ваш перевод: ').strip()
    end = time.time()

    if user_input.upper() == STOP_WORD:
        return True, False, 0.0

    return False, user_input.lower() == correct.strip().lower(), end - start


def train_until_mistake(words: dict[str, str]) -> None:
    """
    Режим 'до первой ошибки': игра завершается при первой ошибке или
    по команде 'СТОП'.
    """
    if not words:
        print('Словарь пуст. Добавьте слова перед игрой.')
        return

    print('Режим: Игра до первой ошибки! Чтобы выйти вручную, введите СТОП')

    words_list = list(words.keys())
    score = 0
    total_time = 0.0

    while True:
        word = random.choice(words_list)
        correct_translation = words[word]

        exit_flag, is_correct, answer_time = ask_and_check(
            word, correct_translation
        )

        if exit_flag:
            print('Выход из режима по запросу пользователя.')
            break

        total_time += answer_time

        if is_correct:
            score += 1
            print(
                f'Верно! Всего очков: {score} '
                f'(ответ за {answer_time:.2f} секунд)'
            )
        else:
            print(f'Ошибка! Неверно. Правильный ответ: {correct_translation}')
            break

    print_statistics(score, total_time)


def print_statistics(score: int, total_time: float) -> None:
    """
    Выводит итоговый счёт, общее время и среднее время
    (или прочерк, если ответов не было).
    """
    print(f'Ваш итоговый счёт: {score}')
    print(f'Время игры: {total_time:.2f} секунд ')

    if score > 0:
        print(f'(среднее время: {total_time / score:.2f} сек.)')
    else:
        print('(среднее время: —)')


def main() -> None:
    """Главное меню программы."""
    words = load_words()
    print(f'Загружено {len(words)} слов.')

    while True:
        print(MAIN_MENU)
        menu_choice = input('Пункт меню: ').strip()

        if menu_choice == '1':
            start_game(words)
        elif menu_choice == '2':
            add_words(words)
        elif menu_choice == '3':
            train_until_mistake(words)
        elif menu_choice == '4':
            show_all_words(words)
        elif menu_choice == '5':
            save_words(words)
            print('До свидания!')
            sys.exit()
        else:
            print('Неизвестный пункт меню. Пожалуйста, повторите ввод.')


if __name__ == '__main__':
    main()
