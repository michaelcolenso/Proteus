# Job Application Tracking System

This directory helps you track all job applications in one place, version-controlled with your CV.

## Structure

```
applications/
├── tracker.md              # Main tracking spreadsheet (table format)
├── 2025-01-company-a.md   # Detailed notes per application
├── 2025-01-company-b.md
└── responses/              # Interview prep and follow-up notes
    ├── company-a-interview-prep.md
    └── company-a-thank-you.md
```

## Using the Tracker

1. **tracker.md** - Update this markdown table for each application:
   - Date applied
   - Company name
   - Position title
   - CV variant used
   - Cover letter template used
   - Status (Applied, Phone Screen, Interview, Offer, Rejected)
   - Next action/follow-up date

2. **Individual Application Files** - Create `YYYY-MM-DD_company-name.md` for each application with:
   - Job posting details (URL, key requirements)
   - Why you're interested
   - Research notes about the company
   - Key talking points for interviews
   - Customizations made to CV/cover letter

3. **responses/** - Store interview prep notes, thank you emails, follow-ups

## Benefits

- **Version Control**: All applications tracked in git
- **Historical Record**: See what worked and what didn't
- **Interview Prep**: Quick reference to what you wrote in application
- **Pattern Recognition**: Identify which CV variants get best response
- **Follow-Up Reminders**: Track when to follow up
- **Portfolio Building**: Document your job search journey

## Example Workflow

```bash
# 1. Create application file
echo "# ABC Construction - Senior PM Application" > applications/2025-01-15_abc-construction.md

# 2. Add details to the application file
# (company research, job requirements, why interested)

# 3. Generate appropriate CV variant
./generate.sh senior-pm

# 4. Customize cover letter
cp letters/senior_pm.typ letter.typ
# Edit letter.typ with company-specific details
typst compile letter.typ

# 5. Update tracker.md with new row

# 6. Submit application

# 7. Create interview prep notes if you get a call
# applications/responses/abc-construction-interview-prep.md
```

## Tips

- Update tracker.md immediately after applying (while details are fresh)
- Review tracker weekly to identify follow-up opportunities
- Note which CV variant was used - helps optimize over time
- Save job posting text in application file (postings often get removed)
- Track recruiter contacts separately if using recruiters
