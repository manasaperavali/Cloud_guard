class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def printf(text, color="green", size="large"):
    size_code = {
        'small': '\033[1m',
        'medium': '\033[2m',
        'large': '\033[3m',
        'x-large': '\033[4m',
    }.get(size, '')

    color_code = getattr(Color, color.upper(), '')
    
    formatted_text = f"{size_code}{color_code}{text}{Color.RESET}"
    
    print(formatted_text)

# Example Usage:
printf("Hello, World!", color='green', size='large')
printf("This is bold and red.", color='red', size='small')
printf("Underlined and blue.", color='blue', size='medium')
