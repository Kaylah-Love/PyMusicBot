queue = {}

def clear_queue(guildId):
    if guildId in queue:
        del queue[guildId]

def get_queue(guildId):
    return queue.get(guildId)

def add_to_queue(guildId, videoInfo):
    if guildId not in queue:
        queue[guildId] = [videoInfo]
    else:
        queue[guildId].append(videoInfo)

def pop_from_queue(guildId):
    if guildId in queue:
        return queue[guildId].pop(0)
    return None

def is_queue_empty(guildId):
    return guildId not in queue or len(queue[guildId]) == 0

def get_queue_length(guildId):
    return len(queue.get(guildId, [])) if guildId in queue else 0
