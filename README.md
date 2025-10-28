# HALT-Project

## CAD Files and FEM Analysis Collaboration Workspace

This repository is designed for collaborative work on CAD files and Finite Element Method (FEM) analysis between three team members.

## 📁 Repository Structure

```
HALT-Project/
├── CAD_Files/              # CAD design files
│   ├── Person_1/          # Individual workspace for Person 1
│   ├── Person_2/          # Individual workspace for Person 2
│   ├── Person_3/          # Individual workspace for Person 3
│   └── Shared/            # Finalized CAD files for team review
├── FEM_Analysis/           # FEM analysis files and results
│   ├── Person_1/          # Individual FEM work for Person 1
│   ├── Person_2/          # Individual FEM work for Person 2
│   ├── Person_3/          # Individual FEM work for Person 3
│   └── Shared/            # Shared analysis results and reports
└── Shared_Resources/       # Common resources
    ├── Documentation/     # Project documentation and guides
    ├── Standards/         # Design standards and specifications
    └── Templates/         # CAD and analysis templates
```

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/MechanicalMinister/HALT-Project.git
cd HALT-Project
```

### 2. Set Up Your Workspace
- Navigate to your assigned person folder (Person_1, Person_2, or Person_3)
- Create subdirectories for your projects as needed

### 3. Working with CAD Files
- Place work-in-progress CAD files in your personal folder: `CAD_Files/Person_X/`
- Once finalized, copy or move files to `CAD_Files/Shared/` for team review
- Follow the naming conventions outlined in the Collaboration Guidelines

### 4. Working with FEM Analysis
- Store analysis input files and scripts in your personal folder: `FEM_Analysis/Person_X/`
- Export result summaries (PDF, images, small data files) for version control
- Large result files (.rst, .odb, etc.) are automatically ignored by Git
- Share final analysis reports in `FEM_Analysis/Shared/`

## 📝 File Management Guidelines

### Supported CAD Formats
- STEP (.stp, .step) - Preferred for sharing
- IGES (.iges, .igs)
- STL (.stl)
- Native formats (SolidWorks, CATIA, Inventor, etc.)

### Supported FEM Software
- ANSYS
- Abaqus
- LS-DYNA
- COMSOL
- NX Nastran
- Other FEM packages

### Best Practices
1. **Naming Convention**: Use descriptive names with dates
   - Example: `2025-10-28_BracketDesign_v1.stp`
   - Example: `2025-10-28_StressAnalysis_Bracket_v1_summary.pdf`

2. **Version Control**:
   - Large binary CAD/FEM files are ignored by Git
   - Commit only summaries, reports, and documentation
   - Use external file sharing (cloud storage) for large files if needed

3. **Documentation**:
   - Include README files in project subdirectories
   - Document assumptions and boundary conditions for FEM analysis
   - Keep a log of design changes and analysis revisions

4. **Collaboration**:
   - Use descriptive commit messages
   - Review shared files before starting dependent work
   - Communicate design changes that affect others

## 🔧 Workflow Example

### For CAD Work:
1. Create your design in `CAD_Files/Person_X/ProjectName/`
2. Export key files as STEP format for compatibility
3. Add a README or documentation file describing the design
4. When ready, move finalized files to `CAD_Files/Shared/`
5. Commit documentation and small reference files to Git

### For FEM Analysis:
1. Set up analysis in `FEM_Analysis/Person_X/ProjectName/`
2. Run simulations (large result files auto-ignored)
3. Export results summary (images, plots, PDF reports)
4. Commit summary files and analysis documentation
5. Share final reports in `FEM_Analysis/Shared/`

## 📚 Additional Resources

- See `Shared_Resources/Documentation/` for detailed guides
- Check `Shared_Resources/Standards/` for design standards
- Use `Shared_Resources/Templates/` for starting templates

## 🤝 Team Communication

- Use GitHub Issues for tracking tasks and problems
- Use Pull Requests for major changes that need review
- Document decisions in commit messages and README files

## ⚠️ Important Notes

- **Large Files**: CAD and FEM result files are excluded from Git tracking. Use external storage (Google Drive, OneDrive, Dropbox, etc.) for sharing large files and reference them in documentation
- **Backups**: Maintain regular backups of your work outside this repository
- **Software Versions**: Document which software versions you're using in your analysis reports

## 📖 License

[Add your license information here]

## 👥 Contributors

- Person 1: [Name/Email]
- Person 2: [Name/Email]
- Person 3: [Name/Email]