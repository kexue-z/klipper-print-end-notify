import http.client
import urllib


class PrintEndNotify:
    def __init__(self, config) -> None:
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object("gcode")
        self.print_stats = self.printer.lookup_object("print_stats")
        self.reactor = self.printer.get_reactor()

        # 配置
        self.api_key = config.get("api_key")
        self.user_key = config.get("user_key")
        self.timeout = config.get("timeout", 10)

        # Register commands
        self.gcode.register_command(
            "PRINT_END_NOTIFY",
            self.cmd_PRINT_END_NOTIFY,
            desc=self.cmd_PRINT_END_NOTIFY_help,
        )

    cmd_PRINT_END_NOTIFY_help = "发送打印完成通知到 PushOver 中"

    def cmd_PRINT_END_NOTIFY(self, params):
        title = "3D打印完成"
        device_id = params.get("DEVICE", "")
        sound = params.get("SOUND", "")

        try:
            curtime = self.reactor.monotonic()
            status = self.print_stats.get_status(curtime)

            filename = status["filename"]

            total_duration = status["total_duration"]
            total_hours = int(total_duration / 3600)
            total_minutes = int((total_duration % 3600) / 60)
            total_seconds = int(total_duration % 60)

            # 转换打印时长为时分秒格式
            print_duration = status["print_duration"]
            print_hours = int(print_duration / 3600)
            print_minutes = int((print_duration % 3600) / 60)
            print_seconds = int(print_duration % 60)

            # 转换用料为米并保留两位小数
            filament_used = round(status["filament_used"] / 1000, 2)
            message = (
                f"文件名: {filename}\n"
                f"总时长：{total_hours} 时 {total_minutes} 分 {total_seconds}秒\n"
                f"打印时长：{print_hours} 时 {print_minutes} 分 {print_seconds} 秒\n"
                f"消耗材料：{filament_used} 米"
            )

        except:  # noqa
            self.gcode.error("Error")
            return

        # 发送消息
        self.gcode.respond_info(f"发送消息: \n{title}\n{message}")
        conn = http.client.HTTPSConnection(
            "api.pushover.net", 443, timeout=self.timeout
        )
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode(
                {
                    "token": self.api_key,
                    "user": self.user_key,
                    "device": device_id,
                    "title": title,
                    "sound": sound,
                    "message": message,
                }
            ),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        response = conn.getresponse()

        message = response.read().decode()
        if response.status == 200:
            self.gcode.respond_info(f"{response.status} {response.reason}: {message}")
        else:
            raise self.gcode.error(f"{response.status} {response.reason}: {message}")


def load_config(config):
    return PrintEndNotify(config)
