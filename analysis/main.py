from sqlalchemy.orm import sessionmaker

from util.db import create_projects_db, add_projects_to_db
from util.read import read_project_list


def main():
    engine = create_projects_db()

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    project_list = read_project_list()

    add_projects_to_db(session, project_list)


if __name__ == "__main__":
    main()
