import sqlite3


class Database():
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def check_user_exist(self, user_id):
        with self.connection:
            user_status = self.cursor.execute("SELECT * FROM storage_users WHERE user_id = ?", (user_id, )).fetchall()
            return bool(len(user_status))

    def get_all_channels_text(self):
        with self.connection:
            return self.cursor.execute("SELECT channel_text FROM storage_channels").fetchall()

    def get_channel(self, channel_text):
        with self.connection:
            return self.cursor.execute("SELECT channel_url FROM storage_channels WHERE channel_text = (?)", (channel_text,)).fetchone()

    def add_new_question(self, question_text, question_channel, user_id, question_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_questions VALUES(?,?,?,?)", (question_text, question_channel, user_id, question_id))

    def get_question(self, question_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM storage_questions WHERE question_id = ?", (question_id,)).fetchone()

    def get_question_channel_id(self, question_channel):
        with self.connection:
            return self.cursor.execute("SELECT channel_id FROM storage_channels WHERE channel_url = ?", (question_channel, )).fetchone()

    def delete_question(self, question_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM storage_questions WHERE question_id = ?", (question_id,))

    def add_channelx(self, channel_url, channel_text, channel_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_channels VALUES(?,?,?)", (channel_url, channel_text, channel_id))

    def delete_channelx(self, channel_text):
        with self.connection:
            return self.cursor.execute("DELETE FROM storage_channels WHERE channel_text = ?", (channel_text, ))

    def add_userx(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_users VALUES(?)", (user_id, ))

    def get_count_userx(self):
        with self.connection:
            return self.cursor.execute('SELECT COUNT(user_id) FROM storage_users').fetchone()

    def get_all_userx(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM storage_users").fetchall()

    def ban_userx(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_banned VALUES(?)", (user_id,))

    def get_banned_userx(self, user_id):
        with self.connection:
            user_status = self.cursor.execute("SELECT * FROM storage_banned WHERE user_id = ?", (user_id, )).fetchall()
            return bool(len(user_status))

    def get_question_userx(self, question_id):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM storage_questions WHERE question_id = ?", (question_id, )).fetchone()
