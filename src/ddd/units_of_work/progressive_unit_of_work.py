# -*- coding: utf-8 -*-
"""Progressive Unit of Work."""

# Standard Library Imports
from __future__ import annotations
from typing import Optional

# Third-Party Imports
from tqdm import tqdm

# Local Imports
from .base_unit_of_work import BaseUnitOfWork

__all__ = ["ProgressiveUnitOfWork"]


class ProgressiveUnitOfWork(BaseUnitOfWork):
    """Class implements a progressive unit of work.

    Args:
        *args (optional): Positional arguments.
        progress_bar (optional): Progress bar. Default ``None``.
        **kwargs (optional): Keyword arguments.

    Attributes:
        progress_bar: Progress bar.

    """

    def __init__(
        self,
        *args,
        progress_bar: Optional[tqdm] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._progress_bar = progress_bar or tqdm()

    def __enter__(self) -> ProgressiveUnitOfWork:
        self._progress_bar.reset()
        super().__enter__()
        return self

    def __exit__(self, *args) -> None:
        super().__exit__(*args)
        self._progress_bar.close()

    @property
    def progress(self) -> tqdm:
        """Progress bar."""
        return self._progress_bar
