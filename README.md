```css
{ooer is:an('experimental')}[tech]support.forum{founded on:the('philosophy')}[that]everyone.has{something that:they('can')}[contribute].
```

# Boot up your very own version of cromgis!
1. [Create a Discord bot account](https://discordpy.readthedocs.io/en/latest/discord.html)
2. [Clone this repo](https://docs.github.com/en/free-pro-team@latest/desktop/contributing-and-collaborating-using-github-desktop/cloning-a-repository-from-github-to-github-desktop)
3. Run [`poetry install`](https://python-poetry.org/docs/) in the project's directory
4. Use `.env.template` (TODO: make .env.template)[^1] to create and fill out a `.env` file in the project's directory
5. Start the bot with `poetry run python main.py`

[^1]: If you Ctrl+F the code for `os.environ` you'll find all the environment variables you have to fill out
