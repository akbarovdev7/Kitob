from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMIN_ID = "ADMIN_ID" # adminlar ro'yxati

