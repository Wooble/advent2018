import collections
import dataclasses

TEST_DATA = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".splitlines()


@dataclasses.dataclass
class Guard:
    total_sleep: int = 0
    hours_slept: collections.Counter = dataclasses.field(
        default_factory=collections.Counter
    )


def make_guards(data):
    guards = collections.defaultdict(Guard)
    current_guard = None
    data_iter = iter(data)
    for line in data_iter:
        if "Guard #" in line:
            current_guard = int(line.partition("Guard #")[2].split()[0])
            continue
        assert "falls asleep" in line
        start_time = int(line.partition(":")[2][:2])
        line2 = next(data_iter)
        assert "wakes up" in line2
        end_time = int(line2.partition(":")[2][:2])
        guard = guards[current_guard]
        for t in range(start_time, end_time):
            guard.total_sleep += 1
            guard.hours_slept[t] += 1
    return guards


def most_freq(data):
    guards = make_guards(data)
    chosen_guard = max(
        guards.items(), key=lambda item: item[1].hours_slept.most_common(1)[0][1]
    )
    return chosen_guard[0] * chosen_guard[1].hours_slept.most_common(1)[0][0]


def findtime(data):
    guards = make_guards(data)
    chosen_guard = max(guards.items(), key=lambda item: item[1].total_sleep)
    return chosen_guard[0] * chosen_guard[1].hours_slept.most_common(1)[0][0]


def test_findtime():
    assert findtime(TEST_DATA) == 240


def test_most_freq():
    assert most_freq(TEST_DATA) == 4455


if __name__ == "__main__":
    with open("04_input.txt") as f:
        print(findtime(sorted(f)))
        f.seek(0)
        print(most_freq(sorted(f)))
