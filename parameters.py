import ctypes
user32 = ctypes.windll.user32
monitor = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

title = "8 марта: Поле Чудес"
size = width, height = monitor[0] // 2, monitor[1] // 2
fullscreen = False
fps = 60

