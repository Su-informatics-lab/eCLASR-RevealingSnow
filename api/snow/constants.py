# Configuration Keys
LOGGING_CONFIG_FILE = 'LOGGING_CONFIG_FILE'
SCREENING_DATA_FILE = 'SCREENING_DATA_FILE'
CRITERIA_DATA_MODEL_FILE = 'CRITERIA_DATA_MODEL_FILE'
TRACKING_API_ENABLED = 'TRACKING_API_ENABLED'
TRACKING_API_URL_BASE = 'TRACKING_API_URL_BASE'
TRACKING_API_EXPORT_PATH = 'TRACKING_API_EXPORT_PATH'
TRACKING_API_AUTH_USER = 'TRACKING_API_AUTH_USER'
TRACKING_API_AUTH_PASS = 'TRACKING_API_AUTH_PASS'
TRACKING_API_TIMEOUT = 'TRACKING_API_TIMEOUT'

# Environmnent Keys
DEFAULT_ENVIRONMENT_FILE = '.config.env'
RSENV_FILE = 'RSENV_FILE'

# Criteria Data Model & Metadata Keys
FILTERS = 'filters'
YMCA_SITES = 'ymca_sites'
PATIENT_SUBSET = 'patient_subset'
EXPORT_LABEL = 'label'
EXPORT_DESCRIPTION = 'description'
EXPORT_USER = 'userid'
DATA_VERSION = 'data_version'
VERSION_DETAILS = 'version_details'

# Filter Keys
FLK_KEY = 'key'
FLK_TYPE = 'type'

# Filter Types
FLT_TOGGLE = 'toggle'
FLT_RANGE = 'range'
FLT_DATE_TOGGLE = 'date_toggle'

# Special Query Argument Keys
QK_SITE = 'site'
QK_SITE_MAXDIST = 'maxdist'
QK_SITE_MINDIST = 'mindist'

QK_LIMIT_LAST_VISIT_DATE = 'last_encounter_date'
QK_LIMIT_CLOSEST_YMCA = 'closest_ymca'

QK_EXPORT_LIMIT = 'limit'
QK_EXPORT_ORDER_BY = 'order_by'
QK_EXPORT_ORDER_ASC = 'order_asc'
QK_EXPORT_ORDER_VALUES = [QK_LIMIT_LAST_VISIT_DATE, QK_LIMIT_CLOSEST_YMCA]

# Version-Related Keys
APP_VERSION_KEY = 'app'
VERSION_KEY = 'key'
VERSION_LABEL_KEY = 'label'
VERSION_DATE_KEY = 'date'
VERSION_VERSION_KEY = 'version'

# Export
EXPORT_FILENAME = 'patients.zip'
EXPORT_FILE_PATIENTS = 'patients.txt'
EXPORT_FILE_METADATA = 'metadata.yml'

# Demographic Columns
COL_PTNUM = 'patient_num'
COL_SEX = 'sex'
COL_RACE = 'race'
COL_ETHNICITY = 'ethnicity'
COL_AGE = 'age'

COL_YMCA_PREFIX = 'ymca_'

# Special Response Keys
RK_TOTAL = 'total'

# Export Payload Keys
EP_ID = 'id'
EP_TS = 'timestamp'
EP_SUBJECTS = 'subjects'
EP_METADATA = 'metadata'
EP_FLAGS = 'flags'

# Static Export Flags (only change for manual API calls, outside of viz tool)
EP_FLAG_VALUES = {
    'source': 'EMR',
    'mailing_type': 'EMR',
    'research_project': False,
    'site': 'TBD'
}
