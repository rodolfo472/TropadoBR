import os
import discord
from discord import app_commands
from openai import OpenAI

DISCORD_TOKEN = os.getenv("MTU1MTk3Nzg5MTQ4NTQ1ODU5Mw.GgPGBd.r8JHShxmgIhHT7Qa2IpjHeN0UpwFDgO4JSnnC0")
MODELFLARE_API_KEY = os.getenv("sk-1zWRm3LxO8vR3nTqdBPhsOGuAnG0MxQGwj3XloofM0KDmDkP")
MODELFLARE_BASE_URL = os.getenv("https://modelflare.dev/keys")

ai = OpenAI(
    api_key=MODELFLARE_API_KEY,
    base_url=MODELFLARE_BASE_URL
)

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot conectado como {bot.user}")


@tree.command(
    name="ia",
    description="Converse com a IA"
)
@app_commands.describe(
    pergunta="Digite sua pergunta"
)
async def ia(
    interaction: discord.Interaction,
    pergunta: str
):
    await interaction.response.defer()

    try:
        resposta = ai.chat.completions.create(
            model=os.getenv("IA DE TROPAS DO REDUTO", "default"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é a IA do servidor Discord. "
                        "Responda sempre em português brasileiro. "
                        "Seja amigável, útil e direto."
                    )
                },
                {
                    "role": "user",
                    "content": pergunta
                }
            ]
        )

        texto = resposta.choices[0].message.content

        if not texto:
            texto = "Não consegui gerar uma resposta."

        if len(texto) > 1900:
            texto = texto[:1900] + "..."

        await interaction.followup.send(
            f"🤖 **ALL Black IA**\n\n{texto}"
        )

    except Exception as erro:
        print(f"❌ Erro: {erro}")

        await interaction.followup.send(
            "❌ A IA encontrou um erro. Verifique as configurações da API."
        )


if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN não configurado.")

if not MODELFLARE_API_KEY:
    raise RuntimeError("MODELFLARE_API_KEY não configurada.")

if not MODELFLARE_BASE_URL:
    raise RuntimeError("MODELFLARE_BASE_URL não configurada.")

bot.run(DISCORD_TOKEN)
