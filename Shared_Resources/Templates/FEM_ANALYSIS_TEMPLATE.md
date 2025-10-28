# FEM Analysis Template

## Analysis Information
- **Project Name**: [Enter analysis name]
- **Date Started**: [YYYY-MM-DD]
- **Analyst**: [Person 1/2/3]
- **Status**: [In Progress / Under Review / Finalized]
- **Last Updated**: [YYYY-MM-DD]

## Analysis Objectives
[Describe the purpose of this analysis]

### Questions to Answer
1. [Question 1]
2. [Question 2]
3. [Question 3]

## Software Information
- **FEM Software**: [e.g., ANSYS Workbench 2024 R1]
- **Solver Type**: [e.g., Static Structural, Thermal, Modal]
- **Version**: [Software version number]

## Geometry
### Source
- **CAD File**: [filename or link]
- **Format**: [e.g., STEP, IGES]
- **Location**: [Path or external storage link]

### Simplifications
- [List any geometry simplifications made]
- [Reason for each simplification]

### Coordinate System
- Origin: [Describe origin location]
- X-axis: [Direction]
- Y-axis: [Direction]
- Z-axis: [Direction]

## Material Properties
### Material 1: [Material Name]
- Type: [e.g., Isotropic, Orthotropic]
- Young's Modulus: [value + units]
- Poisson's Ratio: [value]
- Density: [value + units]
- Yield Strength: [value + units]
- Ultimate Strength: [value + units]
- Thermal Expansion: [value + units] (if applicable)
- Thermal Conductivity: [value + units] (if applicable)

### Material 2: [Material Name] (if applicable)
- [Same properties as above]

## Mesh Information
### Mesh Settings
- **Element Type**: [e.g., SOLID187, C3D8]
- **Element Size**: [value + units]
- **Refinement**: [Locations and sizing]
- **Total Elements**: [number]
- **Total Nodes**: [number]

### Mesh Quality
- **Aspect Ratio**: [Max value]
- **Jacobian**: [Min value]
- **Skewness**: [Max value]

### Mesh Convergence
[Describe mesh convergence study if performed]
- Mesh 1: [X elements, Result Y]
- Mesh 2: [X elements, Result Y]
- Mesh 3: [X elements, Result Y]
- Convergence: [% change]

## Boundary Conditions

### Constraints (Fixed Supports)
- Location 1: [Describe location and type]
  - DOF Fixed: [X, Y, Z, RX, RY, RZ]
  - Reason: [Why this constraint]

- Location 2: [Describe location and type]
  - DOF Fixed: [Specify]
  - Reason: [Why this constraint]

### Loads
- Load 1: [Type - Force, Pressure, etc.]
  - Location: [Describe]
  - Magnitude: [value + units]
  - Direction: [Specify]
  - Reason: [Physical basis]

- Load 2: [Type]
  - Location: [Describe]
  - Magnitude: [value + units]
  - Direction: [Specify]
  - Reason: [Physical basis]

### Contact Conditions (if applicable)
- Contact Pair 1:
  - Type: [Bonded, Frictionless, Frictional]
  - Surfaces: [Describe]
  - Coefficient of Friction: [if applicable]

## Analysis Settings
- **Analysis Type**: [Static, Dynamic, Thermal, etc.]
- **Solver Type**: [Direct, Iterative]
- **Convergence Criteria**: [Tolerance values]
- **Time Steps**: [if transient]
- **Load Steps**: [if multiple]

## Results Summary

### Maximum Values
- Maximum Stress (von Mises): [value + units at location]
- Maximum Displacement: [value + units at location]
- Maximum Strain: [value + units at location]
- Safety Factor (minimum): [value at location]

### Critical Locations
1. Location 1: [Description]
   - Stress: [value]
   - Factor of Safety: [value]
   - Assessment: [Pass/Fail]

2. Location 2: [Description]
   - Stress: [value]
   - Factor of Safety: [value]
   - Assessment: [Pass/Fail]

## Results Validation

### Verification Methods
- [ ] Hand calculation comparison
- [ ] Literature/benchmark comparison
- [ ] Physical testing comparison
- [ ] Sensitivity study

### Validation Results
[Describe how results were validated]
- Expected: [value]
- Calculated: [value]
- Difference: [%]

## Assumptions
1. [List all assumptions made in the analysis]
2. [Material behavior assumptions]
3. [Loading assumptions]
4. [Geometric assumptions]
5. [Boundary condition assumptions]

## Limitations
1. [List limitations of this analysis]
2. [What was not captured]
3. [Areas of uncertainty]

## Conclusions
### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Design Assessment
- [ ] Design meets requirements
- [ ] Design requires modification
- [ ] Further analysis needed

## Files Generated
### Input Files
- [List input files and locations]

### Output Files (Large - not in Git)
- [List result files and locations in external storage]

### Summary Files (In Git)
- [filename.pdf] - Full analysis report
- [filename.png] - Stress contour plot
- [filename.png] - Displacement plot
- [filename.csv] - Key results data (if small)

## Review Status
### Review 1 (YYYY-MM-DD)
- Reviewer: [Name]
- Comments: [Summary]
- Action Items: [List]
- Status: [Resolved/Pending]

## Revision History
### Version 1 (YYYY-MM-DD)
- Initial analysis
- [Key parameters]

### Version 2 (YYYY-MM-DD)
- [Changes made]
- [Reason for revision]

## References
- [Standards applied]
- [Literature references]
- [Related analyses]

---
**Contact**: [Your name/email for questions]
