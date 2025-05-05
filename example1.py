import time
from termspin import Spinner, SpinnerStyle

with Spinner(text="Thinking", theme=SpinnerStyle.DOTS, color="\033[96m"):
        time.sleep(2)
    