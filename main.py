from discord import channel, Embed, client, member
from discord.ext import commands
import discord
from mojang import MojangAPI
from mcrcon import MCRcon
import json

global whitejson
global tituloembed
global logoembled
global token
global host
global port
global password
global canaldediscord
global rolesdedicord

##### Personalizacion

canaldediscord = <id_del_canal>
#rolesdedicord = "11111111111 , 2222222222"
whitejson = "<directorio>/Minecraft/whitelist.json"
tituloembed = "Titulo"
logoembled = "https://ejemplo.es/img/Logo.png"
token = "tocken de discord"

### MCRON

host = "localhost"
port = 25575
password = "password"


class switch:

    def __init__(self, variable, comparator=None, strict=False):
        self.variable = variable
        self.matched = False
        self.matching = False
        if comparator:
            self.comparator = comparator
        else:
            self.comparator = lambda x, y: x == y
        self.strict = strict

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def case(self, expr, break_=False):
        if self.strict:
            if self.matched:
                return False
        if self.matching or self.comparator(self.variable, expr):
            if not break_:
                self.matching = True
            else:
                self.matched = True
                self.matching = False
            return True
        else:
            return False

    def default(self):
        return not self.matched and not self.matching


bot = commands.Bot(command_prefix='>', description="Bot creado y gestionado por @Sorienrot")


@bot.event
async def on_ready():
    print('El bot de Mine Angela se esta ejecutando')


@bot.command()
@commands.has_any_role(1111111111, 2222222222)
async def whitelist(ctx, estado=None, nombre=None):
    global whitejson
    global tituloembed
    global logoembled
    global token
    global host
    global port
    global password
    global canaldediscord
    global rolesdedicord
    if ctx.channel.id == canaldediscord:
        if estado is None:
            await ctx.send("No has puesto que hacer!!!. Pon >whitelist add o >whitelist del")
        else:
            with switch(estado) as s:
                if s.case("add", True):
                    if nombre is None:
                        await ctx.send("No has puesto el nombre!!!!")
                        return
                    with open(whitejson) as f:
                        whitedata = json.load(f)
                    total = len(whitedata)
                    for X in range(total):
                        n = whitedata[X]['name']
                        if n == nombre:
                            await ctx.send("Este usuario ya existe")
                            return
                    uuid = MojangAPI.get_uuid(nombre, timestamp=None)
                    if uuid is None:
                        await ctx.send("El usuario {} no existe".format(nombre))
                        return
                    resultado = uuid[:8] + "-" + uuid[8:]
                    resultado = resultado[:13] + "-" + resultado[13:]
                    resultado = resultado[:18] + "-" + resultado[18:]
                    resultado = resultado[:23] + "-" + resultado[23:]
                    ingreso = {'uuid': resultado, 'name': nombre}
                    whitedata.append(ingreso)
                    with open(whitejson, 'w') as salida:
                        json.dump(whitedata, salida)
                    embed = discord.Embed(title=nombre, description="Se le ha añadido a la whitelist")
                    embed.set_author(name=tituloembed, icon_url=logoembled)
                    embed.set_thumbnail(url="https://crafatar.com/avatars/{}".format(uuid))
                    await ctx.send(embed=embed)
                    mcr = MCRcon(host, password, port)
                    mcr.connect()
                    mcr.command("/whitelist reload")
                    mcr.disconnect()
                if s.case("del", True):
                    if nombre is None:
                        await ctx.send("No has puesto el nombre!!!!")
                        return
                    uuid = MojangAPI.get_uuid(nombre, timestamp=None)
                    if uuid is None:
                        await ctx.send("El usuario {} no existe".format(nombre))
                        return
                    with open(whitejson) as f:
                        whitedata = json.load(f)
                    total = len(whitedata)
                    for x in range(total):
                        n = whitedata[x]['name']
                        if n == nombre:
                            del whitedata[x]
                            with open(whitejson, 'w') as salida:
                                json.dump(whitedata, salida)
                            embed = discord.Embed(title=nombre, description="Se le ha eliminado de la whitelist")
                            embed.set_author(name=tituloembed,
                                             icon_url=logoembled)
                            embed.set_thumbnail(url="https://crafatar.com/avatars/{}".format(uuid))
                            await ctx.send(embed=embed)
                            try:
                                mcr = MCRcon(host, password, port)
                                mcr.connect()
                                mcr.command("/whitelist reload")
                                mcr.disconnect()
                            except:
                                pass
                            return
                    await ctx.send("No existe ese usuario en la lista")
                    if s.case("list", True):
                        pass


bot.run(token)