# CLAUDE.md - API Dummy Data Module

This module provides dummy data generation for CD-SEM (Critical Dimension Scanning Electron Microscope) equipment testing and development.

## Module Structure

- `sem_lists.py` - Generates dummy CD-SEM equipment data
- `storage.py` - Storage implementations for dummy data
- `sample_data/cd_sem_dummy_data.csv` - Sample CSV data file

## CD-SEM Equipment Data Structure

The dummy data represents CD-SEM equipment with the following structure:

### DataFrame Schema
- **Type**: pandas.DataFrame with 2D structure
- **Size**: Default 300 rows (configurable)

### Column Definitions

#### fac_id (string)
- **Description**: Facility identifier where equipment is located
- **Values**: M10, M11, M14, M15, M16, R3
- **Format**: Alphanumeric, suggesting regional/divisional organization

#### eqp_id (string)
- **Description**: Unique equipment identifier
- **Examples**: ECXDX123, PCD456, MCD789, HCDX234, ACD567, VCD890
- **Format**: Mix of alphanumeric formats (vendor-specific prefixes + 3-digit numbers)

#### eqp_model_cd (string)
- **Description**: Equipment model code
- **Values by Vendor**:
  - HITACHI: CG6300, CG6320, CG6340, CG6360, CG6380
  - AMAT: TP3000, TP3500, TP4000, TP4500, PROVISION_10, PROVISION_20, VERITYSEM_4, VERITYSEM_5

#### eqp_grp_id (string)
- **Description**: Equipment grouping identifier
- **Format**: Prefix + 2-digit number (01-03)
- **Prefixes**: G-ECD-, G-MCD-, G-KCD-, G-MDS-, G-PCD-, G-ACD-
- **Examples**: G-ECD-01, G-MCD-02, G-KCD-03

#### vendor_nm (string)
- **Description**: Vendor/manufacturer name
- **Values**: HITACHI, AMAT

#### eqp_ip (string)
- **Description**: Private IP address assigned to equipment
- **Format**: IPv4 address, primarily in 177.x.x.x or 197.x.x.x ranges
- **Examples**: 177.10.5.123, 197.168.1.45

#### fab_name (string)
- **Description**: Fabrication unit name (specific location within facility)
- **Format**: fac_id + suffix letter (A, B, or C)
- **Examples**: M16A, M14B, M10C, R4
- **Note**: R3 facility can have R4 fab_name (R stands for research center)

#### updt_dt (datetime64)
- **Description**: Last updated timestamp
- **Format**: YYYY-MM-DD HH:MM:SS
- **Range**: Within last 90 days from generation time

#### available (string)
- **Description**: Equipment operational status
- **Values**: "On", "Off"
- **Distribution**: 90% "On", 10% "Off"

#### version (int64)
- **Description**: Equipment software/firmware version
- **Values**: 1, 2, 3

## Usage

```python
from api.dummy.sem_lists import generate_equipment_data, df

# Use the default dataset
equipment_df = df

# Generate a custom dataset
custom_df = generate_equipment_data(n_rows=500)
```

## Data Consistency Rules

1. Equipment IDs are unique across the dataset
2. Vendor names match their respective model codes
3. IP addresses use private network ranges (177.x.x.x or 197.x.x.x)
4. Fab names are derived from facility IDs with appropriate suffixes
5. Update dates are realistic (within 90 days)

## CD-SEM Storage Information Data Structure

The storage module provides dummy data for CD-SEM equipment storage metrics and recipe counts.

### DataFrame Schema
- **Type**: pandas.DataFrame with storage metrics for CD-SEM equipment
- **Size**: Default 300 rows (matches equipment data)

### Column Definitions

#### eqp_id (string)
- **Description**: Unique equipment identifier
- **Format**: Same as equipment data

#### eqp_ip (string)
- **Description**: Private IP address assigned to equipment
- **Examples**: 177.10.5.123, 197.168.1.45, 177.254.100.200
- **Format**: IPv4 address in 177.x.x.x or 197.x.x.x ranges
- **Range**: x.1-254.1-254.1-254

#### fac_id (string)
- **Description**: Facility identifier where equipment is located
- **Format**: Letter + number indicating regional/divisional organization

#### total (string)
- **Description**: Total storage capacity allocated to the equipment
- **Examples**: 766G, 850G, 1.5T, 2.0T
- **Format**: Number + unit (G for Gigabytes, T for Terabytes)
- **Range**:
  - GB: 500G - 999G (70% probability)
  - TB: 1.0T - 2.0T (30% probability)

#### used (string)
- **Description**: Storage currently utilized by recipes/data
- **Examples**: 361G, 425G, 1.2T
- **Format**: Number + unit (G or T)
- **Calculation**: 20% - 90% of total storage capacity

#### avail (string)
- **Description**: Available free storage space
- **Examples**: 405G, 275G, 0.3T
- **Format**: Number + unit (G or T)
- **Calculation**: total - used

#### percent (string)
- **Description**: Percentage of utilized storage relative to total
- **Examples**: 47%, 72%, 85%
- **Format**: Integer percentage with % symbol
- **Range**: 20% - 90%
- **Calculation**: (used / total) × 100, rounded to integer

#### storage_mt (datetime64)
- **Description**: Timestamp when storage metrics were collected
- **Format**: YYYY-MM-DD HH:MM:SS.ffffff
- **Example**: 2024-03-15 14:23:45.123456
- **Range**: Within last 7 days from current time

#### rcp_counts (int64)
- **Description**: Total number of recipes stored on the equipment
- **Examples**: 127, 289, 456
- **Range**: 50 - 500

#### rcp_counts_mt (datetime64)
- **Description**: Timestamp when recipe count was last updated
- **Format**: YYYY-MM-DD HH:MM:SS.ffffff
- **Example**: 2024-03-15 14:45:12.654321
- **Relationship**: Usually within ±12 hours of storage_mt

#### storage_mt_date (datetime64)
- **Description**: Date portion of storage_mt (no time component)
- **Format**: YYYY-MM-DD
- **Example**: 2024-03-15

#### fab_name (string)
- **Description**: Fabrication unit name (specific location within facility)

#### eqp_model_cd (string)
- **Description**: Equipment model code
- **Format**: Model series with version/generation numbers

### Data Relationships
- **Equipment Identity**: eqp_id is unique and corresponds to specific eqp_model_cd and vendor
- **Location Hierarchy**: fac_id → fab_name (fab_name = fac_id + location suffix)
- **Storage Calculation**: total = used + avail
- **Utilization**: percent = (used / total) × 100
- **Timestamp Correlation**: storage_mt_date is derived from storage_mt

### Usage Notes
- Storage values can be in GB or TB format - ensure proper unit conversion when processing
- Timestamps (storage_mt, rcp_counts_mt) include microseconds for precise tracking
- IP addresses are in private ranges suitable for internal network deployment
- Recipe counts may update at different intervals than storage metrics (see timestamp difference)

### Storage Usage

```python
from api.dummy.storage import generate_storage_data, df

# Use the default storage dataset
storage_df = df

# Generate a custom storage dataset
custom_storage_df = generate_storage_data(n_rows=500)
```