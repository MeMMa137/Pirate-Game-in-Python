class NPC(AnimatedSprite):
    def __init__(self, pos, frames, groups, dialog, data, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):
        super().__init__(pos, frames, groups, z, animation_speed)
        self.dialog = dialog
        self.data = data
        self.current_dialog_index = 0
        self.interacting = False

    def interact(self):
        if self.current_dialog_index < len(self.dialog):
            self.data.ui.show_dialog(self.dialog[self.current_dialog_index])
            self.current_dialog_index += 1
        else:
            self.data.ui.hide_dialog()
            self.interacting = False
            self.current_dialog_index = 0

    def update(self, dt):
        self.animate(dt)
        if self.rect.colliderect(self.data.player.rect):
            if not self.interacting:
                self.interacting = True
                self.interact()

class QuestNPC(NPC):
    def __init__(self, pos, frames, groups, dialog, quest_data, data, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):
        super().__init__(pos, frames, groups, dialog, data, z, animation_speed)
        self.quest_data = quest_data
        self.quest_given = False

    def give_quest(self):
        self.data.quests.append(self.quest_data)
        self.quest_given = True
        self.data.ui.show_quest(self.quest_data)

    def interact(self):
        if not self.quest_given:
            self.give_quest()
        super().interact()

class MerchantNPC(NPC):
    def __init__(self, pos, frames, groups, dialog, inventory, data, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):
        super().__init__(pos, frames, groups, dialog, data, z, animation_speed)
        self.inventory = inventory

    def interact(self):
        self.data.ui.show_inventory(self.inventory)
        super().interact()

class TrainerNPC(NPC):
    def __init__(self, pos, frames, groups, dialog, training_data, data, z=Z_LAYERS['main'], animation_speed=ANIMATION_SPEED):
        super().__init__(pos, frames, groups, dialog, data, z, animation_speed)
        self.training_data = training_data

    def train_player(self):
        for attribute, value in self.training_data.items():
            setattr(self.data.player, attribute, getattr(self.data.player, attribute) + value)
        self.data.ui.show_training(self.training_data)

    def interact(self):
        self.train_player()
        super().interact()
