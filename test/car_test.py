import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
import os
load_dotenv()
from main import DataMall
key=os.getenv("LTADATAMALL_API_KEY")
Datamall=DataMall(api_key=key)

print(Datamall.carpark.get_carpark_availability())
