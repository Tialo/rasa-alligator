import sqlite3

from rasa_sdk import Action

from add_words import Mode, get_word, write

write()


class ActionNewGame(Action):
    def name(self):
        return "action_new_game"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id

        with sqlite3.connect("db.db") as conn:
            curs = conn.cursor()
            curs.execute(
                "select count(*) from games where user_id = ?",
                (user_id, )
            )
            [res] = curs.fetchone()
            if res:
                curs.execute(
                    "update games set score = 0, mode = 0 where user_id = ?",
                    (user_id, )
                )
            else:
                curs.execute(
                    "insert into games (user_id, mode, score) values (?, ?, ?)",
                    (user_id, 0, 0)
                )
            conn.commit()
        word = get_word(Mode.EASY)
        dispatcher.utter_message(word)
        return []


class ActionChangeToHard(Action):
    def name(self):
        return "action_change_to_hard"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        with sqlite3.connect("db.db") as conn:
            curs = conn.cursor()
            curs.execute(
                "update games set mode = ? where user_id = ?",
                (1, user_id)
            )
            conn.commit()
        return []


class ActionChangeToEasy(Action):
    def name(self):
        return "action_change_to_easy"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        with sqlite3.connect("db.db") as conn:
            curs = conn.cursor()
            curs.execute(
                "update games set mode = ? where user_id = ?",
                (0, user_id)
            )
            conn.commit()
        return []


class ActionScoreWord(Action):
    def name(self):
        return "action_score_word"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        with sqlite3.connect("db.db") as conn:
            curs = conn.cursor()
            curs.execute(
                "update games set score = score + 1 where user_id = ?",
                (user_id, )
            )
            conn.commit()
            curs.execute(
                "select mode from games where user_id = ?",
                (user_id, )
            )
            [mode] = curs.fetchone()
            mode = Mode.HARD if mode else Mode.EASY
        word = get_word(mode)
        dispatcher.utter_message(word)
        return []


class ActionSkipWord(Action):
    def name(self):
        return "action_skip_word"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        with sqlite3.connect("db.db") as conn:
            curs = conn.cursor()
            curs.execute(
                "select mode from games where user_id = ?",
                (user_id, )
            )
            [mode] = curs.fetchone()
            mode = Mode.HARD if mode else Mode.EASY
        dispatcher.utter_message(get_word(mode))
        return []


class ActionPrintScore(Action):
    def name(self):
        return "action_print_score"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        with sqlite3.connect("db.db") as conn:
            curs = conn.cursor()
            curs.execute(
                "select score from games where user_id = ?",
                (user_id, )
            )
            res = curs.fetchone()
            if res is None:
                dispatcher.utter_message("Не удалось найти счет для этой игры")
                return []
            res = res[0]
        dispatcher.utter_message(str(res))
        return []
