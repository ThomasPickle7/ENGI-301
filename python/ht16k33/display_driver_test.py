import ht16k33 as display

if __name__ == '__main__':
    sev_seg = display.HT16K33(1, 0x70)
    import time
    sev_seg.text("bruh")

