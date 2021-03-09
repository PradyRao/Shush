import logging

import discord

from Config import env_dev
from Config import var_config


def process_leave_end(member: discord.Member, voice_state: discord.VoiceState, state_type: str):
    # check if the user that left was previously practicing
    if var_config.practicemap[str(voice_state.channel.id)] == str(member.id):
        # get text channel associated with the voice channel that user left from
        text_channel = voice_state.channel.guild.get_channel(int(var_config.broadcastchs[str(voice_state.channel.id)]))

        # user's total time practiced - not implemented
        logging.log(level=logging.INFO, msg=f'processing time practiced for {member.name}#{member.discriminator} id:{member.id}')
        time_practiced = [0, 0, 0, 0]

        # update user's time in the database and update server total time - not implemented
        logging.log(level=logging.INFO, msg=f'updating database entry for user {member.name}#{member.discriminator} id:{member.id}')

        # we need to re-mute the member since were practicing
        # only if they move to a configured voice channel
        # already handled by state_type
        if state_type == "move":
            member.edit(mute=True)

        # reset practicemap for this channel
        logging.log(level=logging.INFO, msg=f'resetting practice slot for channel {voice_state.channel.name} id: {voice_state.channel.id}')
        del var_config.practicemap[str(voice_state.channel.id)]
        del var_config.practicemap[str(voice_state.channel.id) + 'piece']

        text_channel.send(content=f'{member.name}#{member.discriminator} practice session ended. they practiced '
                                  f'for {time_practiced[1]} hours {time_practiced[2]} minutes and {time_practiced[3]} seconds')

        # remute all excused members
        logging.log(level=logging.INFO, msg=f'resetting all excused members in voice channel {voice_state.channel.name} id: {voice_state.channel.id}')
        # if this channel's excused key exists in practice map, and if the list value of that key is not empty
        if str(voice_state.channel.id) + 'excused' in var_config.practicemap.keys() and var_config.practicemap[str(voice_state.channel.id) + 'excused']:
            # get the list of all excused members
            excused_members = var_config.practicemap[voice_state.channel.id + 'excused']
            # for each user in that voice channel
            for user in voice_state.channel.members:
                # if the user is excused, re-mute them
                if user.id in excused_members:
                    user.edit(mute=True)

        del var_config.practicemap[str(voice_state.channel.id) + 'excused']

        # reset the bit rate and the user limit of the channel
        logging.log(level=logging.INFO, msg=f'resetting bit rate and user limit for channel {voice_state.channel.name} id: {voice_state.channel.id}')
        voice_state.channel.edit(bitrate=var_config.bit_tier[voice_state.channel.guild.premium_tier], user_limit=0)

    # this channel's excused key exists in practice map, and if the user that left was excused in the voice channel they were in
    elif str(voice_state.channel.id) + 'excused' in var_config.practicemap.keys() and \
            str(member.id) in var_config.practicemap[str(voice_state.channel.id) + 'excused']:
        logging.log(level=logging.INFO, msg=f'excused user {member.name}#{member.discriminator} id:{member.id} left. resetting from voice channel {voice_state.channel.name} id:'
                                            f' {voice_state.channel.id}')

        # we need to re-mute the member since they were excused
        # only if they moved to another configured voice channel
        # already handled by state_type
        if state_type == "move":
            member.edit(mute=True)

        # remove their entry from the excused list
        var_config.practicemap[str(voice_state.channel.id) + 'excused'].remove(str(member.id))

    # user is not practicing nor excused
    else:
        logging.log(level=logging.INFO, msg=f'user {member.name}#{member.discriminator} id:{member.id} left configured voice channel {voice_state.channel.name} id: {voice_state.channel.id}')
        # here all we have to check is whether user is leaving or moving to an unconfigured channel
        # already handled by state_type
        if state_type == "leave":
            member.edit(mute=False)
        # this is really not necessary because if they were not practicing or excused they would be muted already, but I'll keep it here anyways
        elif state_type == 'move':
            member.edit(mute=True)

