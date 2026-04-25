#!/bin/bash
# CV Generation Script
# Compiles CV and cover letter

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to compile and show status
compile_file() {
    local source=$1
    local output=$2
    local description=$3

    echo -e "${BLUE}Compiling ${source}...${NC}"
    if typst compile "${source}" "${output}"; then
        echo -e "${GREEN}✓ ${description} compiled successfully${NC}"
        echo -e "  Output: ${output}"
        return 0
    else
        echo -e "${YELLOW}✗ Failed to compile ${source}${NC}"
        return 1
    fi
}

# Main script
case $1 in
    "cv"|"")
        echo "=== Generating CV ==="
        compile_file "cv.typ" "cv.pdf" "CV"
        ;;

    "letter")
        echo "=== Generating Cover Letter ==="
        compile_file "letter.typ" "letter.pdf" "Cover Letter"
        ;;

    "portfolio")
        echo "=== Generating Luxury Residential Portfolio ==="
        compile_file "portfolio.typ" "portfolio.pdf" "Portfolio"
        ;;

    "all")
        echo "=== Generating All Documents ==="
        echo ""
        compile_file "cv.typ" "cv.pdf" "CV"
        echo ""
        compile_file "letter.typ" "letter.pdf" "Cover Letter"
        echo ""
        compile_file "portfolio.typ" "portfolio.pdf" "Portfolio"
        echo ""
        echo -e "${GREEN}=== All documents compiled ===${NC}"
        ;;

    "watch")
        target=${2:-cv}
        case $target in
            "cv")
                echo "Watching cv.typ (Ctrl+C to stop)"
                typst watch --font-path otfs cv.typ
                ;;
            "letter")
                echo "Watching letter.typ (Ctrl+C to stop)"
                typst watch --font-path otfs letter.typ
                ;;
            "portfolio")
                echo "Watching portfolio.typ (Ctrl+C to stop)"
                typst watch --font-path otfs portfolio.typ
                ;;
            *)
                echo "Unknown watch target: $target"
                echo "Available targets: cv, letter, portfolio"
                exit 1
                ;;
        esac
        ;;

    "export")
        if [ -z "$2" ]; then
            formats="all"
        else
            shift
            formats="$@"
        fi

        echo "=== Exporting CV to format(s): $formats ==="
        python3 scripts/export_cv.py cv --formats $formats
        ;;

    "autopilot")
        if [ -z "$2" ]; then
            echo "Usage: ./generate.sh autopilot <job_posting.txt> [--update-tracker]"
            exit 1
        fi
        shift
        echo "=== Building application autopilot brief ==="
        python3 scripts/application_autopilot.py --file "$@"
        ;;

    "autopilot-ui")
        echo "=== Launching application autopilot UI ==="
        python3 scripts/autopilot_ui.py "${@:2}"
        ;;

    "discover")
        echo "=== Scanning for new jobs (one-shot) ==="
        python3 scripts/job_discovery.py "${@:2}"
        ;;

    "discover-auto")
        echo "=== Scanning for new jobs + auto-generating briefs ==="
        python3 scripts/job_discovery.py --auto "${@:2}"
        ;;

    "discover-daemon")
        echo "=== Job discovery daemon (Ctrl+C to stop) ==="
        python3 scripts/job_discovery.py --daemon "${@:2}"
        ;;

    "clean")
        echo "=== Cleaning compiled PDFs ==="
        rm -f cv.pdf letter.pdf portfolio.pdf
        echo -e "${GREEN}✓ Cleaned all PDF files${NC}"
        ;;

    "help"|"--help"|"-h")
        echo "CV Generation Script"
        echo ""
        echo "Usage: ./generate.sh [command]"
        echo ""
        echo "Commands:"
        echo "  cv              Generate CV (default)"
        echo "  letter          Generate cover letter"
        echo "  portfolio       Generate luxury residential portfolio"
        echo "  all             Generate CV, cover letter, and portfolio"
        echo "  watch [target]  Watch and auto-compile on changes (cv, letter, or portfolio)"
        echo "  export [formats] Export CV to multiple formats"
        echo "  autopilot <file> Generate tailored application brief from job posting"
        echo "  autopilot-ui [args] Launch local web UI for autopilot"
        echo "  discover        Scan all sources for new jobs (one-shot)"
        echo "  discover-auto   Scan + auto-generate briefs for top matches"
        echo "  discover-daemon Continuously poll all sources for new jobs"
        echo "  clean           Remove all compiled PDFs"
        echo "  help            Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./generate.sh                    # Compile CV"
        echo "  ./generate.sh cv                 # Compile CV"
        echo "  ./generate.sh letter             # Compile cover letter"
        echo "  ./generate.sh all                # Compile everything"
        echo "  ./generate.sh watch              # Auto-compile CV on changes"
        echo "  ./generate.sh watch letter       # Auto-compile letter on changes"
        echo "  ./generate.sh export             # Export CV to all formats"
        echo "  ./generate.sh export txt html    # Export CV to specific formats"
        echo "  ./generate.sh autopilot sample_job_posting.txt"
        echo "  ./generate.sh autopilot-ui --port 8787"
        echo "  ./generate.sh discover           # One-shot scan"
        echo "  ./generate.sh discover-auto      # Scan + auto-generate briefs"
        echo "  ./generate.sh discover-daemon    # Continuous polling"
        echo "  ./generate.sh discover --reset   # Clear cache, rescan everything"
        echo "  ./generate.sh clean              # Remove PDFs"
        echo ""
        echo "Export Formats:"
        echo "  • pdf      - Standard PDF (via Typst)"
        echo "  • txt      - Plain text (for online forms)"
        echo "  • md       - Markdown (for GitHub/LinkedIn)"
        echo "  • html     - Styled HTML (for portfolio)"
        echo "  • all      - All of the above"
        echo ""
        echo "Note: Exporting requires Python 3 and optionally pdftotext/pandoc"
        echo ""
        ;;

    *)
        echo "Unknown command: $1"
        echo "Run './generate.sh help' for usage information"
        exit 1
        ;;
esac
