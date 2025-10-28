# Design and Analysis Standards

## Purpose
This document establishes standards for CAD design and FEM analysis work in the HALT-Project to ensure consistency, quality, and effective collaboration.

## CAD Design Standards

### Units
- **Standard Unit System**: SI (metric)
  - Length: millimeters (mm)
  - Mass: kilograms (kg)
  - Force: Newtons (N)
  - Pressure: Pascals (Pa) or MPa
  - Temperature: Celsius (°C) or Kelvin (K)

- **Alternative**: If using Imperial units, clearly document in all files

### Coordinate System
- **Global Origin**: Define and document for each assembly
- **Standard Orientation**:
  - X-axis: [Define standard direction]
  - Y-axis: [Define standard direction]
  - Z-axis: [Define standard direction - typically vertical]

### File Naming
- Use descriptive names with dates
- Format: `YYYY-MM-DD_ProjectName_ComponentName_vX.extension`
- No spaces in filenames (use underscores or hyphens)
- Version numbers start at v1 and increment

### File Formats
- **Primary Exchange Format**: STEP (.stp, .step) - AP214 or AP242
- **Secondary Format**: IGES (.iges, .igs) - for legacy compatibility
- **Visualization**: STL (.stl) - for 3D printing or visualization
- **Native Format**: Keep original files in software-specific format

### Model Organization
- **Part Files**: Single component per file
- **Assembly Files**: Clear hierarchy and structure
- **Reference Planes**: Include reference geometry for assembly
- **Origin**: Part origin should be at logical location

### Design Features
- **Parametric Design**: Use parameters and equations where possible
- **Feature Names**: Use descriptive names for features
- **Configurations**: Document all configurations clearly
- **Derived Parts**: Document parent-child relationships

### Documentation Requirements
Each design must include:
- Design intent and objectives
- Key dimensions and tolerances
- Material specification
- Manufacturing method
- Assembly instructions (if applicable)
- Revision history

## FEM Analysis Standards

### Analysis Planning
Before starting analysis:
1. Define clear objectives and questions to answer
2. Identify critical failure modes
3. Determine required accuracy
4. Select appropriate analysis type

### Geometry Preparation
- **Simplification**: Document all geometry simplifications
- **Cleanup**: Remove unnecessary features (small fillets, chamfers)
- **Suppression**: Remove features that don't affect results
- **Partitioning**: Split bodies for mesh control or contact
- **Defeaturing**: Balance between accuracy and computational cost

### Material Models
- Use validated material properties
- Document material source (standard, test data, literature)
- Include all required properties for analysis type
- Note temperature dependence if applicable
- Document safety factors applied

### Meshing Guidelines

#### Element Selection
- **Structural**: Second-order tetrahedral or hexahedral elements preferred
- **Thermal**: First-order elements often sufficient
- **Dynamic**: Consider element formulation carefully

#### Element Size
- **General Rule**: 3-5 elements through thickness
- **Stress Concentrations**: Refine mesh at critical locations
- **Convergence**: Perform mesh convergence study

#### Mesh Quality Criteria
- **Aspect Ratio**: < 5 preferred, < 10 acceptable
- **Jacobian**: > 0.6 preferred
- **Skewness**: < 0.8 preferred
- **Warpage**: < 10 degrees preferred

### Boundary Conditions

#### Constraints
- **Fixed Supports**: Use only when fully constrained in reality
- **Symmetry**: Use when applicable to reduce model size
- **Remote Points**: Use for complex constraints
- **Springs**: Use to simulate flexible supports

#### Loads
- **Application**: Apply at correct location and direction
- **Magnitude**: Verify units and values
- **Distribution**: Uniform, varying, or point loads
- **Safety Factors**: Document any factors applied

#### Contact
- **Bonded**: Use when parts are welded, glued, or integral
- **No Separation**: Parts can slide but not separate
- **Frictionless**: No friction in tangential direction
- **Frictional**: Include coefficient of friction

### Solution Settings
- **Solver Selection**: Direct for small models, iterative for large
- **Convergence**: Set appropriate tolerances
- **Substeps**: Use multiple substeps for nonlinear analyses
- **Output Controls**: Request necessary results only

### Results Interpretation

#### Required Outputs
- Maximum von Mises stress
- Maximum displacement
- Maximum principal stresses (if applicable)
- Safety factors (based on yield or ultimate strength)
- Reaction forces

#### Validation Checks
1. Check reaction forces balance applied loads
2. Verify deformation is reasonable
3. Compare to hand calculations where possible
4. Review stress singularities (ignore if at sharp corners)
5. Check energy balance (if applicable)

#### Documentation
- Create clear contour plots with legends
- Use appropriate color scales
- Include deformation scale factor
- Annotate critical values and locations
- Export high-resolution images

### Reporting Standards

#### Analysis Report Must Include
1. **Executive Summary**
   - Objective
   - Key findings
   - Conclusions
   - Recommendations

2. **Model Description**
   - Geometry source
   - Material properties
   - Mesh information

3. **Loading and Boundary Conditions**
   - All constraints clearly described
   - All loads documented

4. **Results**
   - Contour plots
   - Tables of critical values
   - Comparison to criteria

5. **Validation**
   - Verification methods used
   - Comparison results

6. **Conclusions**
   - Does design meet requirements?
   - Recommended changes
   - Further work needed

## Quality Assurance

### Design Review Checklist
- [ ] Design intent documented
- [ ] Requirements met
- [ ] Materials specified
- [ ] Manufacturing feasibility considered
- [ ] Tolerances appropriate
- [ ] Assembly considerations addressed
- [ ] Files exported in STEP format
- [ ] Documentation complete

### Analysis Review Checklist
- [ ] Objectives clearly stated
- [ ] Geometry appropriate
- [ ] Material properties validated
- [ ] Mesh quality acceptable
- [ ] Mesh convergence demonstrated
- [ ] Boundary conditions realistic
- [ ] Loads correctly applied
- [ ] Results validated
- [ ] Assumptions documented
- [ ] Conclusions clear
- [ ] Report complete

## Version Control Standards

### Commit Messages
- Use present tense
- Be specific and descriptive
- Reference related issues

### File Organization
- Keep related files together
- Use consistent naming
- Document file relationships

### Branching Strategy
- `main`: Stable, reviewed work
- `feature/*`: New features or major changes
- `bugfix/*`: Corrections and fixes

## Safety and Compliance

### Safety Factors
- Document all safety factors used
- Consider failure modes
- Account for uncertainties
- Follow industry standards

### Standards Compliance
Document compliance with relevant standards:
- ASME (American Society of Mechanical Engineers)
- ISO (International Organization for Standardization)
- Industry-specific standards
- Company/project-specific requirements

## Training and Resources

### Required Skills
- CAD software proficiency
- FEM fundamentals
- Material science basics
- Structural mechanics
- Git version control

### Recommended Training
- FEM best practices courses
- CAD advanced techniques
- Design for manufacturing
- Git and GitHub

### Reference Materials
- Software documentation
- FEM textbooks
- Design handbooks
- Industry standards

## Continuous Improvement

### Feedback
- Regularly review and update standards
- Incorporate lessons learned
- Adapt to new tools and methods

### Best Practices
- Share successful techniques
- Document common pitfalls
- Maintain knowledge base

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-28  
**Next Review**: [Schedule regular reviews]
