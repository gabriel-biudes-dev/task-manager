from dashing import HSplit, VSplit, VGauge
from psutil import virtual_memory

ui = HSplit(
    VSplit(
        VGauge(title = 'RAM'),
        title = 'Memory',
        border_color = 3
    )
)

while True:
    mem_tui = ui.items[0]
    ram_tui = mem_tui.items[0]
    ram_tui.value = virtual_memory().percent
    ram_tui.title = "Porcentagem"
    try:
        ui.display()
    except KeyboardInterrupt:
        break
