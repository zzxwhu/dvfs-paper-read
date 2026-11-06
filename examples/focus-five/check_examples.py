"""Offline checks for the five-paper reading guide. Python 3, standard library only."""
from math import isclose


def feasible_choice(rows, deadline_ms, correction=1.0):
    feasible = [(watts * latency * correction, name)
                for name, latency, watts in rows
                if latency * correction <= deadline_ms]
    return min(feasible)[1] if feasible else None


def main():
    # Published Table 3: (kHz, CRC32 microjoules).
    crc = [(131, 9.17), (262, 4.66), (524, 3.41), (1048, 2.95),
           (2097, 2.83), (4194, 2.95), (8000, 3.72), (16000, 4.61)]
    best = min(crc, key=lambda row: row[1])
    assert best == (2097, 2.83)
    print("STM32 Table 3: best kHz/uJ", best)

    # Published Tables VI/VII. Power ratio and a separate deadline distribution.
    power_saving = 100 * (1 - 1.84490 / 2.17700)
    any_late = 2.33 + 1.50 + 10.67
    assert round(power_saving, 2) == 15.25 and isclose(any_late, 14.50)
    print("DDQN: power saving %.2f%%, late %.2f%%" % (power_saving, any_late))

    # Published TinyLlama ShareGPT results: two distinct operating goals.
    print("FUSE G1: TPOT reduction %.2f%%" % (100 * (1 - 157.2 / 210.7)))
    print("FUSE G2: charge reduction %.2f%%" % (100 * (1 - 672.3 / 738.1)))

    # Teaching data, not measurements. Request correction must affect feasibility.
    actions = [("A", 45, 6), ("B", 36, 8)]
    assert feasible_choice(actions, 50) == "A"
    assert feasible_choice(actions, 50, 1.2) == "B"
    assert feasible_choice(actions, 30) is None
    print("DVFSLM toy: A -> B after bias correction; 30 ms infeasible")

    # Published decode cycles and mean CD. Distinct experiment boundaries.
    print("SCMI: decode %.2f us, original/optimized CD fractions %.2f%% / %.2f%%"
          % (263 / 20, 100 * 2.20 / 20, 100 * 0.77 / 20))


if __name__ == "__main__":
    main()
