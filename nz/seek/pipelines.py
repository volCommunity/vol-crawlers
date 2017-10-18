# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SeekDuplicatesPipeline(object):
    def process_item(self, item, spider):
        """
        Do something with our Data!
        :param item:
        :param spider:
        :return:
        """
        """
        # Does it already exist? If so: Raise
        """

        return item

class SeekDependeniesPipeline(object):
    def process_item(self, item, spider):
        """
        Do something with our Data!
        :param item:
        :param spider:
        :return:
        """
        """
        # Do we need to create label, set ids
        # Do we need to create site, set ids
        # Do we need to create org, set ids -TODO: can we spider the org from this pipeline?
        """

        return item


class SeekCreateJobPipeline(object):
    def process_item(self, item, spider):
        """
        Do something with our Data!
        :param item:
        :param spider:
        :return:
        """
        """
        # Create the fucking job already
        """

        return item
