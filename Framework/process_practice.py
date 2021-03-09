import logging

import discord

from Config import env_dev
from Config import var_config


def process_leave_end(member: discord.Member, voice_state: discord.VoiceState):
    # check if the user that left was previously practicing
    if var_config.practicemap[str(voice_state.channel.id)] == str(member.id):
        # get text channel associated with the voice channel that user left from
        text_channel = voice_state.channel.guild.get_channel(var_config.broadcastchs[str(voice_state.channel.id)])

        # user's total time practiced
        logging.log(level=logging.INFO, msg=f'processing time practiced for {member.name}#{member.discriminator} id:{member.id}')
        time_practiced = [0, 0, 0, 0]

        # update user's time in the database and update server total time
        logging.log(level=logging.INFO, msg=f'updating database entry for user {member.name}#{member.discriminator} id:{member.id}')

        # reset practicemap for this channel
        logging.log(level=logging.INFO, msg=f'resetting practice slot for channel {voice_state.channel.name} id: {voice_state.channel.id}')
        var_config.practicemap[str(voice_state.channel.id)] = None
        var_config.practicemap[str(voice_state.channel.id) + 'piece'] = None

        text_channel.send(content=f'{member.name}#{member.discriminator} practice session ended. they practiced '
                                  f'for {time_practiced[1]} hours {time_practiced[2]} minutes and {time_practiced[3]} seconds')

        # remute all excused members
        logging.log(level=logging.INFO, msg=f'resetting all excused members in voice channel {voice_state.channel.name} id: {voice_state.channel.id}')
        if str(voice_state.channel.id) + 'excused' in var_config.practicemap.keys() and var_config.practicemap[str(voice_state.channel.id) + 'excused']:
            excused_members = var_config.practicemap[voice_state.channel.id + 'excused']
            for user in voice_state.channel.members:
                if user.id in excused_members:
                    user.edit(mute=False)

        var_config.practicemap[str(voice_state.channel.id) + 'excused'] = []

        # reset the bitrate and the user limit of the channel
        logging.log(level=logging.INFO, msg=f'resetting bitrate and user limit for channel {voice_state.channel.name} id: {voice_state.channel.id}')
        voice_state.channel.edit(bitrate=var_config.bit_tier[voice_state.channel.guild.premium_tier], user_limit=0)

    elif str(voice_state.channel.id) + 'excused' in var_config.practicemap.keys() and \
            str(member.id) in var_config.practicemap[str(voice_state.channel.id) + 'excused']:
        logging.log(level=logging.INFO, msg=f'excused user left. resetting from voice channel {voice_state.channel.name} id: {voice_state.channel.id}')
        var_config.practicemap[str(voice_state.channel.id) + 'excused'].remove(str(member.id))
