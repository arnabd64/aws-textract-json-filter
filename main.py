from textract_fetch import Fetcher
from block_filter import Blocks


def main(job_id: str):
    # fetch the data
    fetcher = Fetcher(job_id)
    if not fetcher.wait():
        return None

    # download the entire data
    _blocks = fetcher.download_full_data()

    # filter the data
    _filter = Blocks(_blocks)

    # get the filtered data
    table_data = _filter.getRelationMap()

    return table_data


if __name__ =="__main__":
    job_id = ""
    print(main(job_id))