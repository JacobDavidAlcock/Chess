import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color=(255, 255, 255)):
        self.base_rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.animation_scale = 1.0
        self.target_scale = 1.0

    def draw(self, surface):
        # Animate the scale
        if self.is_hovered:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0
        
        # Simple interpolation for smooth animation
        self.animation_scale += (self.target_scale - self.animation_scale) * 0.2

        # Calculate animated size and position
        width = self.base_rect.width * self.animation_scale
        height = self.base_rect.height * self.animation_scale
        animated_rect = pygame.Rect(
            self.base_rect.centerx - width / 2,
            self.base_rect.centery - height / 2,
            width,
            height
        )

        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, animated_rect, border_radius=12)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=animated_rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.base_rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                return True
        return False 