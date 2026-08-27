import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
import os
load_dotenv()
from main import DataMall

Datamall=DataMall(api_key=os.getenv("LTADATAMALL_API_KEY"))

print(Datamall.bus.routes.get_bus_routes())
