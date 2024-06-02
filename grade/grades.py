import discord
from discord.ext import commands

available_roles = {
    "Member": 0,
    "Bot": 1,
    "Grad2": 2,
    "Grad2": 3,
    "Grad2": 4,
    "Grad2": 5,
    "Grad2": 6,
    "Grad2": 7,
    "Administrtor": 8,
}

async def add_role(ctx, member: discord.Member, role_name: str):
    if role_name in available_roles:
        role_id = available_roles[role_name]
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        
        if role:
            try:
                await member.add_roles(role)
                await ctx.send(f"Rolul {role_name} a fost atribuit membrului {member.mention}.")
            except discord.Forbidden:
                await ctx.send("Nu am permisiunea să atribui acest rol.")
            except Exception as e:
                await ctx.send(f"A apărut o eroare în timpul atribuirii rolului: {e}")
        else:
            await ctx.send("Rolul nu există pe server.")
    else:
        await ctx.send("Rolul specificat nu este în lista de grade disponibile.")

async def find_member_by_name(guild, member_name):
    for member in guild.members:
        if member_name.lower() == member.name.lower() + '#' + member.discriminator:
            return member
    return None