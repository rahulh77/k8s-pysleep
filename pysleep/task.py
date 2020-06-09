import dataclasses


@dataclasses.dataclass
#@dataclasses.dataclass()                                       # alternative
class Task:
    task_name : str
    sleep_time : int = 0