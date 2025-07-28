# --- 必要的引用 ---
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger


# --- 插件注册 ---
@register(
    "my_cool_plugin",
    "你的名字",
    "我的第一个超酷插件",
    "1.0.0"
)
class MyCoolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # --- 消息监听器 ---
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def my_universal_handler(self, event: AstrMessageEvent):
        msg_text = event.message_str
        user_id = event.get_sender_id()

        # --- 你的逻辑区 ---

        # 示例1：关键词回复
        if "笨笨豆" == msg_text:
            yield event.plain_result("很笨")
