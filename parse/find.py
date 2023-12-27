import parse.googlevision as gv
import parse.calcs as calcs
import pendulum
import re
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

async def search_user(update, context, name, file):

    await update.message.reply_text("Thanks! Processing...")
    try:
        gv.detect_text(file)
        first, last = name.split()
        wage = 38.18
        total = day_earned = match_count = 0
        day = shift_duration = ""
        minutes = lambda x: round((x - int(x))*100)
        found = False

        with open('result.txt', 'r') as file:

            # num = current number of line
            for num, line in enumerate(file, 1):

                # searching for date
                if re.search(r'\d{2}/\d{2}', line.strip()):
                    day = pendulum.datetime(
                        pendulum.now().year, 
                        int(line.strip()[-2:]), 
                        int(line.strip()[:2])
                    )

                # searching for name match
                if first in line and last in line:
                    
                    found = True
                    match_count += 1

                # searching for shift hours
                if re.search(r'\d{2}:\d{2}-\d{2}:\d{2}', line.strip()) and found:
                        
                        shift_duration = line.strip()
                        day_hours_calc = calcs.calc_time(
                            int(shift_duration[:2]), 
                            int(shift_duration[3:5]), 
                            int(shift_duration[6:8]), 
                            int(shift_duration[9:])
                        )

                        total += day_hours_calc
                        day_earned = calcs.calc_salary(int(day_hours_calc), minutes(day_hours_calc), wage, day.format('dddd'))
                        found = False

                        await update.message.reply_text(
                            f"{day.format('dddd, DD/MM')}\n{shift_duration}\nDay earned: {day_earned:.2f} ILS")

                        time.sleep(1)
        
        if match_count:
            await update.message.reply_text(f"{match_count} " + ("shifts " if match_count > 1 else "shift ") + f"this week. {int(total)} hours and {round((total - int(total))*100)} minutes in total.")
        else:
            await update.message.reply_text(f"\n{name} not found.")

        os.remove("result.txt")
    except:
            await update.message.reply_text("Something went wrong.")
