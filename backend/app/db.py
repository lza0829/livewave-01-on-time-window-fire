import os
import sqlite3
from pathlib import Path

数据目录 = Path(os.environ.get("数据目录", Path(__file__).resolve().parent.parent / "data"))
夹具目录 = Path(os.environ.get("夹具目录", Path(__file__).resolve().parent.parent.parent / "fixtures"))
库路径 = 数据目录 / "播浪.db"


def 连接() -> sqlite3.Connection:
    数据目录.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(库路径, timeout=5.0)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    # 关窗事务与事件入流并发交错时，让写锁等待而不是立刻 OperationalError；配合写闸仍只可能有一单提交胜出
    c.execute("PRAGMA busy_timeout = 5000")
    c.execute("PRAGMA journal_mode = WAL")
    return c
