from telebot.types import Message
from telebot import TeleBot

from ..data import User, JobFair


import requests
import tempfile
import shutil
import os
from datetime import datetime


def get_user_type(message: Message):
    chat_id = message.chat.id


def form_and_send_new_cv_archive(bot: TeleBot, user: User):
    UPDATE_INTERVAL = 1  # minutes
    ejf = JobFair.objects.first()
    chat_id = user.chat_id

    # show sending document
    bot.send_chat_action(chat_id, action="upload_document")

    # update archive only once in 10 min
    archive_last_update = ejf.cv_archive_last_update
    if archive_last_update:
        date_diff = (
            user.last_interaction_date - archive_last_update
        ).total_seconds() / 60.0
        if date_diff < UPDATE_INTERVAL:
            bot.send_message(
                chat_id,
                text=f"Почекай ще {UPDATE_INTERVAL-date_diff:.2f} хвилин...",
            )
            return

    # make temp directory
    with tempfile.TemporaryDirectory(prefix="ejf_bot_") as temp_dir_path:

        for cv_user in User.objects.filter(cv_file_id__ne=None):

            # get file from telegram servers
            file_info = bot.get_file(file_id=cv_user.cv_file_id)
            file_name = cv_user.cv_file_name
            downloaded_file = bot.download_file(file_info.file_path)

            # save file to temp directory
            temp_file_path = os.path.join(temp_dir_path, file_name)
            with open(temp_file_path, "wb") as new_file:
                new_file.write(downloaded_file)

        # make archive
        archive_path = shutil.make_archive("CV_database", "zip", temp_dir_path)

    # send archive
    with open(archive_path, "rb") as archive:
        message = bot.send_document(chat_id, archive)

    # update db info
    ejf.cv_archive_size = User.objects.filter(cv_file_id__ne=None).count()
    ejf.cv_archive_last_update = user.last_interaction_date
    ejf.cv_archive_file_id = message.document.file_id
    ejf.save()

    # delete archive
    os.remove(archive_path)