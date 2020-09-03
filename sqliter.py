import sqlite3


class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_users(self, user_id):  # получаем список всех подписчиков бота
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`  WHERE `user_id` = ?", (user_id,)).fetchall()

    def user_search(self, user_id, day):  # проверяем на наличие юзера в базе
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ? AND `day` = ?", (user_id, day))
            return result

    def add_lesson(self, user_id, day, number, lesson, time):  # добавление подписчика
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `day`, `number`, `lesson`, `time`) VALUES (?,?,?,?,?)",
                (user_id, day, number, lesson, time))

    def update_subscription(self, user_id, status):  # обновление статуса
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        self.connection.close()
