class Text:

    def __init__(self, pos, text, font):
        self.pos = pos
        self.text = text
        self.font = font

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.pos)

    def draw(self, surface):
        surface.blit(self.text_surface, self.text_rect)
