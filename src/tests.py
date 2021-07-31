import uuid
import json
from typing import List

from dataclasses import dataclass, asdict, field
from .application import config

@dataclass
class Test:

    input: List[str]
    output: List[str]


@dataclass
class TestSet:

    tests: List[Test]
    id: str = field(default_factory=lambda: str(uuid.uuid1()))


def save_testset(ts: TestSet):
    testsets_dir = config.get().TESTSETS_DIR
    if not testsets_dir.exists():
        testsets_dir.mkdir(parent=True)
    testset_path = testsets_dir / ts.id
    with testset_path.open("w") as f:
        f.write(json.dumps(asdict(ts)))


class TestDoesNotExist(Exception):
    pass


def get_testset(id: str) -> TestSet:
    testset_path = config.get().TESTSETS_DIR / id
    if not testset_path.exists():
        raise TestDoesNotExist
    with testset_path.open("r") as f:
        return TestSet(**json.load(f))