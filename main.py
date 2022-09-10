from operator import delitem
import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, ifft
import wave
import os


BYTES_IN_UINT8 = 1

def plot_fft(t: np.ndarray, x: list, sample_rate: int) -> None:
    plt.style.use('seaborn-poster')
    plt.figure(figsize = (8, 6))
    plt.plot(t, x, 'r')
    plt.ylabel('Amplitude')

    X = fft(x)
    N = len(X)
    n = np.arange(N)
    T = N/sample_rate
    freq = n/T 

    plt.figure(figsize = (12, 6))
    plt.subplot(121)

    plt.stem(freq, np.abs(X), 'b', \
            markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz)')
    plt.ylabel('FFT Amplitude |X(freq)|')
    plt.xlim(0, 8000)

    plt.subplot(122)
    plt.plot(t, ifft(X), 'r')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.xlim(0,2.5)
    plt.tight_layout()
    plt.show()

def main(cli_args: list) -> None:
    if len(cli_args) < 2:
        print("Two Arguments Required, [Input Filename, Data Type]")
        print("\tReceived:", cli_args)
        return
    else: #len(cli_args) < 2:
        filename = cli_args[1]
        data_type = cli_args[2]

    try:
        match data_type:
            case "int16":
                data = np.fromfile(filename, dtype=np.int16)
                sample_width = 2
            case "uint8":
                data = np.fromfile(filename, dtype=np.uint8) 
                sample_width = 1
            case "utf8":
                with open(filename, "r", encoding="utf8") as file:
                    data = file.readlines()
                data = [int(element) for element in data]
                sample_width = 1
            case "string":
                with open(filename, "r") as file:
                    lines = file.readlines()
                data = []
                for line in lines:
                    elements = line.split(',')
                    for element in elements:
                        data.append(element)
                sample_width = 1
                data = [int(i).to_bytes(1, 'little') for i in data]
            case _:
                print("Unrecognized Data Type:", data_type)
                print("\tOptions: uint8, utf8, string, int16")
                return
    except IOError:
        print(f"Error Opening File: '{filename}'")

    sample_rate = 8000 # sampling rate
    duration = len(data)/sample_rate # sampling interval
    ts = 1/sample_rate
    t = np.arange(0,duration,ts)

    # freq = 1.
    shifted_data = []
    for sample in data:
        if sample == 0:
            shifted_data.append(0)
        else:
            shifted_data.append(int(sample) - 128)

    if input("Plot Data? (Y/n): ") == 'Y':
        plot_fft(t, shifted_data, sample_rate)

    if input("Write to '.wav' file? (Y/n): ") == 'Y':
        wave_filename = os.path.splitext(filename)[0]+'.wav'   
        wave_obj = wave.open(wave_filename,'w')
        wave_obj.setnchannels(1) # mono
        wave_obj.setsampwidth(sample_width)
        wave_obj.setframerate(sample_rate)
        for sample in data:
            wave_obj.writeframesraw(sample)
        # wave_obj.close()

if __name__ == "__main__":
    main(sys.argv)
