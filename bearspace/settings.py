BOT_NAME = "bearspace"

SPIDER_MODULES = ["bearspace.spiders"]
NEWSPIDER_MODULE = "bearspace.spiders"
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    "bearspace.pipelines.save_dataframe.SaveInDataframe": 1,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
