import asyncio

from pytgcalls import GroupCallFactory
from telethon import TelegramClient, events
from telethon.tl import functions, types
from telethon.tl.types import PeerChat, ChatFull, Chat
from telethon.tl.types.phone import GroupParticipants

import config

async def participants_are_updated(group_call, participants):
    print(f'Updated participant list: {participants}')

app = TelegramClient("remove_inactive", config.api_id, config.api_hash).start()
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON)
group_call = group_call_factory.get_file_group_call('input.raw')
group_call.on_participant_list_updated(participants_are_updated)


## @group_call.on_participant_list_updated
async def participants_are_updated(group_call2, participants):
    print("--")
    gr: ChatFull = await app(functions.messages.GetFullChatRequest(-1 * config.GROUP))
    print(f'Updated participant list: {participants}')
    for participant in participants:
        if participant.video is not None and not participant.is_self:
            await app(functions.phone.EditGroupCallParticipantRequest(
                call=gr.full_chat.call,
                participant=config.nyx,
                muted=True,
                volume=participant.volume,
                video_stopped=True,
                video_paused=False,
            ))
        await group_call2.edit_group_call_member(participant.peer.user_id, muted=True)
        print(participant.video is not None)


app.run_until_disconnected()
