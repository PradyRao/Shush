import sys
import logging
import importlib

import discord

from Framework import time_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))
env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))


async def process_leave_end(member: discord.Member, voice_state: discord.VoiceState):
    # check if the user that left was previously practicing
    if str(voice_state.channel.id) in var_config.practicemap.keys() and var_config.practicemap[str(voice_state.channel.id)] == str(member.id):
        # get text channel associated with the voice channel that user left from
        text_channel = voice_state.channel.guild.get_channel(int(var_config.broadcastchs[str(voice_state.channel.id)]))

        # user's total time practiced
        logging.log(level=logging.INFO, msg=f'processing time practiced for {member.name}#{member.discriminator} id:{member.id}')
        time_practiced_seconds = time_utils.time_practiced_seconds(voice_state.channel.id)
        time_practiced = time_utils.time_readable(time_practiced_seconds)

        # update user's time in the database and update server total time - not implemented
        logging.log(level=logging.INFO, msg=f'updating database entry for user {member.name}#{member.discriminator} id:{member.id}')

        # reset practicemap for this channel - part 1/2
        logging.log(level=logging.INFO, msg=f'resetting practice slot for channel {voice_state.channel.name} id: {voice_state.channel.id}')
        del var_config.practicemap[str(voice_state.channel.id)]
        del var_config.practicemap[str(voice_state.channel.id) + 'start_time']
        if str(voice_state.channel.id) + 'piece' in var_config.practicemap.keys():
            del var_config.practicemap[str(voice_state.channel.id) + 'piece']

        await text_channel.send(content=f'{member.name}#{member.discriminator} practice session ended. they practiced '
                                  f'for {time_practiced[1]} hours {time_practiced[2]} minutes and {time_practiced[3]} seconds')

        # remute all excused members
        logging.log(level=logging.INFO, msg=f'resetting all excused members in voice channel {voice_state.channel.name} id: {voice_state.channel.id}')
        # if this channel's excused key exists in practice map, and if the list value of that key is not empty
        if str(voice_state.channel.id) + 'excused' in var_config.practicemap.keys() and var_config.practicemap[str(voice_state.channel.id) + 'excused']:
            # get the list of all excused members
            excused_members = var_config.practicemap[str(voice_state.channel.id) + 'excused']
            # for each user in that voice channel
            for user in voice_state.channel.members:
                # if the user is excused, re-mute them
                if user.id in excused_members:
                    await user.edit(mute=True)

        # reset excused in practicemap as well - part 2/2
        if str(voice_state.channel.id) + 'piece' in var_config.practicemap.keys():
            del var_config.practicemap[str(voice_state.channel.id) + 'excused']

        # reset the bit rate and the user limit of the channel
        logging.log(level=logging.INFO, msg=f'resetting bit rate and user limit for channel {voice_state.channel.name} id: {voice_state.channel.id}')
        await voice_state.channel.edit(bitrate=var_config.bit_tier[voice_state.channel.guild.premium_tier], user_limit=0)

    # check if channel's excused key exists in practicemap, and if the user that left was excused in the voice channel they were in
    elif str(voice_state.channel.id) + 'excused' in var_config.practicemap.keys() and \
            str(member.id) in var_config.practicemap[str(voice_state.channel.id) + 'excused']:
        logging.log(level=logging.INFO, msg=f'excused user {member.name}#{member.discriminator} id:{member.id} left. removing entry from voice channel {voice_state.channel.name} id:'
                                            f' {voice_state.channel.id}')

        # remove their entry from the excused list
        var_config.practicemap[str(voice_state.channel.id) + 'excused'].remove(member.id)

    # user is not practicing nor excused
    else:
        return

