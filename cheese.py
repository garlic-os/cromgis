import bs4
import pycountry
from discord.ext import commands

from utils import Crombed


class Cheese(commands.Cog):
    """Also made by garlicOS®"""

    BASE = "https://cheese.com"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def anchors2markdown(tag: bs4.Tag) -> str:
        """Converts any HTML anchors inside a tag to markdown links."""
        for a in tag.find_all("a"):
            a.replace_with(f"[{a.text}]({Cheese.BASE}{a['href']})")
        return tag.text

    @staticmethod
    def summary_point(soup: bs4.BeautifulSoup, emoji: str, class_: str) -> str:
        """Extracts a summary point from the cheese page."""
        text = Cheese.anchors2markdown(soup.find('li', class_=class_).p)
        return f"- {emoji} {text}"

    @staticmethod
    def country_summary_point(soup: bs4.BeautifulSoup) -> str:
        """Extracts the country summary point from the cheese page.
        
        It's special because it derives the flag emoji to use based on the
        country.
        """
        p = soup.find("li", class_="summary_country").p
        country_name = p.a.text
        possible_countries = pycountry.countries.search_fuzzy(country_name)
        if len(possible_countries) > 0:
            country_code = possible_countries[0].alpha_2.lower()
            emoji = f":flag_{country_code}:"
        else:
            emoji = "🏳️"
        text = Cheese.anchors2markdown(p)
        return f"- {emoji} {text}"


    @commands.command()
    async def cheese(self, ctx: commands.Context) -> None:
        """Get the Cheese of the Day from cheese.com."""
        async with self.bot.http_session.get(Cheese.BASE) as response:
            landing_html = await response.text()
        soup = bs4.BeautifulSoup(landing_html, 'lxml')
        name = soup.find("a", class_="more").get("href")[1:-1]
        url = f"{Cheese.BASE}/{name}"
        print("Accessing Cheese of the Day", url)

        async with self.bot.http_session.get(url) as response:
            cheese_html = await response.text()
        soup = bs4.BeautifulSoup(cheese_html, 'lxml')
        image_url = soup.find('div', class_='cheese-image-border').a.img['src']
        image_url = f"{Cheese.BASE}/{image_url}"
        description_ps = soup.find("div", class_="description").find_all("p")
        description = "\n".join([p.text for p in description_ps]).strip()
        attribution = soup.find("div", class_="image-license").text.strip()
        summary_points = [
            Cheese.summary_point(soup, "🥛", "summary_milk"),
            Cheese.country_summary_point(soup),
            Cheese.summary_point(soup, "📁", "summary_moisture_and_type"),
            Cheese.summary_point(soup, "📊", "summary_texture"),
            Cheese.summary_point(soup, "💧", "summary_tint"),
            Cheese.summary_point(soup, "🥄", "summary_taste"),
            Cheese.summary_point(soup, "🍴", "summary_smell"),
            Cheese.summary_point(soup, "🥚", "summary_vegetarian"),
            Cheese.summary_point(soup, "🌿", "summary_vegan"),
            Cheese.summary_point(soup, "📖", "summary_synonym"),
        ]
        description += "\n" + "\n".join(summary_points)

        embed = Crombed(
            title=name.upper(),
            description=description,
            url=url,
        ).set_footer(text=attribution).set_image(url=image_url)
        await ctx.send(embed=embed)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cheese(bot))
