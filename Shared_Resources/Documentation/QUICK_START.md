# Quick Start Guide

## Welcome to HALT-Project!

This guide will help you get started with the CAD and FEM collaboration workspace.

## Prerequisites

### Software You'll Need
- **Git**: For version control ([Download Git](https://git-scm.com/downloads))
- **CAD Software**: SolidWorks, CATIA, Inventor, or similar
- **FEM Software**: ANSYS, Abaqus, LS-DYNA, or similar
- **PDF Reader**: For viewing reports
- **Text Editor**: For documentation (VS Code, Notepad++, etc.)

### Skills You Should Have
- Basic Git knowledge (clone, commit, push, pull)
- Familiarity with your CAD software
- Understanding of FEM analysis basics

## Step-by-Step Setup

### 1. Clone the Repository

Open a terminal/command prompt and run:
```bash
git clone https://github.com/MechanicalMinister/HALT-Project.git
cd HALT-Project
```

### 2. Identify Your Workspace

You'll be assigned one of three personal workspaces:
- **Person_1**: First team member
- **Person_2**: Second team member
- **Person_3**: Third team member

Ask your team lead which workspace is yours.

### 3. Set Up External Storage (for large files)

Since CAD and FEM files are too large for Git, set up a shared storage location:
- Create a shared folder on Google Drive, OneDrive, or Dropbox
- Share access with all team members
- Document the link in your project README files

### 4. Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Your First Project

### Starting a CAD Design

1. **Create a project folder**:
   ```bash
   cd CAD_Files/Person_X/  # Replace X with your number
   mkdir MyFirstProject
   cd MyFirstProject
   ```

2. **Create a README**:
   ```bash
   echo "# My First Project" > README.md
   echo "Design objectives: [Describe your design]" >> README.md
   ```

3. **Work on your CAD file**:
   - Open your CAD software
   - Create or import your design
   - Save files in this project folder
   - Export as STEP format for sharing

4. **Document your work**:
   - Edit README.md with design notes
   - Include key dimensions or specifications

5. **Commit documentation** (not the large CAD files):
   ```bash
   git add README.md
   git commit -m "Add initial documentation for MyFirstProject"
   git push
   ```

### Starting an FEM Analysis

1. **Create analysis folder**:
   ```bash
   cd FEM_Analysis/Person_X/  # Replace X with your number
   mkdir MyFirstAnalysis
   cd MyFirstAnalysis
   ```

2. **Document analysis setup**:
   Create README.md with:
   - Analysis objectives
   - Software and version
   - Geometry source
   - Material properties
   - Boundary conditions
   - Expected outputs

3. **Run your analysis**:
   - Import geometry
   - Create mesh
   - Apply loads and constraints
   - Run simulation
   - Large result files are automatically ignored by Git

4. **Export results**:
   - Create summary PDF report
   - Export key plots as images (PNG/JPG)
   - Save small data files if needed

5. **Commit results summary**:
   ```bash
   git add README.md results_summary.pdf stress_plot.png
   git commit -m "Add FEM results for MyFirstAnalysis"
   git push
   ```

## Daily Workflow

### Morning Routine
1. **Pull latest changes**:
   ```bash
   git pull
   ```

2. **Review what's new**:
   - Check commit messages
   - Read updated documentation
   - Review shared files

### During Work
1. Work in your personal folders
2. Document as you go
3. Export summaries and reports

### End of Day
1. **Stage changes**:
   ```bash
   git add .
   ```

2. **Commit with clear message**:
   ```bash
   git commit -m "Describe what you did today"
   ```

3. **Push to share**:
   ```bash
   git push
   ```

## Sharing Your Work

### When to Share CAD Files
Share when your design is:
- ✅ Finalized (or at a stable milestone)
- ✅ Documented with README
- ✅ Exported as STEP format
- ✅ Ready for team review

### How to Share CAD Files
1. Copy files to `CAD_Files/Shared/ProjectName/`
2. Include comprehensive documentation
3. Commit the documentation:
   ```bash
   cd CAD_Files/Shared/ProjectName/
   git add README.md
   git commit -m "Share finalized design for ProjectName"
   git push
   ```

### When to Share FEM Results
Share when your analysis is:
- ✅ Complete and verified
- ✅ Documented with assumptions
- ✅ Summarized in PDF report
- ✅ Ready for team discussion

### How to Share FEM Results
1. Copy summary to `FEM_Analysis/Shared/ProjectName/`
2. Include all documentation
3. Commit and push:
   ```bash
   cd FEM_Analysis/Shared/ProjectName/
   git add README.md results_summary.pdf *.png
   git commit -m "Share FEM analysis results for ProjectName"
   git push
   ```

## Common Tasks

### Checking Repository Status
```bash
git status
```
Shows what files have changed.

### Viewing Recent Changes
```bash
git log --oneline -10
```
Shows last 10 commits.

### Pulling Latest Updates
```bash
git pull
```
Downloads and merges latest changes.

### Creating a New Branch (Advanced)
```bash
git checkout -b feature/my-new-feature
```
Creates a branch for experimental work.

## Tips for Success

### DO:
- ✅ Commit documentation frequently
- ✅ Write clear commit messages
- ✅ Pull before you push
- ✅ Document assumptions
- ✅ Ask questions early
- ✅ Review teammates' work

### DON'T:
- ❌ Commit large CAD/FEM files
- ❌ Push without testing
- ❌ Overwrite others' work
- ❌ Skip documentation
- ❌ Work in isolation
- ❌ Forget to pull updates

## Getting Help

### Built-in Help
- Read `COLLABORATION_GUIDELINES.md` for detailed workflows
- Check folder README files for specific guidance
- Review `.gitignore` to see what files are ignored

### Git Help
```bash
git help <command>
```
Example: `git help commit`

### Team Help
- Open a GitHub Issue for questions
- Ask in team chat/email
- Review existing Issues for similar problems

## Troubleshooting

### "Large files detected"
- Check if you're accidentally committing CAD/FEM files
- Review `.gitignore` file
- Use `git rm --cached filename` to unstage

### "Merge conflict"
- Don't panic! This is normal
- Pull latest changes: `git pull`
- Edit conflicted files manually
- Commit the resolution

### "Permission denied"
- Check your GitHub access
- Verify SSH keys or HTTPS credentials
- Contact repository administrator

## Next Steps

1. ✅ Complete this quick start guide
2. ✅ Create your first project
3. ✅ Share something with the team
4. ✅ Review a teammate's work
5. ✅ Read detailed collaboration guidelines

## Resources

- [Git Basics Tutorial](https://git-scm.com/docs/gittutorial)
- [GitHub Guides](https://guides.github.com/)
- Repository README: `../../../README.md`
- Collaboration Guidelines: `COLLABORATION_GUIDELINES.md`

---

**Ready to start?** Create your first project and share it with the team!
