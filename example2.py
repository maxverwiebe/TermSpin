import random
import time
from termspin import ProgressBar, BarStyle

pb = ProgressBar(total=100, style=BarStyle.STRIPED, show_eta=True)
for _ in range(100):
    time.sleep(random.uniform(0.02, 1))
    pb.step()
pb.finish()
