import re
#import pandas as pd
import numpy as np
import subprocess
from functools import reduce

def obtenerDatos():

    hora = r'(?P<hora>\d+:\d+:\d+)\.\d+,'
    ipv4 = r'(?:\d{1,3}\.){3}\d{1,3}'
    ipv6 = r'(?:(?:\d[a-f]){0,2}:){5}(?:\d[a-f]){0,2}'
    ip_orig = r'(?P<ip_orig>(?:'+ipv4+'|'+ipv6+'))'
    ip_dest = r'(?P<ip_dest>(?:'+ipv4+'|'+ipv6+'))'
    puerto_orig = r'(?P<puerto_orig>\d+)'
    puerto_dest = r'(?P<puerto_orig>\d+)'
    length = r'length (?P<length>\d+)'



    arpRequest = re.compile(r' '.join([hora, r'(?P<protocolo>ARP, Request) who-has', ip_orig, r'tell', ip_dest, length]))
    arpReply = re.compile(r' '.join([hora, r'(?P<protocolo>ARP, Reply)', ip_orig, r'is-at', ip_dest, length]))

    #regex = re.compile(rb'(?P<hora>\d+:\d+:\d+)\.\d+ IP (?P<ip_orig>(?:\d{1,3}\.){3}\d{1,3})\.(?P<puerto_orig>\d+) > (?P<ip_dest>(?:\d{1,3}\.){3}\d{1,3})\.(?P<puerto_dest>\d+): (?P<protocolo>[^,]+), length (?P<length>\d+)')

    regexes = (arpRequest,
               arpReply)

    p = subprocess.Popen(['tcpdump', '-l', '-f', '-c', '10'], stdout=subprocess.PIPE)

    for line in p.stdout:
        matches = (r.search(line) for r in regexes)
        yield reduce(bool.__or__, matches)

def main():


    for match in obtenerDatos():
        print(match.groups())


    return

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