import time
from datetime import datetime
from multiprocessing import Pool, cpu_count
from flask import jsonify
from python.util.common import get_logger
import os

logger = get_logger()



def compute_partial(start, end):
    pid = os.getpid()

    logger.info(f"[PID {pid}] 計算區段開始: {start} ~ {end - 1}")

    segment_start_time = time.time()

    partial_total = 0
    for i in range(start, end):
        partial_total += (i % 5) * (i % 3)

    segment_end_time = time.time()
    elapsed = round(segment_end_time - segment_start_time, 4)

    logger.info(
        f"[PID {pid}] 區段完成，結果: {partial_total}，耗時: {elapsed} 秒"
    )

    return partial_total

def bench_cpu_result(count=10000000):
    logger.info(f"🧪 開始 CPU 測試任務，總計算量：{count}")

    start_time = datetime.utcnow().isoformat() + "Z"
    start = time.time()

    num_processes = cpu_count()
    logger.info(f"🧠 系統偵測可用 CPU 核心數：{num_processes}")

    chunk_size = count // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]

    if count % num_processes != 0:
        ranges[-1] = (ranges[-1][0], count)
    logger.debug(f"📊 分配計算區段範圍：{ranges}")

    logger.info("🚀 啟動 multiprocessing 計算")
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(compute_partial, ranges)

    total = sum(results)
    logger.info(f"✅ 計算完成，結果 total={total}")

    end = time.time()
    end_time = datetime.utcnow().isoformat() + "Z"
    elapsed = round(end - start, 4)

    logger.info(f"⌛ CPU 計算耗時：{elapsed} 秒")

    return jsonify({
        "total": total,
        "time_sec": elapsed,
        "cpu_count": num_processes,
        "start_time": start_time,
        "end_time": end_time
    })