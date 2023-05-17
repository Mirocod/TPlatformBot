#-*-coding utf-8-*-
# Общественное достояние, 2023, Алексей Безбородов (Alexei Bezborodov) <AlexeiBv+mirocod_platform_bot@narod.ru> 

from enum import Enum
from enum import auto

# Тип поля в таблице
class TableFieldType(Enum):
    INT = 'INTEGER'
    STR = 'TEXT'

# Предназначение поля в таблице
class TableFieldDestiny(Enum):
    KEY = auto()
    NAME = auto()
    DESC = auto()
    PHOTO = auto()
    ACCESS = auto()
    DEFAULT_ACCESS = auto()
    CREATE_DATE = auto()
    PARENT_ID = auto()
    OTHER = auto()

class TableField:
    def __init__(self, a_Name, a_Destiny : TableFieldDestiny, a_Type : TableFieldType):
        self.m_Name = a_Name
        self.m_Destiny = a_Destiny
        self.m_Type = a_Type

class Table:
    def __init__(self, a_TableName, a_Fields : [TableField]):
        self.m_TableName = a_TableName
        self.m_Fields = a_Fields

    def GetName(self):
        return self.m_TableName

    def GetFields(self):
        return self.TableFieldType

    def GetFieldsCount(self):
        return len(self.m_Fields)

    def GetFieldByDestiny(self, a_Destiny):
        for f in self.m_Fields:
            if f.m_Destiny == a_Destiny:
                return f
        return None

    def GetFieldNameByDestiny(self, a_Destiny):
        f = self.GetFieldByDestiny(a_Destiny)
        if f:
            return f.m_Name
        return None

    def GetFieldIDByDestiny(self, a_Destiny):
        for i in range(len(self.m_Fields)):
            f = self.m_Fields[i]
            if f.m_Destiny == a_Destiny:
                return i
        return None

    def GetInitTableRequest(self):
        request = f'CREATE TABLE IF NOT EXISTS {self.GetName()}('
        fields = []
        for f in self.m_Fields:
            key_str = ''
            if f.m_Destiny == TableFieldDestiny.KEY:
                key_str = 'PRIMARY KEY'
            fields += [' '.join([f.m_Name, str(f.m_Type.value), key_str])]
        return request + ', '.join(fields) + ');'

    def ReplaceAllFieldTags(self, a_String, a_BDItem):
        result = a_String
        for i in range(len(self.m_Fields)):
            f = self.m_Fields[i]
            result = result.replace(f'#{f.m_Name}', str(a_BDItem[i]))
        return result

def Test():
    table = Table('tname', [
            TableField('f1', TableFieldDestiny.KEY, TableFieldType.INT),
            TableField('f2', TableFieldDestiny.NAME, TableFieldType.STR),
            TableField('f3', TableFieldDestiny.DESC, TableFieldType.STR),
            ])
    assert table.GetName() == 'tname'
    assert table.GetFieldByDestiny(TableFieldDestiny.KEY).m_Name == 'f1'
    assert table.GetFieldNameByDestiny(TableFieldDestiny.KEY) == 'f1'
    assert table.GetFieldByDestiny(TableFieldDestiny.KEY).m_Destiny == TableFieldDestiny.KEY
    assert table.GetFieldByDestiny(TableFieldDestiny.KEY).m_Type == TableFieldType.INT
    assert table.GetFieldIDByDestiny(TableFieldDestiny.KEY) == 0
    assert table.GetFieldByDestiny(TableFieldDestiny.NAME).m_Name == 'f2'
    assert table.GetFieldNameByDestiny(TableFieldDestiny.NAME) == 'f2'
    assert table.GetFieldByDestiny(TableFieldDestiny.NAME).m_Destiny == TableFieldDestiny.NAME
    assert table.GetFieldByDestiny(TableFieldDestiny.NAME).m_Type == TableFieldType.STR
    assert table.GetFieldIDByDestiny(TableFieldDestiny.NAME) == 1
    assert table.GetFieldByDestiny(TableFieldDestiny.DESC).m_Name == 'f3'
    assert table.GetFieldNameByDestiny(TableFieldDestiny.DESC) == 'f3'
    assert table.GetFieldByDestiny(TableFieldDestiny.DESC).m_Destiny == TableFieldDestiny.DESC
    assert table.GetFieldByDestiny(TableFieldDestiny.DESC).m_Type == TableFieldType.STR
    assert table.GetFieldIDByDestiny(TableFieldDestiny.DESC) == 2

    assert table.GetFieldByDestiny(TableFieldDestiny.PHOTO) == None
    assert table.GetFieldIDByDestiny(TableFieldDestiny.PHOTO) == None
    assert table.GetFieldNameByDestiny(TableFieldDestiny.PHOTO) == None

    assert table.GetFieldsCount() == 3

    assert table.GetInitTableRequest() == 'CREATE TABLE IF NOT EXISTS tname(f1 INTEGER PRIMARY KEY, f2 TEXT , f3 TEXT );'

    item = [10, 'i1', 'i2']
    assert table.ReplaceAllFieldTags('#f1 #f2 #f3', item) == '10 i1 i2'
