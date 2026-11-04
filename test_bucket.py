import pytest
import logging
from main_reviewed import BucketBuilder, BucketBuilderException, process_bucket

class TestBucketBuilder:
    def test_bucket_is_empty_when_instantiated(self):
        bucket = BucketBuilder()
        assert bucket.bucket == []

    def test_bucket_can_add_item(self):
        bucket = BucketBuilder()

        for item in range(10):
            bucket.add_item(item)

        assert bucket.bucket == list(range(10))

    def test_bucket_can_add_only_int_item(self):
        bucket = BucketBuilder()

        item = 1.0
        with pytest.raises(BucketBuilderException, match=f"add_item needs item as int. given item={item}"):
            bucket.add_item(item)

        assert bucket.bucket == []

    def test_bucket_can_remove_item(self):
        bucket = BucketBuilder()

        for item in range(10):
            bucket.add_item(item)
            bucket.remove_item(item)

        assert bucket.bucket == []

    def test_bucket_can_remove_only_int_item(self):
        bucket = BucketBuilder()

        item_to_remove=1.0
        bucket.add_item(1)

        with pytest.raises(BucketBuilderException, match=f"remove_item needs item as int. given item={item_to_remove}"):
            bucket.remove_item(item_to_remove)

        assert bucket.bucket == [1]

    def test_bucket_remove_item_does_not_raise_error_if_item_not_in_bucket(self):
        bucket = BucketBuilder()
        bucket.bucket == []

        for i in range(10):
            bucket.remove_item(i)

class TestProcessBucket:
    def test_process_bucket_adds_items(self):
        bucket = BucketBuilder()
        bucket_contents = process_bucket(bucket, is_add_operation=True)

        assert bucket_contents == list(range(10))

    def test_process_bucket_removes_items(self):
        bucket = BucketBuilder()
        bucket_contents = process_bucket(bucket, is_add_operation=True)

        for item in list(bucket_contents):
            process_bucket(bucket, item, is_add_operation=False)

        assert bucket.bucket == []

    def test_process_bucket_add_item_has_log_debug(self, caplog):
        caplog.set_level(logging.DEBUG)

        bucket = BucketBuilder()
        bucket_contents = process_bucket(bucket, is_add_operation=True)

        assert "Adding" in caplog.messages[-1]

    def test_process_bucket_remove_item_has_log_debug(self, caplog):
        caplog.set_level(logging.DEBUG)

        bucket = BucketBuilder()
        bucket_contents = process_bucket(bucket, is_add_operation=True)


        for item in list(bucket_contents):
            process_bucket(bucket, item, is_add_operation=False)

        assert "Removing" in caplog.messages[-1]
