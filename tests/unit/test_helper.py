from app.python.helper import getTimeRemaining
from time import time

# methods to test:
# getTimeRemaining (done)

# ---Get Time Remaining---
def test_helper_time_remaining():
    result = getTimeRemaining(int(time()) - 1800)
    assert result == 30