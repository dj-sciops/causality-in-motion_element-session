import datajoint as dj
from element_animal import subject
from element_lab import lab, project

from element_session import DB_PREFIX

# TODO: These need to be activated from the forks of the element_lab and element_animal modules
lab.activate(f"{DB_PREFIX}lab")
Lab = lab.Lab
User = lab.User
Protocol = lab.Protocol
project.activate(f"{DB_PREFIX}project", linking_module=__name__)
Source = lab.Source
subject.activate(f"{DB_PREFIX}subject", linking_module=__name__)


schema = dj.schema(f"{DB_PREFIX}session")


@schema
class Session(dj.Manual):
    """Central Session table

    Attributes:
        Subject (foreign key): Key for Subject table
        session_id ( VARCHAR(16) ): Unique numeric session ID
        session_datetime (datetime): date and time of the session
        session_type( VARCHAR(32) ): type of session, e.g. 'behavior', 'ephys', 'training', 'recording'
    """

    definition = """
    # Top-level, singular, discrete instance of an experiment or task run
    -> subject.Subject
    session_id                               : VARCHAR(16)                 # session number or other identifier
    ---
    session_datetime=NULL                    : DATETIME                    # beginning of a session as a microsecond precision datetime
    session_type=NULL                        : VARCHAR(32)                 # type of session, e.g. 'behavior', 'ephys', 'training', 'recording'
    """

    class Attribute(dj.Part):
        """Additional feature of interest for a session.

        Attributes:
            Session (foreign key): Key for Session table
            attribute_name ( varchar(32) ): Name shared across instances of attribute
            attribute_value ( varchar(2000), optional ):  Attribute value
            attribute_blob (longblob, optional): Optional data store field
        """

        definition = """
        -> master
        attribute_name: varchar(32)
        ---
        attribute_value='': varchar(2000)
        attribute_blob=null: longblob
        """


@schema
class SessionDirectory(dj.Manual):
    """Relative path information for files related to a given session.

    Attributes:
        Session (foreign key): Key for Session table
        session_dir ( varchar(256) ): Path to the data directory for a session
    """

    definition = """
    -> Session
    ---
    session_dir: varchar(256) # Path to the data directory for a session
    """


@schema
class SessionExperimenter(dj.Manual):
    """Individual(s) conducting the session

    Attributes:
        Session (foreign key): Key for Session table
        User (foreign key): Key for User table
    """

    definition = """
    # Individual(s) conducting the session
    -> Session
    -> lab.User
    """


@schema
class SessionNote(dj.Manual):
    """Additional notes related to a given session

    Attributes:
        Session (foreign key): Key for Session table
        session_note ( varchar(1024) ): : Additional notes
    """

    definition = """
    -> Session
    ---
    session_note: varchar(1024)
    """


@schema
class ProjectSession(dj.Manual):
    """Table linking upstream Projects with Session

    Attributes:
        Project (foreign key): Key for Project table
        Session (foreign key): Key for Session table
    """

    definition = """
    -> project.Project
    -> Session
    """
