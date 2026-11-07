"""Five DVFS method demonstrations; Python 3, standard library only.

Run: python method_walkthrough.py
No drivers are written, no frequencies are changed, and no neural model is trained.
Published CRC32 table values are identified below. All other environments and
Q scores are teaching data, not measurements or author-code reproductions.
"""
from dataclasses import dataclass
from math import ceil, isclose
from random import Random
import json


def crc32_choice(deadline_ms, overhead_ms=0.2):
    # Paper Tables 1 and 3; time in ms, energy in microjoules.
    # Overhead is a teaching assumption; switching energy is omitted.
    rows = [(0.131, 85.34, 9.17), (0.262, 29.67, 4.66),
            (0.524, 12.88, 3.41), (1.048, 6.04, 2.95),
            (2.097, 2.93, 2.83), (4.194, 1.44, 2.95),
            (8.000, 0.75, 3.72), (16.000, 0.37, 4.61)]
    candidates = [r for r in rows if r[1] + overhead_ms <= deadline_ms]
    return min(candidates, key=lambda r: r[2]) if candidates else None


def tem_update(residency_ms, labels, frequency_index, max_util,
               avg_util, elapsed_ms, busy_ms, delta_ms):
    """A teaching 2-frequency x 2-load-bin encoding; not author tensor config."""
    assert 0 <= max_util <= 1 and 0 <= avg_util <= 1
    load_bin = int(max_util >= 0.6)
    result = [row[:] for row in residency_ms]
    for index, label in enumerate(labels):
        if label == 1:
            result[index][frequency_index * 2 + load_bin] += delta_ms
    return result, elapsed_ms + delta_ms, busy_ms + delta_ms * avg_util


def double_q_target(reward, terminal, gamma, online_next, target_next):
    """Standard DDQN target illustration; network values are supplied, not learned."""
    if terminal:
        return reward
    next_action = max(range(len(online_next)), key=online_next.__getitem__)
    return reward + gamma * target_next[next_action]


def fuse_g1(gpu_scan, cpu_profiles, budget_mj):
    """Teaching G1 boundary search. Rows are ordered high frequency first.

    gpu_scan: (GPU_name, latency_ms, energy_mJ)
    cpu_profiles[GPU]: (CPU_name, latency_ms, energy_mJ)
    Returns the chosen row or None. Curve assumptions must be checked separately.
    """
    previous = None
    gpu_candidates = []
    for gpu, latency, energy in gpu_scan:
        if energy <= budget_mj:
            gpu_candidates = [gpu] + ([previous] if previous else [])
            break
        previous = gpu
    feasible = []
    for gpu in gpu_candidates:
        for cpu, latency, energy in cpu_profiles[gpu]:
            if energy <= budget_mj:
                feasible.append((gpu, cpu, latency, energy))
                break
    return min(feasible, key=lambda r: r[2]) if feasible else None


@dataclass(frozen=True)
class Point:
    gpu_index: int
    emc_index: int
    ms: float
    watts: float

    def energy_mj(self, alpha):
        return self.ms * alpha * self.watts


def enumerate_points(strips, deadline_ms, alpha):
    feasible = [p for strip in strips for p in strip if p.ms * alpha <= deadline_ms]
    return min(feasible, key=lambda p: p.energy_mj(alpha)) if feasible else None


def pruned_points(strips, deadline_ms, alpha):
    """Algorithm-1-style pruning only for positive, monotone estimated curves.

    Each strip must be sorted by ascending GPU frequency. Returns whether full
    enumeration was used to preserve correctness when assumptions do not hold.
    """
    assert alpha > 0
    for strip in strips:
        if any(p.ms <= 0 or p.watts <= 0 for p in strip):
            raise ValueError('invalid estimator output')
        monotone = all(a.ms >= b.ms and a.watts <= b.watts
                       for a, b in zip(strip, strip[1:]))
        if not monotone:
            return enumerate_points(strips, deadline_ms, alpha), True
    best = None
    best_energy = float('inf')
    for strip in strips:
        t_min = strip[-1].ms * alpha
        lower_bound = strip[0].watts * t_min
        if t_min > deadline_ms or lower_bound >= best_energy:
            continue
        for point in strip:
            t = point.ms * alpha
            if t > deadline_ms:
                continue
            if point.watts * t_min >= best_energy:
                break
            if point.energy_mj(alpha) < best_energy:
                best, best_energy = point, point.energy_mj(alpha)
    return best, False


def adaptation(measured_ms, base_predictions_ms):
    assert len(measured_ms) == len(base_predictions_ms) > 0
    if sum(base_predictions_ms) <= 0:
        raise ValueError('nonpositive prediction denominator')
    return sum(measured_ms) / sum(base_predictions_ms)


def hlc_frequency(max_frequency, compute_share, memory_share, beta):
    # beta is total allowed runtime multiplier; beta=1.1 means +10%.
    assert beta >= 1 and compute_share > 0 and memory_share >= 0
    return max_frequency * compute_share / (
        memory_share * (beta - 1) + compute_share * beta)


def timing_demo(event_driven, fast_down, direction):
    """Discrete-event timing example in ms, NOT the paper's HIL measurements.

    Phase change at 0.21, HLC tick 1.0, mailbox+decode 0.1,
    LLC tick 0.5, application one further LLC tick later.
    Fast-down delay 0.02 is a teaching parameter.
    """
    phase = 0.21
    request = phase if event_driven else ceil(phase / 1.0) * 1.0
    decoded = request + 0.1
    if fast_down and direction == 'down':
        applied = decoded + 0.02
    else:
        applied = ceil(decoded / 0.5) * 0.5 + 0.5
    return dict(phase_ms=phase, request_ms=request, decoded_ms=decoded,
                applied_ms=applied, control_delay_ms=round(applied-phase, 6))


def main():
    assert crc32_choice(3)[0] == 4.194
    assert crc32_choice(4)[0] == 2.097
    assert crc32_choice(0.5) is None
    print('CRC32: 3ms -> 4.194MHz; 4ms -> 2.097MHz; 0.5ms -> infeasible')

    p, elapsed, busy = tem_update([[0.0]*4 for _ in range(3)],
                                  [2, 1, 0], 0, 0.8, 0.5, 100, 60, 10)
    assert p == [[0.0]*4, [0.0, 10.0, 0.0, 0.0], [0.0]*4]
    assert elapsed == 110 and busy == 65
    target = double_q_target(0, False, 0.9, [0.6, 0.8], [0.9, 0.7])
    assert isclose(target, 0.63)
    assert double_q_target(0.7, True, 0.9, [0.6, 0.8], [0.9, 0.7]) == 0.7
    print('TEM: task 2 low-frequency/high-load bin +10ms; busy +5ms')
    print('DDQN: online selects H, target evaluates H=0.7; Bellman target=0.63')

    fuse = fuse_g1([('H',30,330), ('M',40,280), ('L',60,310)],
                   {'H':[('high',30,330),('mid',32,295)],
                    'M':[('high',40,280),('mid',44,260)]}, 300)
    assert fuse == ('H', 'mid', 32, 295)
    print('FUSE G1: retain H and M; CPU refinement chooses H/mid,32ms,295mJ')

    actions = [[Point(0,0,45,6), Point(1,0,36,8), Point(2,0,31,11)]]
    assert pruned_points(actions,50,1)[0].gpu_index == 0
    assert pruned_points(actions,50,1.2)[0].gpu_index == 1
    assert pruned_points(actions,30,1.2)[0] is None
    assert isclose(adaptation([60,60],[50,50]),1.2)
    rng = Random(902)
    for _ in range(200):
        strips = []
        for emc in range(4):
            times = sorted([rng.uniform(5,100) for _ in range(11)], reverse=True)
            powers = sorted([rng.uniform(1,20) for _ in range(11)])
            strips.append([Point(i,emc,t,p) for i,(t,p) in enumerate(zip(times,powers))])
        deadline, alpha = rng.uniform(1,120), rng.uniform(0.7,1.5)
        full = enumerate_points(strips,deadline,alpha)
        pruned, fallback = pruned_points(strips,deadline,alpha)
        assert not fallback and full == pruned
    nonmonotone = [[Point(0,0,45,6),Point(1,0,50,5),Point(2,0,31,11)]]
    assert pruned_points(nonmonotone,60,1)[1]
    print('DVFSLM: bias changes A -> B; impossible deadline detected;')
    print('200 synthetic monotone grids match exhaustive search; invalid shape falls back')

    assert isclose(hlc_frequency(3.4,0.3,0.7,1.1),2.55)
    timing = {name:timing_demo(event,fast,'down') for name,event,fast in
              [('periodic',False,False),('event',True,False),('event_fast',True,True)]}
    assert isclose(timing['periodic']['control_delay_ms'],1.79)
    assert isclose(timing['event']['control_delay_ms'],0.79)
    assert isclose(timing['event_fast']['control_delay_ms'],0.12)
    assert timing_demo(True,True,'up') == timing_demo(True,False,'up')
    print('HLC: 30% compute,70% memory,beta=1.1 -> 2.55GHz from 3.4GHz')
    print('SCMI toy event times (not measured paper results):')
    print(json.dumps(timing,indent=2))


if __name__ == '__main__':
    main()
