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

class PromotionDialog:
    def __init__(self, x, y, color, font):
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.selected_piece = None
        
        # Dialog dimensions
        self.width = 320
        self.height = 180
        
        # Create buttons for each piece type
        button_width = 60
        button_height = 60
        button_spacing = 10
        start_x = x + (self.width - (4 * button_width + 3 * button_spacing)) // 2
        start_y = y + 90
        
        self.buttons = {
            'queen': Button(start_x, start_y, button_width, button_height, "Q", font, (180, 140, 70), (220, 180, 110)),
            'rook': Button(start_x + button_width + button_spacing, start_y, button_width, button_height, "R", font, (180, 140, 70), (220, 180, 110)),
            'bishop': Button(start_x + 2 * (button_width + button_spacing), start_y, button_width, button_height, "B", font, (180, 140, 70), (220, 180, 110)),
            'knight': Button(start_x + 3 * (button_width + button_spacing), start_y, button_width, button_height, "N", font, (180, 140, 70), (220, 180, 110))
        }
        
    def draw(self, surface):
        # Draw semi-transparent background
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw dialog box
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (50, 50, 50), dialog_rect, border_radius=15)
        pygame.draw.rect(surface, (200, 200, 200), dialog_rect, width=3, border_radius=15)
        
        # Draw title
        title_text = self.font.render("Choose Promotion Piece", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.x + self.width // 2, self.y + 40))
        surface.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.buttons.values():
            button.draw(surface)
    
    def handle_event(self, event):
        for piece_type, button in self.buttons.items():
            if button.handle_event(event):
                self.selected_piece = piece_type
                return piece_type
        return None 