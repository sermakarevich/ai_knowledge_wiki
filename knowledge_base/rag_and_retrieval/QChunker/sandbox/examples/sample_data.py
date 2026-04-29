"""Sample domain document for testing QChunker pipeline.

This simulates a dense technical document with terminology, abbreviations,
and contextual dependencies -- the kind of document where naive chunking
produces fragmented, incomprehensible chunks.
"""

SAMPLE_DOCUMENT = """\
Lithium-Ion Battery Safety Assessment Protocol (Rev. 3.2)

1. Overview

This document establishes the safety assessment protocol for Li-ion \
battery systems used in electric vehicles (EVs). The protocol follows \
UN/ECE R100 (Regulation No. 100) and GB/T 31485-2015 standards. All \
testing must be conducted by certified laboratories holding CNAS \
accreditation (China National Accreditation Service for Conformity \
Assessment).

The State of Charge (SOC) must be maintained at 100% before all abuse \
tests unless otherwise specified. The Battery Management System (BMS) \
must remain active during all test phases.

2. Thermal Abuse Testing

The Thermal Propagation Test (TPT) evaluates cell-to-cell thermal runaway \
propagation within the battery pack. Per GB 38031-2020 Section 8.2.2, \
the trigger cell must be heated at a rate of 5°C/min until thermal runaway \
onset, defined as dT/dt > 1°C/s.

The pack must provide a minimum 5-minute warning before hazardous gas \
concentration in the passenger compartment exceeds the Immediately \
Dangerous to Life or Health (IDLH) threshold. The IDLH value for hydrogen \
fluoride (HF), the primary toxic byproduct, is 30 ppm per NIOSH \
standards.

Acceptance criteria: No fire or explosion for 5 minutes after thermal \
runaway trigger. The Thermal Management System (TMS) must maintain \
adjacent cell temperatures below 150°C during the propagation window.

3. Mechanical Abuse Testing

The Crush Test follows SAE J2464 Section 5.2. The battery pack is \
compressed at 1 mm/s using a 150mm-radius hemispherical indenter until \
a 30% dimensional reduction or 200 kN force is reached, whichever occurs \
first. Post-crush, the pack must be monitored for 1 hour.

The Nail Penetration Test (NPT) uses a 3mm-diameter steel nail driven \
at 80 mm/s through the cell center. This simulates internal short circuit \
(ISC) conditions. The cell voltage must be monitored at 1 kHz sampling \
rate during NPT.

4. Electrical Abuse Testing

External Short Circuit (ESC) testing connects battery terminals through \
a resistance < 5 mΩ for 10 minutes at SOC=100%. The maximum skin \
temperature of the casing must not exceed 150°C per IEC 62660-3.

Overcharge testing charges the cell at 1C rate to 200% SOC or until the \
BMS interrupt threshold is reached. The Cell Voltage Management Unit \
(CVMU) must trigger a protective disconnect within 10 seconds of \
detecting any cell exceeding 4.25V (for NMC chemistry) or 3.75V \
(for LFP chemistry).

5. Documentation Requirements

All test results must be reported using the UNECE GTR-20 template. \
The report must include the Failure Mode and Effects Analysis (FMEA) \
for each test, thermal imaging data at 30 fps minimum, and gas \
chromatography results for off-gas analysis. Reports must reference the \
Battery Passport ID as defined in EU Battery Regulation 2023/1542 \
Article 77.
"""
