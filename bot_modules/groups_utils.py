# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы пользователей

from bot_sys import user_access

def GetUserGroupData(a_Bot, a_UserID):
    def GetGroupNamesForUser(a_UserID):
        return a_Bot.SQLRequest('SELECT groupName FROM user_groups WHERE group_id=(SELECT group_id FROM user_in_groups WHERE user_id = ?)', param = [a_UserID])
    r = GetGroupNamesForUser(a_UserID)
    groups = []
    for i in r:
        if len(i) > 0:
            groups += [i[0]]
    return user_access.UserGroups(a_UserID, groups)
