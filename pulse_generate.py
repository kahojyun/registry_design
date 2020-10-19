import numpy as np

# def roundoff(x, roundto):
#     """Round x to given precision.
#     e.g. roundoff(3.141592653, 1e-3) = 3.142
#     """
#     return np.round(x / roundto) * roundto

def gen_drive_pulse(
    type, amp, width, plat, freq, 
    sample_rate,
    drag_scale=0, drag_detune=0,
):
    if type == 'cosine':
        n_pt_width = int(width * sample_rate)
        n_pt_edge = n_pt_width // 2
        fall_edge = 0.5 * (np.cos(np.pi * np.linspace(0, 1, n_pt_edge)) + 1)
        rise_edge = 1 - fall_edge

        n_pt_plat = int(plat * sample_rate)
        wf_plat = np.ones(n_pt_plat)

        wf_env = amp * np.hstack((rise_edge, wf_plat, fall_edge))

        n_periods = (width + plat) * freq
        n_pts = 2*n_pt_edge + n_pt_plat
        periods = np.linspace(0, n_periods, n_pts)
        osci_i = np.cos(2 * np.pi * periods)
        osci_q = np.sin(2 * np.pi * periods)

        return osci_i * wf_env, osci_q * wf_env
    else:
        raise Exception(f'Error: Type {type} is not supported.')

def gen_ro_pulse(
    type, freq, amp, duration, 
    sample_rate
):
    if type == 'square':
        n_pt = int(duration * sample_rate)
        wf_env = amp * np.ones(n_pt)

        n_periods = duration * freq
        periods = np.linspace(0, n_periods, n_pt)
        osci_i = np.cos(2 * np.pi * periods)
        osci_q = np.sin(2 * np.pi * periods)

        return osci_i * wf_env, osci_q * wf_env
    else:
        raise Exception(f'Error: Type {type} is not supported.')

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    print('-----Test generating drive pulse-----')
    wf_i, wf_q = gen_drive_pulse('cosine', amp=1, width=10e-9, plat=50e-9, freq=100e6, sample_rate=2e9)
    plt.plot(wf_i, label='Waveform I')
    plt.plot(wf_q, label='Waveform Q')
    ax = plt.gca()
    ax.set_title('Drive pulse')
    ax.set_xlabel('Sample point')
    ax.set_ylabel('Voltage')
    plt.show()

    print('-----Test generating readout pulse-----')
    wf_i, wf_q = gen_ro_pulse('square', freq=30e6, amp=0.5, duration=1e-6, sample_rate=2e9)
    plt.plot(wf_i, label='Waveform I')
    plt.plot(wf_q, label='Waveform Q')
    ax = plt.gca()
    ax.set_title('Readout pulse')
    ax.set_xlabel('Sample point')
    ax.set_ylabel('Voltage')
    plt.show()