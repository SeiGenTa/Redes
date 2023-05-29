from bwcgbn import main

name = "data.csv"

try:
    arch = open(name,"x")
    arch.write(f"Tamaño;tiempo (ms);loss;win_size;Tamaño en bytes;tiempo tardado;bw \n")
except:
    arch = open(name,"a")

for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 5
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 10
    loss = 5
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 30
    loss = 5
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 10
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 15
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 20
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 5
    win_size = 5
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 10
    win_size = 10
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 5
    win_size = 15
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 5
    win_size = 20
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")
        
for i in range(5):
    size = 1000 * i + 4000
    timeout = 20
    loss = 5
    win_size = 25
    for i in range(3):
        data = main(size, timeout, loss, win_size, "/etc/services", "anakena.dcc.uchile.cl", 1819)
        arch.write(f"{size};{timeout};{loss};{win_size};{data[0]};{data[1]};{data[2]} \n")

arch.close()
