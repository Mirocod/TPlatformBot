# -*- coding: utf8 -*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

# Языки

from bot_sys import bot_bd, keyboard, user_access, bd_table
from bot_modules import mod_table_operate, mod_simple_message, access_utils
from template import bd_item

# ---------------------------------------------------------
# БД
module_name = 'languages'

table_name = module_name
key_name = 'languageID'
name_field = 'languageName'
desc_field = 'languageDesc'
photo_field = 'languagePhoto'
access_field = 'languageAccess'
create_datetime_field = 'languageCreateDateTime'

table_name_field = bd_table.TableField(name_field, bd_table.TableFieldDestiny.NAME, bd_table.TableFieldType.STR)

table = bd_table.Table(table_name, [
        bd_table.TableField(key_name, bd_table.TableFieldDestiny.KEY, bd_table.TableFieldType.INT),
        table_name_field,
        bd_table.TableField(desc_field, bd_table.TableFieldDestiny.DESC, bd_table.TableFieldType.STR),
        bd_table.TableField(photo_field, bd_table.TableFieldDestiny.PHOTO, bd_table.TableFieldType.STR),
        bd_table.TableField(access_field, bd_table.TableFieldDestiny.ACCESS, bd_table.TableFieldType.STR),
        bd_table.TableField(create_datetime_field, bd_table.TableFieldDestiny.CREATE_DATE, bd_table.TableFieldType.STR),
        ],
        [
            [table_name_field],
        ]
)

init_access = f'{user_access.user_access_group_all}=-'

# ---------------------------------------------------------
# Сообщения и кнопки

button_names = {
    mod_simple_message.ButtonNames.START: "⚑ Языки",
    mod_table_operate.ButtonNames.LIST: "📃 Список языков",
    mod_table_operate.ButtonNames.ADD: "✅ Добавить язык",
    mod_table_operate.ButtonNames.EDIT: "🛠 Редактировать язык",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.PHOTO): "☐ Изменить изображение в языке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.NAME): "≂ Изменить название в языке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.DESC): "𝌴 Изменить описание в языке",
    mod_table_operate.EditButton(bd_table.TableFieldDestiny.ACCESS): "✋ Изменить доступ к языку",
    mod_table_operate.ButtonNames.DEL: "❌ Удалить язык",
}

messages = {
    mod_simple_message.Messages.START: f'''
<b>{button_names[mod_simple_message.ButtonNames.START]}</b>

''',
    mod_table_operate.Messages.SELECT: '''
Пожалуйста, выберите язык:
''',
    mod_table_operate.Messages.ERROR_FIND: '''
❌ Ошибка, язык не найден
''',
    mod_table_operate.Messages.OPEN: f'''
<b>Язык:  #{name_field}</b>

#{desc_field}

Время создания: #{create_datetime_field}
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.NAME): '''
Создание языка. Шаг №1

Введите название языка:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.DESC): '''
Создание языка. Шаг №2

Введите описание языка:
''',
    mod_table_operate.CreateMessage(bd_table.TableFieldDestiny.PHOTO): '''
Создание языка. Шаг №3

Загрузите обложку для языка (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.Messages.SUCCESS_CREATE: '''✅ Язык успешно добавлен!''',
    mod_table_operate.Messages.START_EDIT: '''
Пожалуйста, выберите действие:
''',
    mod_table_operate.Messages.SELECT_TO_EDIT: '''
Выберите язык, который вы хотите отредактировать.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.PHOTO): '''
Загрузите новую обложку для языка (Фото):
Она будет отображаться в его описании.
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.NAME): f'''
Текущее название языка:
#{name_field}

Введите новое название языка:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.DESC): f'''
Текущее описание языка:
#{desc_field}

Введите новое описание языка:
''',
    mod_table_operate.EditMessage(bd_table.TableFieldDestiny.ACCESS): f'''
Текущий доступ к языку:
#{access_field}

{user_access.user_access_readme}

Введите новую строку доступа:
''',
    mod_table_operate.Messages.SUCCESS_EDIT: '''✅ Язык успешно отредактирован!''',
    mod_table_operate.Messages.SELECT_TO_DELETE: '''
Выберите язык, который вы хотите удалить.
Все задачи и потребности в этом языке так же будут удалены!
''',
    mod_table_operate.Messages.SUCCESS_DELETE: '''✅ Язык успешно удалён!''',
}

class ModuleLanguages(mod_table_operate.TableOperateModule):
    def __init__(self, a_ParentModName, a_ChildModName, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log):
        super().__init__(table, messages, button_names, a_ParentModName, a_ChildModName, init_access, a_ChildModuleNameList, a_EditModuleNameList, a_Bot, a_ModuleAgregator, a_BotMessages, a_BotButtons, a_Log)
        self.m_LanguageIDs = {}

    def GetName(self):
        return module_name

    def GetLangID(self, a_Lang):
        return self.m_LanguageIDs.get(a_Lang, None)

    def GetLangName(self, a_LangID):
        for lang_name, lang_id in self.m_LanguageIDs:
            if a_LangID == lang_id:
                return lang_name
        return self.m_BotMessages.m_DefaultLanguage

    def FlushLanguages(self):
        msg = self.m_BotMessages.GetMessages()
        for lang, msg_dict in msg.items():
            self.AddOrIgnoreLang(lang)
        langs = bd_item.GetAllItemsTemplate(self.m_Bot, table_name)()
        if langs:
            for l in langs:
                self.m_LanguageIDs[l[1]] = str(l[0])
        print('FlushLanguages', self.m_LanguageIDs)

    def AddOrIgnoreLang(self, a_Lang : str):
        table_name = self.m_Table.GetName()
        name_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.NAME)
        photo_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.PHOTO)
        desc_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.DESC)
        access_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.ACCESS)
        create_datetime_field = self.m_Table.GetFieldNameByDestiny(bd_table.TableFieldDestiny.CREATE_DATE)

        res, error = self.m_Bot.SQLRequest(f'INSERT OR IGNORE INTO {table_name}({photo_field}, {name_field}, {desc_field}, {access_field}, {create_datetime_field}) VALUES(?, ?, ?, ?, {bot_bd.GetBDDateTimeNow()})', 
                commit = True, return_error = True, param = (0, a_Lang, '', access_utils.GetItemDefaultAccessForModule(self.m_Bot, module_name)))

    def OnChange(self):
        self.FlushLanguages()

