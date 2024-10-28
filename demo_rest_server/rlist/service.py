#!/usr/bin/env python3

from typing import List


class ListService:
    def __init__(self) -> None:
        self._storage_ = []

    @property
    def items(self) -> List[str]:
        return self._storage_

    def add(self, item: str) -> None:
        if not isinstance(item, str):
            raise ValueError(item)
        self._storage_.append(item)

    def remove(self, item: str) -> None:
        if not isinstance(item, str):
            raise ValueError(item)
        self._storage_.remove(item)
