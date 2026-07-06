from sortedcontainers import SortedDict
from typing import List, Dict, Tuple, Set
import bisect
import heapq

class MetricStorageEngine:
    def __init__(self, threshold_size: int = 10):
        self.threshold_size = threshold_size
        self.mem_table: Dict[Tuple[str, int], float] = SortedDict()
        self.ss_table: List[List[Tuple[str, int, float]]] = []

    def write(self, metric_name: str, timestamp: int, value: int):
        self.mem_table[(metric_name, timestamp)] = value

        if len(self.mem_table) >= self.threshold_size:
            self.flush()

    def read_range(self, metric_name: str, start_time: int, end_time: int) -> List[Tuple[int, float]]:
        mem_result = []
        mem_keys = self.mem_table.keys()
        start_index = mem_keys.bisect_left((metric_name, start_time))
        end_index = mem_keys.bisect_right((metric_name, end_time))
        for key in mem_keys[start_index:end_index]:
            if key[0] == metric_name:
                mem_result.append((key[1], self.mem_table[key]))

        ss_table_result = []
        for index in range(len(self.ss_table) - 1, -1, -1):
            ss_table = self.ss_table[index]
            start_index = bisect.bisect_left(ss_table, (metric_name, start_time, float('-inf')))
            end_index = bisect.bisect_right(ss_table, (metric_name, end_time, float('inf')))
            for entry in ss_table[start_index:end_index]:
                if entry[0] == metric_name:
                    ss_table_result.append((entry[1], entry[2]))

        merged_result = {}
        seen_timestamps: Set[int] = set()
        for timestamp, value in mem_result:
            seen_timestamps.add(timestamp)
            if value is not None:
                merged_result[timestamp] = value

        for timestamp, value in ss_table_result:
            if timestamp not in seen_timestamps:
                seen_timestamps.add(timestamp)
                if value is not None:
                    merged_result[timestamp] = value

        return sorted(merged_result.items(), key=lambda x: x[0])
        
    def read_latest(self, metric_name: str) -> Tuple[int, float]:
        candidates = []
        seen_timestamps: Set[int] = set()

        index = self.mem_table.bisect_right((metric_name, float('inf')))
        if index > 0:
            key, value = self.mem_table.peekitem(index - 1)
            if key[0] == metric_name:
                seen_timestamps.add(key[1])
                if value is not None:
                    candidates.append((key[1], value))
            
        
        for index in range(len(self.ss_table) - 1, -1, -1):
            ss_table = self.ss_table[index]
            start_index = bisect.bisect_right(ss_table, (metric_name, float('inf'), float('inf')))
            if start_index > 0:
                entry = ss_table[start_index - 1]
                if entry[0] == metric_name:
                    if entry[1] not in seen_timestamps:
                        seen_timestamps.add(entry[1])
                        if entry[2] is not None:
                            candidates.append((entry[1], entry[2]))

        return max(candidates, key=lambda x: x[0]) if candidates else None
        
    def delete(self, metric_name: str, timestamp: int):
        self.mem_table[(metric_name, timestamp)] = None

        if len(self.mem_table) >= self.threshold_size:
            self.flush()

    def flush(self):
        sorted_entries = [(key[0], key[1], value) for key, value in self.mem_table.items()]
        self.ss_table.append(list(sorted_entries))
        self.mem_table.clear()

    def compact(self):
        if not self.ss_table:
            return

        heap_entries = []
        for index in range(len(self.ss_table)):
            ss_table = self.ss_table[index]
            if ss_table:
                heapq.heappush(heap_entries, (ss_table[0][0], ss_table[0][1], -index, 0))

        merged_entries = {}
        seen_entries = set()

        while heap_entries:
            metric_name, timestamp, ss_index, entry_index = heapq.heappop(heap_entries)
            value = self.ss_table[-ss_index][entry_index][2]

            if (metric_name, timestamp) not in seen_entries:
                seen_entries.add((metric_name, timestamp))
                if value is not None:
                    merged_entries[(metric_name, timestamp)] = value

            if entry_index + 1 < len(self.ss_table[-ss_index]):
                next_entry = self.ss_table[-ss_index][entry_index + 1]
                heapq.heappush(heap_entries, (next_entry[0], next_entry[1], ss_index, entry_index + 1))

        merged_result = sorted(
            (metric, ts, value)
            for (metric, ts), value in merged_entries.items()
        )
        self.ss_table = [merged_result]
          