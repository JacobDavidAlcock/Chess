import pygame

# Define the main menu function
def main_menu(screen, clock, width, height):
    background_colour = (255, 255, 255)
    menu_font = pygame.font.SysFont(None, 48)
    title_text = menu_font.render("Chess Game", True, (0, 0, 0))
    pvp_text = menu_font.render("Player vs Player", True, (0, 0, 0))
    pva_easy_text = menu_font.render("AI: Easy", True, (0, 0, 0))
    pva_hard_text = menu_font.render("AI: Hard", True, (0, 0, 0))
    exit_text = menu_font.render("Exit", True, (0, 0, 0))
    
    title_rect = title_text.get_rect(center=(width//2, height//6))
    pvp_rect = pvp_text.get_rect(center=(width//2, 2*height//6))
    pva_easy_rect = pva_easy_text.get_rect(center=(width//2, 3*height//6))
    pva_hard_rect = pva_hard_text.get_rect(center=(width//2, 4*height//6))
    exit_rect = exit_text.get_rect(center=(width//2, 5*height//6))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_rect.collidepoint(event.pos):
                    return "pvp"
                if pva_easy_rect.collidepoint(event.pos):
                    return "pva_easy"
                if pva_hard_rect.collidepoint(event.pos):
                    return "pva_hard"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
        
        screen.fill(background_colour)
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, background_colour, pvp_rect, 2)
        screen.blit(pvp_text, pvp_rect)
        pygame.draw.rect(screen, background_colour, pva_easy_rect, 2)
        screen.blit(pva_easy_text, pva_easy_rect)
        pygame.draw.rect(screen, background_colour, pva_hard_rect, 2)
        screen.blit(pva_hard_text, pva_hard_rect)
        pygame.draw.rect(screen, background_colour, exit_rect, 2)
        screen.blit(exit_text, exit_rect)
        
        pygame.display.update()
        clock.tick(60)