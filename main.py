import wikipedia
from discord import File
from discord import Game
from discord.ext import commands
import os

wiki = commands.Bot(("wiki ", "wikipedia ", "w?"), case_insensitive=True, help_command=None)


@wiki.command(name="search")
async def search(ctx, *, search_term):
    results = wikipedia.search(search_term)
    if len(results) == 0:
        await ctx.send(f"No results were found for '{search_term}'.")
        return 0
    out = "Search results for '**" + search_term + "**':\n"
    if len(results) < 3:
        for result in results:
            out += result + "\n"
    elif len(results) > 3:
        for i in range(3):
            out += results[i] + "\n"
    await ctx.send(out)


@wiki.command(name="summary")
async def summary(ctx, *, search_term):
    try:
        await ctx.send(wikipedia.summary(search_term))
    except wikipedia.exceptions.PageError:
        await ctx.send(f"The page '{search_term}' does not exist. Try using the summary command again with results for your term from the suggest or search commands.")


@wiki.command(name="suggest")
async def suggest(ctx, *, search_term):
    await ctx.send(wikipedia.suggest(search_term))


@wiki.command(name="url", aliases=["link"])
async def url(ctx, *, search_term):
    try:
        page = wikipedia.page(search_term)
        await ctx.send(f"<{page.url}>")
    except wikipedia.exceptions.PageError:
        await ctx.send(f"The page '{search_term}' does not exist. Try using the URL command again with results for your term from the suggest or search commands.")


@wiki.command(name="content")
async def content(ctx, *, search_term):
    try:
        page = wikipedia.page(search_term)
        page_content = page.content
        content_file = open(f"content_dumps/{search_term}.txt", "w")
        content_file.write(page_content)
        content_file.close()
        await ctx.send(file=File(f"content_dumps/{search_term}.txt"))
    except wikipedia.exceptions.PageError:
        await ctx.send(f"The page '{search_term}' does not exist. Try using the content command again with results for your term from the suggest or search commands.")
    except FileNotFoundError:
        await ctx.send("A backend I/O error occurred.")


@wiki.command(name="ping")
async def ping(ctx):
    await ctx.send("Current latency: " + str(round(wiki.latency*100, 2)) + "ms")


@wiki.command(name="copyright", aliases=["copy"])
async def show_copyright(ctx):
    with open("copyright.txt", "r") as copyright_file:
        await ctx.send(copyright_file.read())


@wiki.command(name="help")
async def show_help(ctx):
    with open("help.txt", "r") as help_file:
        await ctx.send(help_file.read())


@wiki.event
async def on_connect():
    print("Wikipedia Discord Bot v1.0")
    print("(c) 2021 Vhectr Software")
    print()
    print("Bot successfully connected to Discord API.")
    await wiki.change_presence(activity=Game(name="For help type w?help."))

wiki.run(os.getenv("token"))
