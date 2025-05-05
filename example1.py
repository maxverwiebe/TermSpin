import time
from termspin import Spinner, SpinnerStyle

with Spinner(text="Thinking", theme=SpinnerStyle.WAVE, color="\033[96m"):
        time.sleep(2)
    