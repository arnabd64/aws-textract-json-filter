import boto3
from time import sleep


class Fetcher:

    def __init__(self, job_id):
        self.job_id = job_id
        self.textract = boto3.client("textract")


    def wait(self, retries: int = 10):
        for _ in range(10):
            _response = self.textract.get_document_analysis(self.job_id)
            if _response["JobStatus"] == "SUCCEEDED":
                print("INFO: Job COMPLETE")
                return True
            
            else:
                print("INFO: Job in PROGRESS. Waiting 5 seconds ...")
                sleep(5)

        print(f"INFO: Job Timed Out after {5 * retries} seconds")
        return False


    def download_full_data(self):
        # candidate response
        _blocks= list()
        next_token = None

        while True:
            if next_token:
                _response = self.textract.get_document_analysis(JobId = self.job_id, NextToken = next_token)

            else:
                _response = self.textract.get_document_analysis(JobId = self.job_id)

            _blocks.extend(_response["Blocks"])

            if "NextToken" in _response:
                next_token = _response["NextToken"]

            else:
                break

        return _blocks
