import requests
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
token = os.getenv('token')
API = os.getenv('API')
ID = os.getenv('ID')

alarme = {}

async def meteo(update, context): #fonction de la météo
    if  len (context.args) == 0 : 
        await update.message.reply_text ("Veuillez indiquer le nom d' une ville après /meteo") 
        return
    
    ville = "".join(context.args) #Renseigne la ville choisie
    url = f'https://api.openweathermap.org/data/2.5/weather?q={ville}&units=metric&APPID={API}'
    reponse = requests.get(url).json()

    if reponse.get( "cod" ) != 200 : #Au cas où la ville est mal orthographié ou si l'api ne parvient pas à récupérer la météo
        await update.message.reply_text(f"Erreur : {reponse.get( 'message')} ") 
        return
    temperature = round(reponse['main']['temp'], 1)
    ressenti = round(reponse['main']['feels_like'], 1)
    vitesseVent = round((reponse['wind']['speed'])*3.6, 1)   
    await update.message.reply_text(f"""Météo à {ville} : 
    - Température : {temperature} °C 
    - Ressenti : {ressenti} °C
    -Vitesse du vent : {vitesseVent} km/h""")
        
async def start(update, context): #fonction de départ
    await update.message.reply_text("""Bienvenue sur le bot de météo d'Hugo.
Pour connaître la température et la vitesse du vent dans votre ville, veuillez-faire : 
    -/meteo "nom de la ville" """)
        
async def alarm(context: ContextTypes.DEFAULT_TYPE):
    if alarme:
        city_alarm = alarme['city']
        max = float(alarme['temp'])
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_alarm}&units=metric&APPID={API}'
        reponse = requests.get(url).json()
        if reponse.get( "cod" ) != 200 : #Au cas où la ville est mal orthographié ou si l'api ne parvient pas à récupérer la météo
            await context.bot.send_message(chat_id = ID, text=f"Erreur : {reponse.get( 'message')} ") 
            return
        temp = round(reponse['main']['temp'], 1)
        if temp >= max:
            await context.bot.send_message(chat_id=ID, text=f'Il fait {temp}°C à {city_alarm}')
            alarme.clear()
            await context.bot.send_message(chat_id=ID, text="L'alarme est atteinte et a été supprimé")

async def set_alarm(update, context):
    if len(context.args) < 2:
        await update.message.reply_text ("Veuillez indiquer le nom d' une ville et la température cible après /set_alarm") 
        return
    alarme["city"] = " ".join(context.args[:-1])
    alarme["temp"] = context.args[-1]
    await update.message.reply_text("Alarme enregistrée !")

async def prevision(update, context):
    if  len (context.args) == 0 : 
        await update.message.reply_text ("Veuillez indiquer le nom d' une ville après /meteo") 
        return
    ville_prevision = "".join(context.args) #Renseigne la ville choisie
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={ville_prevision}&units=metric&appid={API}'
    reponse = requests.get(url).json()
    if reponse.get( "cod" ) != 200 : #Au cas où la ville est mal orthographié ou si l'api ne parvient pas à récupérer la météo
        await update.message.reply_text(f"Erreur : {reponse.get( 'message')} ") 
        return
    temps_par_jour = {}
    for mesure in reponse['list']:
        jour = mesure['dt_txt'][:10]          
        temp = mesure['main']['temp']
        if jour not in temps_par_jour:
            temps_par_jour[jour] = []
        temps_par_jour[jour].append(temp)
    
    for i in temps_par_jour:
        temp_moyenne = sum(temps_par_jour[i]) / len(temps_par_jour[i])
        temps_par_jour[i].append(temp_moyenne)
    
    day = list(temps_par_jour.keys())
    await update.message.reply_text(f'''Prévision 5 jours sur {ville_prevision} : 
    - {day[0]} : {round(temps_par_jour[day[0]][-1], 1)}°C
    - {day[1]} : {round(temps_par_jour[day[1]][-1], 1)}°C
    - {day[2]} : {round(temps_par_jour[day[2]][-1], 1)}°C
    - {day[3]} : {round(temps_par_jour[day[3]][-1], 1)}°C
    - {day[4]} : {round(temps_par_jour[day[4]][-1], 1)}°C
    - {day[5]} : {round(temps_par_jour[day[5]][-1], 1)}°C''')

if __name__ == '__main__':
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('meteo', meteo))
    app.add_handler(CommandHandler('set_alarm', set_alarm))
    app.add_handler(CommandHandler('prevision', prevision))
    job_queue = app.job_queue
    job_minute = job_queue.run_repeating(alarm, interval=300, first=20)
    app.run_polling(poll_interval=5)


