from pathlib import Path
from pytube import YouTube
from colorama import init, Fore


# Easy way of getting a user's download directory (cross-platform)
DL_PATH = str(Path.home() / "Downloads/").replace("\\", "/")


def c_text(text: str, color: str) -> str:
    """
    Wraps text in a contained ansi colour/reset block for better code readability.

    :param text: The text to display
    :param color: The colour to use
    :return:
    """
    return f'{color}{text}{Fore.RESET}'


def c_menu(video_link: str, *options) -> str:
    """
    Displays a colourful menu and validates user selection.

    :param video_link: The video url.
    :param options: A list of dictionaries containing {'opt': str, 'colour': str, 'action': ["str", function]},

    :return: The first character of option or c for cancel
    """
    # build prompt
    prompt = []
    valid_choice = []
    for opt in list(options) + [{'opt': 'cancel', 'colour': Fore.RED, 'action': None}]:
        prompt.append(c_text(f"({opt['opt'][0]}){opt['opt'][1:]}", opt['colour']))
        valid_choice += opt['opt'][0]
    prompt = c_text("\ndownload: ", Fore.RED) + " | ".join(prompt) + ": "

    # get user choice
    pick = None
    while (pick is None) or (pick not in valid_choice):
        if pick is not None:
            print("  > Bad input. Try again.")
        pick = input(prompt).strip()

    # show action
    if pick != "c":
        pick_opt = options[valid_choice.index(pick)]
        print(f"\nDownloading", c_text(pick_opt['action'][0].upper(), pick_opt['colour']),
              "of", c_text(video_link, Fore.CYAN))
        pick_opt['action'][1]().download(DL_PATH)

    # return result
    return pick


def on_progress(stream, chunk, bytes_remaining):
    """
    Download progress event handler.

    :param stream: Remote file stream.
    :param chunk: Current data chunk.
    :param bytes_remaining: Bytes left to download.
    :return: None
    """
    progress = 100 - (bytes_remaining * 100 / stream.filesize)
    progress_text = ((round(progress * 20 / 100) * "#") + (20 * " "))[0:20]
    print(f'\r  > [{c_text(progress_text,  Fore.GREEN)}] {progress:.2f}%', end="")


def on_complete(stream, filepath):
    """
    Download completion event handler.

    :param stream: Remote file stream.
    :param filepath: Local file path.
    :return: None
    """
    print("\rdownload complete! ->", c_text(filepath.replace("\\", "/"), Fore.LIGHTBLUE_EX), "\n")


init()
link = input('Youtube link: ')
video_object = YouTube(link, on_complete_callback=on_complete, on_progress_callback=on_progress)

# information
print(f'{c_text("title:  ", Fore.RED)}{video_object.title}')
print(f'{c_text("length: ", Fore.RED)}{video_object.length / 60:.2f} minutes')
print(f'{c_text("views:  ", Fore.RED)}{video_object.views / 1,000,000} million')
print(f'{c_text("author: ", Fore.RED)}{video_object.author}')

# download
download_choice = c_menu(
    link,
    {'opt': "best", 'colour': Fore.GREEN, 'action': ["best quality", video_object.streams.get_highest_resolution]},
    {'opt': "worst", 'colour': Fore.YELLOW, 'action': ["lowest quality", video_object.streams.get_lowest_resolution]},
    {'opt': "audio", 'colour': Fore.BLUE, 'action': ["audio only", video_object.streams.get_audio_only]}
)
print(f"Bye...\n\n")
