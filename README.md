# Bot Telegram Météo

Un bot Telegram écrit en Python qui fournit la météo en temps réel, des prévisions sur 5 jours et des alarmes de température personnalisées, le tout via l'API [OpenWeatherMap](https://openweathermap.org/).

## Fonctionnalités

- **Météo en temps réel** : température, ressenti et vitesse du vent pour n'importe quelle ville
- **Prévisions sur 5 jours** : température moyenne journalière calculée à partir des relevés de l'API
- **Alarmes de température** : reçois une notification automatique quand une ville atteint la température cible
- **Message d'accueil** : guide d'utilisation à la première interaction

## Commandes

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/start` | Affiche le message d'accueil et l'aide | `/start` |
| `/meteo <ville>` | Météo actuelle de la ville | `/meteo Paris` |
| `/prevision <ville>` | Prévisions sur 5 jours | `/prevision Lyon` |
| `/set_alarm <ville> <température>` | Définit une alarme déclenchée quand la ville atteint la température (°C) | `/set_alarm Marseille 30` |

## Prérequis

- Python 3.9 ou supérieur
- Les bibliothèques listées dans `requirements.txt` :
  - `python-telegram-bot`
  - `requests`
  - `python-dotenv`

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/<ton-pseudo>/<nom-du-repo>.git
   cd <nom-du-repo>
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtenir un token Telegram**
   - Ouvre une conversation avec [@BotFather](https://t.me/BotFather) sur Telegram
   - Envoie `/newbot` et suis les instructions
   - Copie le token fourni

4. **Obtenir une clé API OpenWeatherMap**
   - Crée un compte gratuit sur [openweathermap.org](https://home.openweathermap.org/users/sign_up)
   - Récupère ta clé dans l'onglet « API keys »
   - La clé peut prendre quelques heures avant d'être active

5. **Trouver ton ID Telegram**
   - Ouvre une conversation avec [@userinfobot](https://t.me/userinfobot)
   - Il te renvoie ton ID numérique (nécessaire pour recevoir les alarmes)

## Configuration

Copie le fichier d'exemple et remplis-le avec tes propres clés :

```bash
cp .env.example .env
```

Le fichier `.env` doit contenir :

```
token = 'ton_token_telegram'
API = 'ta_cle_openweathermap'
ID = 'ton_id_telegram'
```

> ⚠️ Ne partage jamais ton fichier `.env`. Il est exclu du dépôt via `.gitignore`.

## Lancement

```bash
python weather.py
```

Le bot se met alors en écoute. Ouvre Telegram, lance `/start` et c'est parti.

## Améliorations possibles

- Support multi-utilisateurs pour les alarmes (actuellement une seule alarme globale)
- Validation que la température cible est bien un nombre
- Choix de l'unité (°C / °F)
- Gestion d'un nombre variable de jours dans les prévisions
- Déploiement sur un serveur ou un Raspberry Pi pour un fonctionnement continu

## Ce que j'ai appris

- Consommer une API REST en Python avec `requests` et parser des réponses JSON imbriquées
- Gérer des clés sensibles avec des variables d'environnement (`python-dotenv`)
- Comprendre la boucle d'événements asynchrone et les handlers de `python-telegram-bot`
- Planifier des tâches récurrentes avec la `job_queue`
