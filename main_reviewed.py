"""
Example output with logging.DEBUG

2026-11-04 15:43:57:    INFO: [__main__]: Hello, world
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 0 to []
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 1 to [0]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 2 to [0, 1]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 3 to [0, 1, 2]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 4 to [0, 1, 2, 3]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 5 to [0, 1, 2, 3, 4]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 6 to [0, 1, 2, 3, 4, 5]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 7 to [0, 1, 2, 3, 4, 5, 6]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 8 to [0, 1, 2, 3, 4, 5, 6, 7]
2026-11-04 15:43:57:   DEBUG: [__main__]: Adding 9 to [0, 1, 2, 3, 4, 5, 6, 7, 8]
2026-11-04 15:43:57:    INFO: [__main__]: bucket_content=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
2026-11-04 15:43:57:    INFO: [__main__]: ----------
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 0 from [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 1 from [1, 2, 3, 4, 5, 6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 2 from [2, 3, 4, 5, 6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 3 from [3, 4, 5, 6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 4 from [4, 5, 6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 5 from [5, 6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 6 from [6, 7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 7 from [7, 8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 8 from [8, 9]
2026-11-04 15:43:57:   DEBUG: [__main__]: Removing 9 from [9]
2026-11-04 15:43:57:    INFO: [__main__]: bucket_content=[]
2026-11-04 15:43:57:    INFO: [__main__]: Goodbye, world :')
"""

from typing import List
import logging

logger = logging.getLogger(__name__)

class BucketBuilderException(Exception):
    pass

class BucketBuilder:
    def __init__(self):
        self.bucket = []

    def add_item(self, item: int) -> List:
        """
        Add item to bucket.
        Returns bucket contents as list
        Args:
            item (int): Item to add
        Returns:
            list
        """
        if not isinstance(item, int):
            raise BucketBuilderException(f"add_item needs item as int. given {item=}")

        self.bucket.append(item)
        return self.bucket

    def remove_item(self, item: int) -> List:
        """
        Remove item from bucket
        If item exists in bucket, will remove first occurence and return bucket
        If item does not exist in bucket, will return bucket
        Args:
            item (int): Item to remove
        Returns:
            list
        """
        if not isinstance(item, int):
            raise BucketBuilderException(f"remove_item needs item as int. given {item=}")

        if item in self.bucket:
            self.bucket.remove(item) # Remove item from the bucket

        return self.bucket

def process_bucket(bucket=None, item:int|None=None, is_add_operation=True) -> List:
    """
    Process bucket and return its contents
    Args:
        bucket (BucketBuilder): bucket to be processed
        item (int or None): used to remove first occurence from bucket
        is_add_operation (bool): True if add operation
    """

    if is_add_operation:
        # Generate values with for only when adding items to bucket
        for i in range(10):
            logger.debug(f"Adding {i} to {bucket.bucket}")
            bucket.add_item(i)

    elif item is not None and isinstance(item, int):
        logger.debug(f"Removing {item} from {bucket.bucket}")
        bucket.remove_item(item)

    return bucket.bucket # Return the final accumulated bucket contents


if __name__ == '__main__':
    logging.basicConfig(
        filename=None,
        level=logging.DEBUG, # Change loglevel to logging.DEBUG
        format='%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger.info("Hello, world") # greet user

    bucket = BucketBuilder()
    bucket_contents = process_bucket(bucket, is_add_operation=True)
    logger.info(f"{bucket_contents=}")
    logger.info("-"*10)

    # avoid mutation by creating a new list with the same contents
    for item in list(bucket_contents):
        # always save last state in bucket_contents
        bucket_contents = process_bucket(bucket, item, is_add_operation=False)

    logger.info(f"{bucket_contents=}")
    logger.info("Goodbye, world :')") # We need to ungreet the user
