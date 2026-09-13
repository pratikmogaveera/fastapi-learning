from datetime import datetime


def ts():
  return datetime.now().strftime("%H:%M:%S")
