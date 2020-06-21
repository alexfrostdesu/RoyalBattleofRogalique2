class SkillCooldown:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.current_cooldown = 0

    def check_cooldown(self):
        if self.current_cooldown == 0:
            self.current_cooldown = self.cooldown
            return True
        else:
            self.current_cooldown -= 1
            return False

    def set_cooldown(self, cooldown):
        self.current_cooldown = cooldown
