# --- 必要的引用 ---
import httpx  # 导入 httpx
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp  # 导入消息组件，用来识别回复


# --- 插件注册 ---
@register("my_cool_plugin", "你的名字", "我的第一个超酷插件", "1.0.0")
class MyCoolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 定义 Napcat API 的地址
        self.napcat_api_base_url = "http://127.0.0.1:6099/"  # !!! 请改成你自己的地址 !!!

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def my_universal_handler(self, event: AstrMessageEvent):
        msg_text = event.message_str

        # --- 新功能：贴表情 ---
        if msg_text.strip() == "/like" or msg_text.strip() == "/贴表情":
            # 1. 检查用户是否回复了某条消息
            reply_component = event.get_first_component(Comp.Reply)
            if not reply_component:
                yield event.plain_result("请回复一条消息来使用此功能哦~")
                return  # 结束处理

            # 2. 获取被回复消息的 message_id
            target_message_id = reply_component.id

            # 3. 定义要发送的表情 ID (可以查阅相关文档或自行测试)
            # 这里的 emoji_id 通常是 Unicode 编码的十六进制表示或其他特定格式
            # 我们先用一个常见的点赞表情做例子，具体 ID 可能需要你测试
            # 比如 QQ 的 "小黄脸点赞" 的 ID 可能是 '100' 或者其他值
            emoji_to_send = "8"  # 假设 "哭" 的 ID 是 '100'

            logger.info(f"检测到贴表情指令，目标消息ID: {target_message_id}, 表情ID: {emoji_to_send}")

            # 4. 准备请求体
            payload = {
                "message_id": int(target_message_id),
                "emoji_id": emoji_to_send,
                "set": True  # True是贴上，False是取消
            }

            # 5. 发送 HTTP 请求
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.napcat_api_base_url}/set_msg_emoji_ku",
                        json=payload
                    )
                    response.raise_for_status()
                    logger.info(f"Napcat API 响应: {response.text}")
                    # 成功后可以不回复，或者撤回用户的指令消息
                    # 这里我们不回复，让效果更自然

            except httpx.HTTPStatusError as e:
                logger.error(f"调用 Napcat 贴表情 API 失败，状态码: {e.response.status_code}, 响应: {e.response.text}")
                yield event.plain_result("贴表情失败了，可能是表情ID不对或者机器人权限不够。")
            except Exception as e:
                logger.error(f"调用 Napcat 贴表情 API 时发生未知错误: {e}")
                yield event.plain_result("贴表情时发生了意料之外的错误。")

        # --- 你原来的逻辑可以保留 ---
        if "笨笨豆" == msg_text:
            yield event.plain_result("很笨")
