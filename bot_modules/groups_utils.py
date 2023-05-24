# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Группы пользователей

from bot_sys import user_access

table_name = 'user_groups'
key_name = 'groupID'
name_field = 'groupName'
desc_field = 'groupDesc'
photo_field = 'groupPhoto'
access_field = 'groupAccess'
create_datetime_field = 'groupCreateDateTime'

table_user_in_groups_name = 'user_in_groups'
user_id_field = 'user_ID'
parent_id_field = 'groupID'

def GetUserGroupData(a_Bot, a_UserID):
    def GetGroupNamesForUser(a_UserID):
        sql_req = f'SELECT {name_field} FROM {table_name} WHERE {key_name} IN (SELECT {parent_id_field} FROM {table_user_in_groups_name} WHERE {user_id_field} = ?)'
        #print('GetGroupNamesForUser', sql_req)
        return a_Bot.SQLRequest(sql_req, param = [a_UserID])
    r = GetGroupNamesForUser(a_UserID)
    groups = []
    for i in r:
        if len(i) > 0:
            groups += [i[0]]
    return user_access.UserGroups(a_UserID, groups)
