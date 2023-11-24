from .command import CommandProcessor


class Events:
    def __init__(
        self,
        keyboard_enabled,
        cross_cmd_enabled,
        pressing_timer_interval,
        d1_pressing_timer_interval,
        d2_pressing_timer_interval,
        command_key_mappings,
    ):
        self.keyboard_enabled = keyboard_enabled
        self.cross_cmd_enabled = cross_cmd_enabled
        self.command_key_mappings = command_key_mappings
        self.pressing_timer_interval = pressing_timer_interval
        self.d1_pressing_timer_interval = d1_pressing_timer_interval
        self.d2_pressing_timer_interval = d2_pressing_timer_interval

        self.cmd_process = CommandProcessor()

        # process cmd related to direction (left, right)
        self.d1_cmd_process = CommandProcessor()  # walk
        self.d2_cmd_process = CommandProcessor()  # face

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    # Toggle keyboard events if encounter cross hands command
    def check_cross_command(self, command):
        if self.cross_cmd_enabled and command == "cross":
            self.keyboard_enabled = not self.keyboard_enabled
            self.cmd_process.release_previous_key()
            self.d1_cmd_process.release_previous_key()
            self.d2_cmd_process.release_previous_key()

    # Add command to pipeline
    def add(self, command):
        self.check_cross_command(command)

        # Split command by type
        if "walk" in command or "d1" in command:
            self.d1_cmd_process.add_command(
                command,
                self.keyboard_enabled,
                self.command_key_mappings,
                self.d1_pressing_timer_interval,
            )
        elif "face" in command or "d2" in command:
            self.d2_cmd_process.add_command(
                command,
                self.keyboard_enabled,
                self.command_key_mappings,
                self.d2_pressing_timer_interval,
            )
        else:
            self.cmd_process.add_command(
                command,
                self.keyboard_enabled,
                self.command_key_mappings,
                self.pressing_timer_interval,
            )

    def __str__(self):
        return f"""
D1 ({len(self.d1_cmd_process.commands)}): {self.d1_cmd_process}

D2 ({len(self.d2_cmd_process.commands)}): {self.d2_cmd_process}

Events ({len(self.cmd_process.commands)}): {self.cmd_process}"""
