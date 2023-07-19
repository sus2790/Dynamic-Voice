from enum import Enum


class Emojis(Enum):
    CROSS = "<a:cross:850333988962959391>"
    SUCCESSFUL = "<a:successful:781204776641626162>"
    JOIN = "<:join:1117112971928277183>"
    LEAVE = "<:leave:1117113002945163305>"
    TEXT = "<:text:1117124300042948718>"
    SAD = "<a:sad:1118488178295320606>"
    CHANGE = "<:change:1118882316677296158>"
    SETTING = "<:setting:1118892230099337267>"
    VOICE = "<:voice:1118901269134852340>"
    LOADING = "<a:loading:1118922788376424579>"
    MENU = "<:menu:1119654045842415677>"
    DATA = "<:database:1129755410199486475>"

    def __str__(self) -> str:
        return str(self.value)
