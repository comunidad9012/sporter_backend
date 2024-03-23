from sqlalchemy.orm import sessionmaker

from product_api_service.database.engine import ENGINE

create_local_session = sessionmaker(autoflush=False, autocommit=False, bind=ENGINE)
