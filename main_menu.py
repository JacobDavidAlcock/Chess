import pygame

# Define the main menu function
def main_menu(screen, clock, width, height):
    background_colour = (255, 255, 255)
    menu_font = pygame.font.SysFont(None, 48)
    title_text = menu_font.render("Chess Game", True, (0, 0, 0))
    play_text = menu_font.render("Play", True, (0, 0, 0))
    exit_text = menu_font.render("Exit", True, (0, 0, 0))
    
    title_rect = title_text.get_rect(center=(width//2, height//4))
    play_rect = play_text.get_rect(center=(width//2, height//2))
    exit_rect = exit_text.get_rect(center=(width//2, 3*height//4))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return "play"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
        
        screen.fill(background_colour)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, background_colour, play_rect, 2)
        screen.blit(play_text, play_rect)
        pygame.draw.rect(screen, background_colour, exit_rect, 2)
        screen.blit(exit_text, exit_rect)
        
        pygame.display.update()
        clock.tick(60)