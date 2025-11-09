# Task 1: HBase Table for Vehicle Repair System
# Student Name: Rohit Panda
# Student UOWID: 89430060
# Date: November 2025

# Create table with column families
create 'VEHICLE_REPAIR', 'VEHICLE', 'REPAIR', 'OWNER', 'TIME'

# Configure versions for REPAIR column family (to track repair history)
alter 'VEHICLE_REPAIR', {NAME=>'REPAIR', VERSIONS=>'3'}

# Verify table structure
describe 'VEHICLE_REPAIR'

# ==========================================
# Load Sample Data - Vehicle 1 (Owner 1)
# ==========================================

# Owner 1 Information
put 'VEHICLE_REPAIR', 'owner:001', 'OWNER:licence-number', 'L001'
put 'VEHICLE_REPAIR', 'owner:001', 'OWNER:first-name', 'John'
put 'VEHICLE_REPAIR', 'owner:001', 'OWNER:last-name', 'Smith'
put 'VEHICLE_REPAIR', 'owner:001', 'OWNER:phone', '555-0101'

# Vehicle 1 Information
put 'VEHICLE_REPAIR', 'vehicle:V001', 'VEHICLE:registration', 'ABC123'
put 'VEHICLE_REPAIR', 'vehicle:V001', 'VEHICLE:make', 'Toyota'
put 'VEHICLE_REPAIR', 'vehicle:V001', 'VEHICLE:model', 'Camry'
put 'VEHICLE_REPAIR', 'vehicle:V001', 'OWNER:licence-number', 'L001'

# Repair 1 for Vehicle 1
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'REPAIR:labour-cost', '250.00'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'REPAIR:parts-cost', '150.00'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'REPAIR:complexity-level', 'medium'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'VEHICLE:registration', 'ABC123'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'TIME:day', '15'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'TIME:month', '10'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'TIME:year', '2025'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'TIME:start-date', '2025-10-15'
put 'VEHICLE_REPAIR', 'repair:V001|R001', 'TIME:end-date', '2025-10-17'

# Repair 2 for Vehicle 1
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'REPAIR:labour-cost', '180.00'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'REPAIR:parts-cost', '95.50'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'REPAIR:complexity-level', 'low'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'VEHICLE:registration', 'ABC123'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'TIME:day', '5'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'TIME:month', '11'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'TIME:year', '2025'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'TIME:start-date', '2025-11-05'
put 'VEHICLE_REPAIR', 'repair:V001|R002', 'TIME:end-date', '2025-11-06'

# ==========================================
# Load Sample Data - Vehicle 2 (Owner 2)
# ==========================================

# Owner 2 Information
put 'VEHICLE_REPAIR', 'owner:002', 'OWNER:licence-number', 'L002'
put 'VEHICLE_REPAIR', 'owner:002', 'OWNER:first-name', 'Sarah'
put 'VEHICLE_REPAIR', 'owner:002', 'OWNER:last-name', 'Johnson'
put 'VEHICLE_REPAIR', 'owner:002', 'OWNER:phone', '555-0202'

# Vehicle 2 Information
put 'VEHICLE_REPAIR', 'vehicle:V002', 'VEHICLE:registration', 'XYZ789'
put 'VEHICLE_REPAIR', 'vehicle:V002', 'VEHICLE:make', 'Honda'
put 'VEHICLE_REPAIR', 'vehicle:V002', 'VEHICLE:model', 'Accord'
put 'VEHICLE_REPAIR', 'vehicle:V002', 'OWNER:licence-number', 'L002'

# Repair 1 for Vehicle 2
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'REPAIR:labour-cost', '320.00'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'REPAIR:parts-cost', '275.00'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'REPAIR:complexity-level', 'high'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'VEHICLE:registration', 'XYZ789'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'TIME:day', '20'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'TIME:month', '10'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'TIME:year', '2025'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'TIME:start-date', '2025-10-20'
put 'VEHICLE_REPAIR', 'repair:V002|R001', 'TIME:end-date', '2025-10-23'

# Repair 2 for Vehicle 2
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'REPAIR:labour-cost', '145.00'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'REPAIR:parts-cost', '85.00'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'REPAIR:complexity-level', 'low'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'VEHICLE:registration', 'XYZ789'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'TIME:day', '8'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'TIME:month', '11'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'TIME:year', '2025'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'TIME:start-date', '2025-11-08'
put 'VEHICLE_REPAIR', 'repair:V002|R002', 'TIME:end-date', '2025-11-09'

# ==========================================
# Verification Queries
# ==========================================

# List all tables
list

# Scan entire table
scan 'VEHICLE_REPAIR'

# Get specific owner information
get 'VEHICLE_REPAIR', 'owner:001'

# Get specific vehicle information
get 'VEHICLE_REPAIR', 'vehicle:V001'

# Get all repairs for Vehicle 1
scan 'VEHICLE_REPAIR', {STARTROW => 'repair:V001|', STOPROW => 'repair:V001~'}

# Count total rows
count 'VEHICLE_REPAIR'
