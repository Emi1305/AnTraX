import re
import pandas as pd
import numpy as np
import subprocess

def main():
    regex = re.compile(rb'(?P<hora>\d+:\d+:\d+)\.\d+ IP (?P<ip_orig>(?:\d{1,3}\.){3}\d{1,3})\.(?P<puerto_orig>\d+) > (?P<ip_dest>(?:\d{1,3}\.){3}\d{1,3})\.(?P<puerto_dest>\d+): (?P<protocolo>[^,]+), length (?P<length>\d+)')

    p = subprocess.Popen(['tcpdump', '-f', '-c', '10'], stdout=subprocess.PIPE)

    p.wait()
    lines = [line for line in p.stdout]
    print(lines)
    matches = [regex.search(line) for line in lines]

    indices = (np.array([m.group('ip_orig') for m in matches if m]),
               np.array([m.group('puerto_orig') for m in matches if m]),
               np.array([m.group('ip_dest') for m in matches if m]),
               np.array([m.group('puerto_dest') for m in matches if m]))

    columnas = ('Hora', 'IP Origen', 'Puerto Origen', 'IP Destino', 'Puerto Destino', 'Protocolo', 'Tamaño')

    datos = np.array([m.group('protocolo') for m in matches if m], [m.group('length') for m in matches if m])

    df = pd.DataFrame(datos, index=indices, columns=columnas)

    print(df)
    input('Presione cualquier tecla para salir.')


if __name__ == '__main__':
    main()