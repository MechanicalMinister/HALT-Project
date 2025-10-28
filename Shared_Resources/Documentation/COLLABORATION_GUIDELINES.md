# Collaboration Guidelines

## Overview
This document outlines best practices for collaborating on CAD files and FEM analysis in the HALT-Project repository.

## General Principles

### 1. Communication
- **Document everything**: Write clear commit messages and maintain README files
- **Coordinate changes**: Notify team members before making changes that affect shared files
- **Ask questions**: Use GitHub Issues for discussions and questions
- **Regular updates**: Keep your work synchronized with the repository

### 2. File Organization
- **Personal folders**: Use for work-in-progress
- **Shared folders**: Use for finalized work ready for team review
- **Descriptive names**: Always use clear, descriptive file names with dates

### 3. Version Control Strategy
- **Small commits**: Commit documentation and summaries frequently
- **Descriptive messages**: Write meaningful commit messages
- **Pull before push**: Always pull latest changes before pushing your work

## CAD File Workflow

### Working on Individual Designs
1. Create project folder in your personal CAD_Files directory
2. Work on your design locally
3. Document design decisions in a README or notes file
4. Export key files in STEP format for compatibility

### Sharing Designs
1. Finalize your design
2. Create comprehensive documentation including:
   - Design intent and requirements
   - Key dimensions and specifications
   - Assembly instructions (if applicable)
   - Known issues or limitations
3. Copy files to CAD_Files/Shared/
4. Notify team members via commit message or GitHub Issue

### Design Reviews
- Review shared designs promptly
- Provide constructive feedback
- Document review comments in project README or GitHub Issues
- Acknowledge when you've incorporated feedback

## FEM Analysis Workflow

### Setting Up Analysis
1. Create analysis folder in your personal FEM_Analysis directory
2. Document the following in a README:
   - Analysis objectives
   - Software and version being used
   - Input file locations
   - Expected outputs

### Running Analysis
1. Set up geometry, mesh, materials, and boundary conditions
2. Document all assumptions
3. Run analysis (large result files are auto-ignored by Git)
4. Extract key results

### Reporting Results
1. Create results summary document (PDF preferred)
2. Include:
   - Analysis setup overview
   - Mesh convergence study (if applicable)
   - Results plots and images
   - Key findings and values
   - Conclusions and recommendations
3. Commit summary files and documentation
4. Move final report to FEM_Analysis/Shared/

### Analysis Reviews
- Verify analysis setup and assumptions
- Check mesh quality and convergence
- Validate results against hand calculations or benchmarks
- Provide feedback on interpretation

## File Naming Conventions

### CAD Files
Format: `YYYY-MM-DD_ProjectName_ComponentName_vX.extension`

Examples:
- `2025-10-28_HALT_MainBracket_v1.stp`
- `2025-11-02_HALT_HousingAssembly_v2.iges`

### FEM Analysis Files
Format: `YYYY-MM-DD_ProjectName_AnalysisType_vX_summary.extension`

Examples:
- `2025-10-28_HALT_Bracket_StressAnalysis_v1_summary.pdf`
- `2025-10-28_HALT_Bracket_StressPlot_v1.png`
- `2025-11-01_HALT_Housing_ThermalAnalysis_v2_summary.pdf`

### Documentation Files
Format: `YYYY-MM-DD_DocumentType_Topic.md`

Examples:
- `2025-10-28_DesignNotes_BracketGeometry.md`
- `2025-10-28_MeetingNotes_WeeklyReview.md`

## Git Workflow

### Daily Workflow
```bash
# Start of day: Get latest changes
git pull

# Make changes to documentation/summaries
# (CAD and FEM result files are automatically ignored)

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add stress analysis results for bracket design"

# Push changes
git push
```

### Commit Message Guidelines
- Use present tense ("Add feature" not "Added feature")
- Be specific about what changed
- Reference related issues if applicable

Examples:
- `Add initial bracket design documentation`
- `Update FEM analysis results with refined mesh`
- `Share finalized housing CAD files for review`

## Handling Large Files

### Problem
CAD and FEM result files can be very large (100MB - several GB), which makes Git inefficient.

### Solution
1. **Git ignores these files** via .gitignore
2. **Use external storage** for sharing large files:
   - Google Drive
   - Dropbox
   - OneDrive
   - Corporate file server
3. **Reference in documentation**: Include links to external storage in README files

### What to Commit
✅ DO commit:
- Documentation (README, notes, specifications)
- Small text files (setup files, material properties)
- Result summaries (PDF reports)
- Images and plots (PNG, JPG)
- Scripts and automation tools

❌ DON'T commit:
- Large CAD files (use external storage)
- Large FEM result files (use external storage)
- Temporary files
- Software-specific cache files

## Best Practices

### Documentation
- Every project should have a README
- Document assumptions and decisions
- Include references to standards or requirements
- Keep a change log for major revisions

### Quality Control
- Perform design reviews before finalizing
- Validate FEM results with hand calculations
- Check units and coordinate systems
- Verify boundary conditions make physical sense

### Backups
- Maintain local backups of all work
- Don't rely solely on Git for large files
- Keep copies of important results

### Software Versions
- Document software versions used
- Note any compatibility issues
- Maintain backward compatibility when possible

## Troubleshooting

### Large Files Accidentally Committed
If you accidentally commit large files:
1. Remove them from tracking: `git rm --cached filename`
2. Add to .gitignore if not already there
3. Commit the change

### Merge Conflicts
If merge conflicts occur:
1. Pull latest changes
2. Resolve conflicts in documentation files
3. Test that nothing is broken
4. Commit resolution

### Questions or Issues
- Open a GitHub Issue for questions
- Tag relevant team members
- Provide context and details

## Resources

### Learning Git
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Guides](https://guides.github.com/)

### CAD File Formats
- STEP/IGES for maximum compatibility
- Native formats when using same software

### FEM Best Practices
- Always perform mesh convergence studies
- Validate with analytical solutions when possible
- Document all assumptions

---

**Questions?** Open an issue or contact a team member.
