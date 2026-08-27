from dotenv import load_dotenv
import os
load_dotenv()
from main import DataMall

Datamall=DataMall(api_key=os.getenv("LTADATAMALL_API_KEY"))
