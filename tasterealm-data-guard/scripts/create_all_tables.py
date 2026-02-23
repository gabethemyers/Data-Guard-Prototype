import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from db.models.base import Base
from db.models import staging
from db.models import validation

engine = create_engine(
    "postgresql://gabriel:devpassword123@localhost:5432/tasterealm_dev"
)

Base.metadata.create_all(engine)
print("tables created")