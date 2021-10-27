import requests
import json
from bs4 import BeautifulSoup
import re
from discord.ext import commands

all = 0
bot = commands.Bot(command_prefix='!')

with open('config.json', 'r', encoding='utf-8') as json_config:
    data = json.load(json_config)

header = {
    'User-Agent': data['user_agent']
}


@bot.command(pass_context=True)
async def themes(ctx, server, num):
    try:
        server = int(server)
        num = int(num)
        num_of_page = int(num)
        url = f'https://forum.advance-rp.ru/forums/{server}/page-'
        global all
        all = 0
        for i in range(1, num_of_page + 1):
            response = requests.get(url + str(i), headers=header)
            html = BeautifulSoup(response.content, 'html.parser')
            elements = []
            for el in html.select('.structItem'):
                if not el.select('.structItem-statuses .structItem-status--locked'):
                    elements.append({
                        'prefix': el.select('.structItem-title > a .label'),
                        'title': el.select('.structItem-title > a[data-xf-init]'),
                        'link': el.select('.structItem-title > a[data-xf-init]')[0]['href']
                    })
            if elements:
                await ctx.send(f'[Страница {i}, всего {len(elements)}]')
                all = all + len(elements)
            for elem in elements:
                number = re.sub("[^0-9]", "", elem['link'])
                link = 'https://forum.advance-rp.ru/threads/' + number
                if len(elem['prefix']):
                    await ctx.send('[' + elem['prefix'][0].text + '] ' + elem['title'][0].text + ': ' + f'<{link}>')
                else:
                    await ctx.send(elem['title'][0].text + ': ' + f'<{link}>')
        await ctx.send(f'Проверено {num} страниц. Всего открытых тем: {all}')
        if all == 0:
            await ctx.send('[Возможно неверно указан номер подфорума, либо количество страниц]')
    except Exception as ex:
        print(ex)
        await ctx.send('Проверьте правильность ввода данных')


@bot.command(pass_context=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


bot.run(data['token'])
